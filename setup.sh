#!/bin/bash

# AdmitAI Setup and Deployment Script
# This script sets up the AdmitAI platform with all integrated tech stack services

echo "🚀 AdmitAI Platform Setup & Deployment"
echo "======================================"

# Function to print colored output
print_status() {
    echo -e "\e[34m[INFO]\e[0m $1"
}

print_success() {
    echo -e "\e[32m[SUCCESS]\e[0m $1"
}

print_error() {
    echo -e "\e[31m[ERROR]\e[0m $1"
}

print_warning() {
    echo -e "\e[33m[WARNING]\e[0m $1"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root"
   exit 1
fi

# Check system requirements
print_status "Checking system requirements..."

# Check Python version
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is required but not installed"
    exit 1
fi

python_version=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" = "$required_version" ]; then
    print_success "Python $python_version is installed"
else
    print_error "Python 3.8+ is required. Current version: $python_version"
    exit 1
fi

# Check Node.js version
if ! command -v node &> /dev/null; then
    print_warning "Node.js not found. Installing Node.js..."
    curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
    sudo apt-get install -y nodejs
fi

node_version=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$node_version" -ge 14 ]; then
    print_success "Node.js $(node --version) is installed"
else
    print_error "Node.js 14+ is required"
    exit 1
fi

# Create virtual environment
print_status "Setting up Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_status "Virtual environment already exists"
fi

# Activate virtual environment
source venv/bin/activate
print_success "Virtual environment activated"

# Install Python dependencies
print_status "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
print_success "Python dependencies installed"

# Install Node.js dependencies
print_status "Installing Node.js dependencies..."
npm install
print_success "Node.js dependencies installed"

# Create necessary directories
print_status "Creating necessary directories..."
mkdir -p uploads
mkdir -p logs
mkdir -p instance
mkdir -p temp
print_success "Directories created"

# Copy environment file template
if [ ! -f ".env" ]; then
    print_status "Creating environment configuration..."
    cp .env.example .env
    print_warning "Please edit .env file with your API keys and configuration"
    print_warning "Required API keys:"
    echo "  - OPENAI_API_KEY or GEMINI_API_KEY (for AI features)"
    echo "  - ELEVENLABS_API_KEY (for text-to-speech)"
    echo "  - AWS credentials (for cloud deployment)"
    echo "  - Webhook URLs for n8n/Make.com (for automation)"
else
    print_status ".env file already exists"
fi

# Initialize database
print_status "Initializing database..."
python3 -c "
from app import app, db
with app.app_context():
    db.create_all()
    print('Database initialized successfully')
"
print_success "Database initialized"

# Create systemd service file (optional)
create_systemd_service() {
    print_status "Creating systemd service file..."
    
    cat > admitai.service << EOF
[Unit]
Description=AdmitAI College Admission Platform
After=network.target

[Service]
Type=simple
User=$(whoami)
WorkingDirectory=$(pwd)
Environment=PATH=$(pwd)/venv/bin
ExecStart=$(pwd)/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF

    print_success "Systemd service file created: admitai.service"
    print_status "To install: sudo cp admitai.service /etc/systemd/system/"
    print_status "To enable: sudo systemctl enable admitai"
    print_status "To start: sudo systemctl start admitai"
}

# Create nginx configuration (optional)
create_nginx_config() {
    print_status "Creating nginx configuration..."
    
    cat > admitai.nginx << EOF
server {
    listen 80;
    server_name admitai.local;

    # Static files
    location /static {
        alias $(pwd)/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Frontend
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    # API Backend
    location /api {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    # Chatbot endpoint
    location /chatbot {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

    print_success "Nginx configuration created: admitai.nginx"
    print_status "To install: sudo cp admitai.nginx /etc/nginx/sites-available/admitai"
    print_status "To enable: sudo ln -s /etc/nginx/sites-available/admitai /etc/nginx/sites-enabled/"
    print_status "Test config: sudo nginx -t"
    print_status "Reload nginx: sudo systemctl reload nginx"
}

# Create docker configuration
create_docker_config() {
    print_status "Creating Docker configuration..."
    
    cat > Dockerfile << EOF
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    curl \\
    nodejs \\
    npm \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy package.json for node dependencies
COPY package*.json ./
RUN npm install

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p uploads logs instance temp

# Expose ports
EXPOSE 5000 8000

# Create startup script
RUN echo '#!/bin/bash\\n\\
python app.py &\\n\\
node server.js &\\n\\
wait' > start.sh && chmod +x start.sh

CMD ["./start.sh"]
EOF

    cat > docker-compose.yml << EOF
version: '3.8'

services:
  admitai:
    build: .
    ports:
      - "5000:5000"
      - "8000:8000"
    environment:
      - FLASK_ENV=production
    volumes:
      - ./uploads:/app/uploads
      - ./logs:/app/logs
      - ./instance:/app/instance
    env_file:
      - .env
    restart: unless-stopped

  mongodb:
    image: mongo:5.0
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db
    environment:
      - MONGO_INITDB_DATABASE=mht_cet_admissions_top20
    restart: unless-stopped

volumes:
  mongodb_data:
EOF

    print_success "Docker configuration created"
    print_status "To build and run: docker-compose up --build"
}

# Function to run setup
setup_production_server() {
    print_status "Setting up production server..."
    
    # Update system packages
    sudo apt-get update
    sudo apt-get install -y nginx supervisor certbot python3-certbot-nginx
    
    # Create directories
    sudo mkdir -p /var/log/admitai
    sudo chown $(whoami):$(whoami) /var/log/admitai
    
    # Setup supervisor configuration
    cat > admitai-supervisor.conf << EOF
[program:admitai-backend]
command=$(pwd)/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:5000 app:app
directory=$(pwd)
user=$(whoami)
autostart=true
autorestart=true
stdout_logfile=/var/log/admitai/backend.log
stderr_logfile=/var/log/admitai/backend_error.log

[program:admitai-frontend]
command=node server.js
directory=$(pwd)
user=$(whoami)
autostart=true
autorestart=true
stdout_logfile=/var/log/admitai/frontend.log
stderr_logfile=/var/log/admitai/frontend_error.log
environment=PORT=8000
EOF

    sudo cp admitai-supervisor.conf /etc/supervisor/conf.d/
    sudo supervisorctl reread
    sudo supervisorctl update
    
    print_success "Production server setup completed"
}

# Function to deploy to AWS
deploy_to_aws() {
    print_status "Preparing AWS deployment..."
    
    # Check if AWS CLI is installed
    if ! command -v aws &> /dev/null; then
        print_error "AWS CLI is required for deployment"
        print_status "Install with: pip install awscli"
        return 1
    fi
    
    # Create deployment package
    print_status "Creating deployment package..."
    tar -czf admitai-deploy.tar.gz \
        --exclude=venv \
        --exclude=node_modules \
        --exclude=.git \
        --exclude=__pycache__ \
        --exclude=*.pyc \
        --exclude=logs \
        --exclude=temp \
        .
    
    print_success "Deployment package created: admitai-deploy.tar.gz"
    print_status "Use AWS CloudFormation template from aws_integration.py for deployment"
}

# Main menu
show_menu() {
    echo
    echo "Setup Options:"
    echo "1. Full setup (recommended for first-time setup)"
    echo "2. Create systemd service"
    echo "3. Create nginx configuration"
    echo "4. Create Docker configuration"
    echo "5. Setup production server"
    echo "6. Deploy to AWS"
    echo "7. Start development servers"
    echo "8. Test installation"
    echo "9. Exit"
    echo
}

# Test installation
test_installation() {
    print_status "Testing installation..."
    
    # Test Python app
    python3 -c "
import sys
sys.path.append('.')
try:
    from app import app
    from config import Config
    print('✓ Flask app imports successfully')
    print('✓ Configuration loaded')
    
    # Test AI services
    from ai_services import ai_service
    status = ai_service.get_service_status()
    print(f'✓ AI services status: {status}')
    
    # Test voice services
    from voice_ai_services import voice_ai_service
    voice_status = voice_ai_service.get_voice_service_status()
    print(f'✓ Voice AI services status: {voice_status}')
    
    # Test automation
    from workflow_automation import workflow_manager
    automation_status = workflow_manager.get_automation_status()
    print(f'✓ Automation services status: {automation_status}')
    
    # Test AWS
    from aws_integration import aws_manager
    aws_status = aws_manager.get_aws_status()
    print(f'✓ AWS services status: {aws_status}')
    
    print('✓ All imports successful')
except Exception as e:
    print(f'✗ Import error: {e}')
    sys.exit(1)
"
    
    if [ $? -eq 0 ]; then
        print_success "Installation test passed"
    else
        print_error "Installation test failed"
        return 1
    fi
}

# Start development servers
start_dev_servers() {
    print_status "Starting development servers..."
    
    # Start Flask backend
    print_status "Starting Flask backend on port 5000..."
    python3 app.py &
    FLASK_PID=$!
    
    sleep 2
    
    # Start Node.js frontend
    print_status "Starting Node.js frontend on port 8000..."
    node server.js &
    NODE_PID=$!
    
    sleep 2
    
    print_success "Development servers started"
    echo "Backend: http://localhost:5000"
    echo "Frontend: http://localhost:8000"
    echo
    print_status "Press Ctrl+C to stop servers"
    
    # Wait for user interrupt
    trap "print_status 'Stopping servers...'; kill $FLASK_PID $NODE_PID 2>/dev/null; exit 0" INT
    wait
}

# Main execution
if [ "$1" = "--auto" ]; then
    # Automated setup
    print_status "Running automated setup..."
    create_docker_config
    test_installation
    print_success "Automated setup completed"
    exit 0
fi

# Interactive menu
while true; do
    show_menu
    read -p "Choose an option [1-9]: " choice
    
    case $choice in
        1)
            create_docker_config
            test_installation
            print_success "Full setup completed"
            ;;
        2)
            create_systemd_service
            ;;
        3)
            create_nginx_config
            ;;
        4)
            create_docker_config
            ;;
        5)
            setup_production_server
            ;;
        6)
            deploy_to_aws
            ;;
        7)
            start_dev_servers
            ;;
        8)
            test_installation
            ;;
        9)
            print_success "Goodbye!"
            exit 0
            ;;
        *)
            print_error "Invalid option. Please try again."
            ;;
    esac
done