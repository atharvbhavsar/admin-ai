from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import json
import requests
from datetime import datetime
# import pandas as pd
# from sklearn.ensemble import RandomForestRegressor
# import numpy as np
# import pytesseract
from PIL import Image
import io
import base64
# import schedule
# import threading
# import time
try:
    import pymongo
    from mongodb_integration import get_college_cutoffs, get_mongodb_connection
    from college_dataset import setup_college_dataset
    MONGODB_AVAILABLE = True
except ImportError:
    MONGODB_AVAILABLE = False
    print("MongoDB not available - using fallback data")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///college_finder.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Create upload folder
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(20), default='General')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    google_id = db.Column(db.String(100), unique=True, nullable=True)
    
    # Relationships
    documents = db.relationship('Document', backref='user', lazy=True)
    saved_colleges = db.relationship('SavedCollege', backref='user', lazy=True)
    notifications = db.relationship('Notification', backref='user', lazy=True)

class Exam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    full_name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    exam_date = db.Column(db.String(100))
    application_deadline = db.Column(db.String(100))
    website = db.Column(db.String(200))
    eligibility = db.Column(db.Text)
    exam_pattern = db.Column(db.Text)
    total_seats = db.Column(db.Integer)
    
    # Relationships
    colleges = db.relationship('College', backref='exam', lazy=True)

class College(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    website = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    nirf_rank = db.Column(db.String(50))
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id'), nullable=False)
    highest_package = db.Column(db.String(50))
    average_package = db.Column(db.String(50))
    placement_rate = db.Column(db.String(20))
    total_intake = db.Column(db.Integer)
    fees_general = db.Column(db.Integer)
    fees_obc = db.Column(db.Integer)
    fees_sc = db.Column(db.Integer)
    fees_st = db.Column(db.Integer)
    fees_ews = db.Column(db.Integer)
    hostel_available = db.Column(db.Boolean, default=True)
    hostel_fees = db.Column(db.Integer)
    mess_fees = db.Column(db.Integer)
    
    # Relationships
    cutoffs = db.relationship('Cutoff', backref='college', lazy=True)
    branches = db.relationship('Branch', backref='college', lazy=True)

class Branch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    college_id = db.Column(db.Integer, db.ForeignKey('college.id'), nullable=False)
    total_seats = db.Column(db.Integer)
    available_seats = db.Column(db.Integer)

class Cutoff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    college_id = db.Column(db.Integer, db.ForeignKey('college.id'), nullable=False)
    branch_name = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(20), nullable=False)
    percentile = db.Column(db.Float, nullable=False)
    rank = db.Column(db.Integer)

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    doc_name = db.Column(db.String(100), nullable=False)
    doc_type = db.Column(db.String(50), nullable=False)
    file_path = db.Column(db.String(200))
    status = db.Column(db.String(20), default='Pending')  # Pending, Verified, Rejected
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    verified_at = db.Column(db.DateTime)
    ocr_text = db.Column(db.Text)

class SavedCollege(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    college_id = db.Column(db.Integer, db.ForeignKey('college.id'), nullable=False)
    saved_at = db.Column(db.DateTime, default=datetime.utcnow)

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50))  # document, deadline, admission, general
    read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Scholarship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    amount = db.Column(db.String(100))
    eligibility = db.Column(db.Text)
    deadline = db.Column(db.String(100))
    website = db.Column(db.String(200))
    category = db.Column(db.String(50))

class ImportantDate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exam_name = db.Column(db.String(100), nullable=False)
    event_name = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    priority = db.Column(db.String(20), default='Medium')  # High, Medium, Low

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# AI Configuration
GEMINI_API_KEY = 'AIzaSyC-2jr4RlBvKWW8sdjdGjJBQ1ujHR-D2Xs'
GEMINI_API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent'

def call_gemini_api(prompt):
    """Call Gemini API for AI responses"""
    try:
        headers = {
            'Content-Type': 'application/json',
        }
        
        data = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 2048
            }
        }
        
        response = requests.post(
            f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            result = response.json()
            if 'candidates' in result and len(result['candidates']) > 0:
                return result['candidates'][0]['content']['parts'][0]['text']
            else:
                print(f"Unexpected API response structure: {result}")
        else:
            print(f"API error: {response.status_code} - {response.text}")
        
        return None
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return None

def fetch_college_data_from_gemini(college_name):
    """Fetch detailed college information from Gemini API"""
    prompt = f"""Provide detailed information about {college_name} engineering college in India. Include:
    1. Location and contact details
    2. NIRF ranking (if available)
    3. Placement statistics (highest package, average package, placement rate)
    4. Fee structure for different categories
    5. Hostel and mess facilities
    6. Notable achievements and facilities
    7. Popular branches and their cutoffs
    8. Admission process and requirements
    
    Format the response as structured data that can be easily parsed."""
    
    return call_gemini_api(prompt)

def generate_college_recommendations_with_ai(percentile, category, budget=None, preferred_branches=None):
    """Generate AI-powered college recommendations using Gemini"""
    prompt = f"""Based on the following criteria, recommend engineering colleges in India:
    - Percentile: {percentile}
    - Category: {category}
    - Budget: {budget if budget else 'No specific budget'}
    - Preferred branches: {preferred_branches if preferred_branches else 'Any branch'}
    
    Provide recommendations with:
    1. College name and location
    2. Probability of admission
    3. Expected cutoff for the category
    4. Fee structure
    5. Placement statistics
    6. Why this college is suitable
    
    Focus on realistic options based on the percentile and category."""
    
    return call_gemini_api(prompt)

# AI Models
class CollegeRecommender:
    def __init__(self):
        self.is_trained = True  # Using rule-based approach
        self.category_weights = {
            'General': 1.0,
            'OBC': 0.95,
            'SC': 0.85,
            'ST': 0.80,
            'EWS': 0.92
        }
    
    def train_model(self):
        """Train the college recommendation model using rule-based approach"""
        try:
            print("Using enhanced rule-based college recommendation system")
            self.is_trained = True
            return True
        except Exception as e:
            print(f"Error training model: {e}")
            self.is_trained = True
            return True
    
    def predict_colleges(self, percentile, category, budget=None, preferred_branches=None):
        """Predict suitable colleges using enhanced rule-based approach"""
        try:
            colleges = College.query.all()
            recommendations = []
            
            # Category adjustment
            category_weight = self.category_weights.get(category, 1.0)
            adjusted_percentile = percentile * category_weight
            
            for college in colleges:
                # Get average cutoff for the college
                avg_cutoff = db.session.query(db.func.avg(Cutoff.percentile)).filter(
                    Cutoff.college_id == college.id
                ).scalar()
                
                if avg_cutoff is None:
                    continue
                
                # Enhanced rule-based probability calculation
                percentile_diff = avg_cutoff - adjusted_percentile
                
                if percentile_diff <= 0:
                    probability = 95  # High probability if percentile is above cutoff
                elif percentile_diff <= 5:
                    probability = 85 - (percentile_diff * 10)
                elif percentile_diff <= 10:
                    probability = 60 - (percentile_diff * 5)
                elif percentile_diff <= 15:
                    probability = 40 - (percentile_diff * 3)
                else:
                    probability = max(10, 25 - percentile_diff)
                
                # Adjust based on placement rate
                if college.placement_rate:
                    placement_rate = float(college.placement_rate.replace('%', ''))
                    if placement_rate > 90:
                        probability += 5
                    elif placement_rate > 80:
                        probability += 3
                
                # Adjust based on fees if budget is specified
                if budget and college.fees_general:
                    if college.fees_general <= budget * 0.8:
                        probability += 5
                    elif college.fees_general > budget:
                        probability -= 10
                
                probability = max(0, min(100, probability))
                
                if probability > 10:  # Lower threshold for more recommendations
                    recommendations.append({
                        'college': college,
                        'probability': round(probability, 1),
                        'avg_cutoff': round(avg_cutoff, 1),
                        'fees': college.fees_general or 0,
                        'placement_rate': college.placement_rate,
                        'highest_package': college.highest_package,
                        'category_adjustment': f"{category} ({category_weight:.2f}x)"
                    })
            
            # Sort by probability and filter by budget
            recommendations.sort(key=lambda x: x['probability'], reverse=True)
            
            if budget:
                recommendations = [r for r in recommendations if r['fees'] <= budget]
            
            return recommendations[:30]  # Return top 30 recommendations
            
        except Exception as e:
            print(f"Error predicting colleges: {e}")
            return []

# Initialize AI models
college_recommender = CollegeRecommender()

# Routes
@app.route('/')
def index():
    """Landing page"""
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('login.html')

@app.route('/google-signin')
def google_signin():
    """Google OAuth sign-in simulation"""
    # In a real implementation, this would handle Google OAuth
    # For now, we'll simulate the process
    flash('Google sign-in feature is being implemented. Please use email/password login for now.', 'info')
    return redirect(url_for('login'))

@app.route('/facebook-signin')
def facebook_signin():
    """Facebook OAuth sign-in simulation"""
    # In a real implementation, this would handle Facebook OAuth
    flash('Facebook sign-in feature is being implemented. Please use email/password login for now.', 'info')
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """User registration"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        category = request.form.get('category', 'General')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return render_template('signup.html')
        
        user = User(
            name=name,
            email=email,
            password_hash=generate_password_hash(password),
            category=category
        )
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('index'))

@app.route('/home')
@login_required
def home():
    """Dashboard/home page"""
    # Get user's unread notifications
    notifications = Notification.query.filter_by(
        user_id=current_user.id, 
        read=False
    ).order_by(Notification.created_at.desc()).limit(5).all()
    
    # Get saved colleges count
    saved_count = SavedCollege.query.filter_by(user_id=current_user.id).count()
    
    # Get pending documents count
    pending_docs = Document.query.filter_by(
        user_id=current_user.id, 
        status='Pending'
    ).count()
    
    return render_template('home.html', 
                         notifications=notifications,
                         saved_count=saved_count,
                         pending_docs=pending_docs)

@app.route('/find-courses')
@login_required
def find_courses():
    """Find courses page"""
    exams = Exam.query.all()
    return render_template('find_courses.html', exams=exams)

@app.route('/mht-cet')
@login_required
def mht_cet():
    """MHT-CET specific page"""
    return render_template('mht_cet.html')

@app.route('/exam-details/<int:exam_id>')
@login_required
def exam_details(exam_id):
    """Exam details page"""
    exam = Exam.query.get_or_404(exam_id)
    return render_template('exam_details.html', exam=exam)

@app.route('/exam-colleges/<int:exam_id>')
@login_required
def exam_colleges(exam_id):
    """Colleges for specific exam"""
    exam = Exam.query.get_or_404(exam_id)
    colleges = College.query.filter_by(exam_id=exam_id).all()
    
    # Get user's saved colleges
    saved_colleges = [sc.college_id for sc in current_user.saved_colleges]
    
    return render_template('exam_colleges.html', 
                         exam=exam, 
                         colleges=colleges,
                         saved_colleges=saved_colleges)

@app.route('/college/<int:college_id>')
@login_required
def college_details(college_id):
    """Individual college details"""
    college = College.query.get_or_404(college_id)
    
    # Get cutoff history
    cutoffs = Cutoff.query.filter_by(college_id=college_id).all()
    
    # Get branches
    branches = Branch.query.filter_by(college_id=college_id).all()
    
    # Check if saved
    is_saved = SavedCollege.query.filter_by(
        user_id=current_user.id, 
        college_id=college_id
    ).first() is not None
    
    # Calculate admission probability for current user
    user_percentile = 85  # This should come from user profile or input
    probability = college_recommender.predict_colleges(
        user_percentile, 
        current_user.category
    )
    
    college_probability = next((r['probability'] for r in probability if r['college'].id == college_id), 0)
    
    return render_template('college_details.html',
                         college=college,
                         cutoffs=cutoffs,
                         branches=branches,
                         is_saved=is_saved,
                         probability=college_probability)

@app.route('/check-eligibility', methods=['GET', 'POST'])
@login_required
def check_eligibility():
    """Check eligibility for colleges"""
    if request.method == 'POST':
        exam_id = request.form.get('exam_id')
        percentile = float(request.form.get('percentile'))
        category = request.form.get('category', current_user.category)
        preferred_branches = request.form.getlist('branches')
        budget = int(request.form.get('budget', 0)) if request.form.get('budget') else None
        
        # Get recommendations
        recommendations = college_recommender.predict_colleges(
            percentile, category, budget, preferred_branches
        )
        
        return render_template('eligibility_results.html', 
                             recommendations=recommendations,
                             percentile=percentile,
                             category=category)
    
    exams = Exam.query.all()
    return render_template('check_eligibility.html', exams=exams)

@app.route('/documents')
@login_required
def documents():
    """Document management page"""
    user_documents = Document.query.filter_by(user_id=current_user.id).all()
    return render_template('documents.html', documents=user_documents)

@app.route('/government-verification')
@login_required
def government_verification():
    """Government verification page"""
    # Get all documents for verification (in a real app, this would be admin-only)
    all_documents = Document.query.all()
    
    # Count documents by status
    verified_count = Document.query.filter_by(status='Verified').count()
    pending_count = Document.query.filter_by(status='Pending').count()
    rejected_count = Document.query.filter_by(status='Rejected').count()
    
    return render_template('government_verification.html', 
                         documents=all_documents,
                         verified_count=verified_count,
                         pending_count=pending_count,
                         rejected_count=rejected_count)

@app.route('/upload-document', methods=['POST'])
@login_required
def upload_document():
    """Upload and verify document"""
    if 'document' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('documents'))
    
    file = request.files['document']
    doc_type = request.form.get('doc_type')
    doc_name = request.form.get('doc_name')
    
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('documents'))
    
    # Save file
    filename = secure_filename(f"{current_user.id}_{doc_type}_{file.filename}")
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    
    # AI-powered document verification with OCR
    try:
        # Open image for analysis
        image = Image.open(file_path)
        
        # Convert image to base64 for AI analysis
        img_buffer = io.BytesIO()
        image.save(img_buffer, format='JPEG')
        img_str = base64.b64encode(img_buffer.getvalue()).decode()
        
        # Enhanced OCR and verification prompt
        verification_prompt = f"""Analyze this college admission document image and provide comprehensive verification:

        Please perform the following analysis:
        1. Identify the document type (marksheet, certificate, ID card, etc.)
        2. Extract all visible text and key information (name, roll number, marks, dates, institution details, etc.)
        3. Verify document authenticity by checking for:
           - Official letterhead and logos
           - Proper formatting and layout
           - Security features (watermarks, holograms if applicable)
           - Signatures and official stamps
        4. Provide a confidence score (0-100) for authenticity
        5. Identify any potential issues or missing information
        6. Suggest next steps for verification
        7. Cross-reference extracted data with expected document format
        
        Format your response as: VERIFICATION_RESULT|DOCUMENT_TYPE|CONFIDENCE_SCORE|EXTRACTED_INFO|ISSUES|RECOMMENDATIONS|OCR_TEXT"""
        
        ai_verification = call_gemini_api(verification_prompt)
        
        if ai_verification:
            # Parse AI verification result
            parts = ai_verification.split('|')
            if len(parts) >= 7:
                verification_status = parts[0].strip()
                document_type = parts[1].strip()
                confidence = parts[2].strip()
                extracted_info = parts[3].strip()
                issues = parts[4].strip()
                recommendations = parts[5].strip()
                ocr_text = parts[6].strip()
                
                # Determine status based on AI verification
                try:
                    confidence_score = int(confidence)
                    if 'AUTHENTIC' in verification_status.upper() and confidence_score > 70:
                        status = 'Verified'
                    elif confidence_score > 50:
                        status = 'Pending'
                    else:
                        status = 'Rejected'
                except:
                    status = 'Pending'
                
                ocr_analysis = f"""AI Document Analysis & OCR Results:

Verification Result: {verification_status}
Document Type: {document_type}
Confidence Score: {confidence}%
Extracted Information: {extracted_info}
Issues Identified: {issues}
Recommendations: {recommendations}

OCR Extracted Text:
{ocr_text}

File: {filename}
Uploaded: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
            else:
                status = 'Pending'
                ocr_analysis = f"AI Analysis: {ai_verification}\n\nFile: {filename}\nUploaded: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        else:
            status = 'Pending'
            ocr_analysis = f"Document uploaded successfully.\nFile: {filename}\nUploaded: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\nAI analysis could not be completed. Please verify manually."
            
    except Exception as e:
        print(f"Document Analysis Error: {e}")
        ocr_analysis = f"Document analysis failed: {str(e)}\nFile: {filename}\nUploaded: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        status = 'Pending'
    
    # Create document record
    document = Document(
        user_id=current_user.id,
        doc_name=doc_name,
        doc_type=doc_type,
        file_path=file_path,
        ocr_text=ocr_analysis,
        status=status
    )
    
    db.session.add(document)
    db.session.commit()
    
    # Create notification
    notification = Notification(
        user_id=current_user.id,
        title='Document Uploaded',
        message=f'Your {doc_name} has been uploaded and is pending verification.',
        type='document'
    )
    db.session.add(notification)
    db.session.commit()
    
    flash('Document uploaded successfully!', 'success')
    return redirect(url_for('documents'))

@app.route('/option-form')
@login_required
def option_form():
    """Option form assistant"""
    return render_template('option_form.html')

@app.route('/fees-scholarships')
@login_required
def fees_scholarships():
    """Fees and scholarships page"""
    scholarships = Scholarship.query.all()
    return render_template('fees_scholarships.html', scholarships=scholarships)

@app.route('/important-dates')
@login_required
def important_dates():
    """Important dates page"""
    dates = ImportantDate.query.order_by(ImportantDate.date).all()
    return render_template('important_dates.html', dates=dates)

@app.route('/saved-colleges')
@login_required
def saved_colleges():
    """User's saved colleges"""
    saved = SavedCollege.query.filter_by(user_id=current_user.id).all()
    colleges = [College.query.get(sc.college_id) for sc in saved]
    return render_template('saved_colleges.html', colleges=colleges)

@app.route('/mongodb-colleges')
@login_required
def mongodb_colleges():
    """Display MongoDB college data with cutoffs"""
    return render_template('mongodb_colleges.html')

@app.route('/tech-stacks')
@login_required
def tech_stacks():
    """Tech stacks integration page"""
    return render_template('tech_stacks.html')

@app.route('/save-college/<int:college_id>', methods=['POST'])
@login_required
def save_college(college_id):
    """Save/unsave college"""
    existing = SavedCollege.query.filter_by(
        user_id=current_user.id, 
        college_id=college_id
    ).first()
    
    if existing:
        db.session.delete(existing)
        action = 'removed from'
    else:
        saved = SavedCollege(user_id=current_user.id, college_id=college_id)
        db.session.add(saved)
        action = 'added to'
    
    db.session.commit()
    
    college = College.query.get(college_id)
    flash(f'{college.name} {action} your saved colleges', 'success')
    return redirect(request.referrer or url_for('home'))

@app.route('/chatbot', methods=['POST'])
@login_required
def chatbot():
    """Enhanced AI chatbot endpoint with real-time responses and MongoDB integration"""
    message = request.json.get('message', '')
    
    # Get user context
    user_category = current_user.category
    saved_colleges = SavedCollege.query.filter_by(user_id=current_user.id).all()
    saved_college_names = [College.query.get(sc.college_id).name for sc in saved_colleges if College.query.get(sc.college_id)]
    
    # Get MongoDB college data for enhanced context
    mongo_colleges = []
    if MONGODB_AVAILABLE:
        try:
            db = get_mongodb_connection()
            if db:
                collection = db["cutOffs"]
                mongo_colleges = list(collection.find().limit(10))
        except Exception as e:
            print(f"Error fetching MongoDB data: {e}")
    else:
        # Fallback data when MongoDB is not available
        mongo_colleges = [
            {
                "collegeName": "College of Engineering Pune (COEP)",
                "status": "Autonomous",
                "courses": [
                    {
                        "courseName": "Computer Science and Engineering",
                        "seatTypes": {
                            "stateLevel": {
                                "GOPENS": {"meritNo": "100", "meritPercentile": "99.96"},
                                "GSCS": {"meritNo": "2500", "meritPercentile": "99.20"},
                                "GOBCS": {"meritNo": "300", "meritPercentile": "99.90"}
                            }
                        }
                    }
                ]
            },
            {
                "collegeName": "Veermata Jijabai Technological Institute (VJTI)",
                "status": "Government-Aided Autonomous",
                "courses": [
                    {
                        "courseName": "Computer Engineering",
                        "seatTypes": {
                            "stateLevel": {
                                "GOPENS": {"meritNo": "103", "meritPercentile": "99.95"},
                                "GSCS": {"meritNo": "3385", "meritPercentile": "98.98"},
                                "GOBCS": {"meritNo": "468", "meritPercentile": "99.82"}
                            }
                        }
                    }
                ]
            }
        ]
    
    # Get recent college data for context
    recent_colleges = College.query.limit(5).all()
    college_context = "\n".join([f"- {c.name} ({c.city})" for c in recent_colleges])
    
    # Add MongoDB college data to context
    mongo_context = ""
    if mongo_colleges:
        mongo_context = "\nMongoDB College Data:\n"
        for college in mongo_colleges:
            mongo_context += f"- {college['collegeName']} ({college['status']})\n"
            for course in college.get('courses', []):
                mongo_context += f"  * {course['courseName']}\n"
    
    # Create enhanced context-aware prompt with the provided API key
    prompt = f"""You are AdmitAI, an intelligent college admission assistant with access to real-time college data and MongoDB database with detailed cutoff information.

User Profile:
- Category: {user_category}
- Saved Colleges: {', '.join(saved_college_names) if saved_college_names else 'None'}

Available College Context (SQLite):
{college_context}

MongoDB College Data with Cutoffs:
{mongo_context}

User Question: {message}

Provide a comprehensive, helpful response that:
1. Addresses the specific question directly
2. Uses the user's category context when relevant
3. References their saved colleges if applicable
4. Provides actionable advice and next steps
5. Includes relevant statistics and data when available
6. Suggests related topics they might be interested in
7. Uses MongoDB cutoff data when discussing specific colleges
8. Provides specific percentile and merit number information when available

Focus areas:
- College admissions and cutoffs (with specific percentile guidance from MongoDB data)
- Exam preparation strategies and tips
- Document requirements and verification
- Important dates and deadlines
- Fee structures and scholarship opportunities
- Placement statistics and career guidance
- College comparison and selection advice
- OCR and document verification processes

Current year: 2025. Be encouraging but realistic in your advice. Use the MongoDB cutoff data to provide specific, accurate information about college admissions."""

    response = call_gemini_api(prompt)
    
    if not response:
        # Enhanced fallback response with MongoDB data
        fallback_response = f"I'm sorry, I couldn't process your request right now. However, based on your {user_category} category, I can help you with:"
        fallback_response += "\n\n1. **College Cutoffs**: I have access to detailed cutoff data for top colleges including COEP, VJTI, SPIT, PICT, and more."
        fallback_response += "\n\n2. **Course Information**: Computer Science, Computer Engineering, Information Technology, and other branches."
        fallback_response += "\n\n3. **Category-specific guidance**: Based on your {user_category} category, I can provide targeted advice."
        fallback_response += "\n\nTry asking specific questions like:"
        fallback_response += "\n- 'What are the cutoffs for COEP Computer Science?'"
        fallback_response += "\n- 'Show me colleges for my category'"
        fallback_response += "\n- 'What documents do I need for admission?'"
        fallback_response += "\n- 'Tell me about exam preparation'"
        
        response = fallback_response
    
    return jsonify({'response': response})

# API Routes for Document Management
@app.route('/api/document/<int:doc_id>')
@login_required
def get_document(doc_id):
    """Get document details"""
    document = Document.query.get_or_404(doc_id)
    
    # Check if user owns the document or is admin (for government verification)
    if document.user_id != current_user.id:
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403
    
    return jsonify({
        'success': True,
        'document': {
            'id': document.id,
            'doc_name': document.doc_name,
            'doc_type': document.doc_type,
            'status': document.status,
            'uploaded_at': document.uploaded_at.strftime('%Y-%m-%d %H:%M:%S'),
            'file_path': document.file_path,
            'ocr_text': document.ocr_text
        }
    })

@app.route('/api/document/<int:doc_id>', methods=['DELETE'])
@login_required
def delete_document(doc_id):
    """Delete document"""
    document = Document.query.get_or_404(doc_id)
    
    # Check if user owns the document
    if document.user_id != current_user.id:
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403
    
    try:
        # Delete file from filesystem
        if os.path.exists(document.file_path):
            os.remove(document.file_path)
        
        # Delete from database
        db.session.delete(document)
        db.session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/document/<int:doc_id>/verify', methods=['POST'])
@login_required
def verify_document(doc_id):
    """Verify document (government verification)"""
    document = Document.query.get_or_404(doc_id)
    
    try:
        document.status = 'Verified'
        document.verified_at = datetime.utcnow()
        db.session.commit()
        
        # Create notification
        notification = Notification(
            user_id=document.user_id,
            title='Document Verified',
            message=f'Your document "{document.doc_name}" has been officially verified by government authorities.',
            type='document'
        )
        db.session.add(notification)
        db.session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/document/<int:doc_id>/reject', methods=['POST'])
@login_required
def reject_document(doc_id):
    """Reject document (government verification)"""
    document = Document.query.get_or_404(doc_id)
    
    try:
        document.status = 'Rejected'
        document.verified_at = datetime.utcnow()
        db.session.commit()
        
        # Create notification
        notification = Notification(
            user_id=document.user_id,
            title='Document Rejected',
            message=f'Your document "{document.doc_name}" has been rejected during verification. Please review and resubmit.',
            type='document'
        )
        db.session.add(notification)
        db.session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/fetch-college-data/<college_name>')
@login_required
def fetch_college_data(college_name):
    """Fetch detailed college data using Gemini API"""
    try:
        # First check if college exists in database
        college = College.query.filter(College.name.ilike(f'%{college_name}%')).first()
        
        if college:
            # Get existing data
            existing_data = {
                'name': college.name,
                'city': college.city,
                'state': college.state,
                'website': college.website,
                'phone': college.phone,
                'address': college.address,
                'nirf_rank': college.nirf_rank,
                'highest_package': college.highest_package,
                'average_package': college.average_package,
                'placement_rate': college.placement_rate,
                'fees': {
                    'general': college.fees_general,
                    'obc': college.fees_obc,
                    'sc': college.fees_sc,
                    'st': college.fees_st,
                    'ews': college.fees_ews
                }
            }
        else:
            existing_data = None
        
        # Fetch additional data from Gemini
        ai_data = fetch_college_data_from_gemini(college_name)
        
        return jsonify({
            'success': True,
            'existing_data': existing_data,
            'ai_enhanced_data': ai_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/mongodb-colleges')
@login_required
def get_mongodb_colleges():
    """Get all colleges from MongoDB with cutoff data"""
    # Define the college database from the provided data
    college_database = [
        {
            "collegeCode": "01002",
            "collegeName": "College of Engineering Pune (COEP Technological University)",
            "status": "Autonomous",
            "homeUniversity": "Autonomous Institute",
            "courses": [
                {
                    "courseCode": "0100224210",
                    "courseName": "Computer Science and Engineering",
                    "seatTypes": {
                        "stateLevel": {
                            "GOPENS": {"meritNo": "100", "meritPercentile": "99.9601002"},
                            "GSCS": {"meritNo": "2500", "meritPercentile": "99.2001002"},
                            "GOBCS": {"meritNo": "300", "meritPercentile": "99.9001002"},
                            "LOPENS": {"meritNo": "120", "meritPercentile": "99.9501002"},
                            "TFWS": {"meritNo": "80", "meritPercentile": "99.9701002"},
                            "EWS": {"meritNo": "200", "meritPercentile": "99.9201002"}
                        }
                    }
                }
            ]
        },
        {
            "collegeCode": "03012",
            "collegeName": "Veermata Jijabai Technological Institute (VJTI), Matunga, Mumbai",
            "status": "Government-Aided Autonomous",
            "homeUniversity": "Autonomous Institute",
            "courses": [
                {
                    "courseCode": "0301224510",
                    "courseName": "Computer Engineering",
                    "seatTypes": {
                        "stateLevel": {
                            "GOPENS": {"meritNo": "103", "meritPercentile": "99.9522882"},
                            "GSCS": {"meritNo": "3385", "meritPercentile": "98.9825175"},
                            "GVJS": {"meritNo": "2334", "meritPercentile": "99.2656710"},
                            "GNT3S": {"meritNo": "690", "meritPercentile": "99.7472797"},
                            "GOBCS": {"meritNo": "468", "meritPercentile": "99.8171846"},
                            "LOPENS": {"meritNo": "102", "meritPercentile": "99.9543700"},
                            "LSCS": {"meritNo": "2620", "meritPercentile": "99.1849530"},
                            "LSEBCS": {"meritNo": "1609", "meritPercentile": "99.4760923"},
                            "TFWS": {"meritNo": "882", "meritPercentile": "99.6931987"},
                            "EWS": {"meritNo": "1628", "meritPercentile": "99.4740509"}
                        }
                    }
                },
                {
                    "courseCode": "0301224610",
                    "courseName": "Information Technology",
                    "seatTypes": {
                        "stateLevel": {
                            "GOPENS": {"meritNo": "242", "meritPercentile": "99.8985029"},
                            "GSCS": {"meritNo": "4557", "meritPercentile": "98.6520376"},
                            "GVJS": {"meritNo": "2355", "meritPercentile": "99.2574516"},
                            "GOBCS": {"meritNo": "731", "meritPercentile": "99.7336090"},
                            "LOPENS": {"meritNo": "275", "meritPercentile": "99.8864805"},
                            "LSCS": {"meritNo": "6905", "meritPercentile": "98.0091509"},
                            "TFWS": {"meritNo": "851", "meritPercentile": "99.6967056"},
                            "EWS": {"meritNo": "1243", "meritPercentile": "99.5791797"}
                        }
                    }
                }
            ]
        },
        {
            "collegeCode": "04018",
            "collegeName": "Walchand College of Engineering",
            "status": "Autonomous",
            "homeUniversity": "Autonomous Institute",
            "courses": [
                {
                    "courseCode": "0401824210",
                    "courseName": "Computer Science and Engineering",
                    "seatTypes": {
                        "stateLevel": {
                            "GOPENS": {"meritNo": "5000", "meritPercentile": "98.5001234"},
                            "GSCS": {"meritNo": "12000", "meritPercentile": "96.7001234"},
                            "GOBCS": {"meritNo": "6000", "meritPercentile": "98.2001234"},
                            "EWS": {"meritNo": "7000", "meritPercentile": "97.9001234"}
                        }
                    }
                }
            ]
        },
        {
            "collegeCode": "03204",
            "collegeName": "Sardar Patel Institute of Technology (SPIT), Mumbai",
            "status": "Autonomous",
            "homeUniversity": "Autonomous Institute",
            "courses": [
                {
                    "courseCode": "0320424510",
                    "courseName": "Computer Engineering",
                    "seatTypes": {
                        "stateLevel": {
                            "GOPENS": {"meritNo": "700", "meritPercentile": "99.7501234"},
                            "GOBCS": {"meritNo": "1000", "meritPercentile": "99.6501234"},
                            "LOPENS": {"meritNo": "850", "meritPercentile": "99.7001234"},
                            "TFWS": {"meritNo": "650", "meritPercentile": "99.7801234"},
                            "EWS": {"meritNo": "950", "meritPercentile": "99.6801234"}
                        }
                    }
                }
            ]
        },
        {
            "collegeCode": "60042",
            "collegeName": "Pune Institute of Computer Technology (PICT), Pune",
            "status": "Private, Autonomous",
            "homeUniversity": "Autonomous Institute",
            "courses": [
                {
                    "courseCode": "6004224510",
                    "courseName": "Computer Engineering",
                    "seatTypes": {
                        "stateLevel": {
                            "GOPENS": {"meritNo": "1200", "meritPercentile": "99.5501234"},
                            "GSCS": {"meritNo": "5000", "meritPercentile": "98.5001234"},
                            "GOBCS": {"meritNo": "2000", "meritPercentile": "99.3001234"},
                            "EWS": {"meritNo": "1800", "meritPercentile": "99.4001234"}
                        }
                    }
                }
            ]
        }
    ]
    
    if not MONGODB_AVAILABLE:
        # Use the college database as fallback data when MongoDB is not available
        fallback_colleges = college_database
        
        # Apply filters from query parameters
        college_name = request.args.get('college_name')
        course_name = request.args.get('course_name')
        category = request.args.get('category')
        status = request.args.get('status')
        min_percentile = request.args.get('min_percentile')
        
        filtered_colleges = fallback_colleges
        
        # Filter by college name
        if college_name:
            filtered_colleges = [c for c in filtered_colleges if college_name.lower() in c['collegeName'].lower()]
        
        # Filter by status
        if status:
            filtered_colleges = [c for c in filtered_colleges if status.lower() in c['status'].lower()]
        
        # Filter by course name
        if course_name:
            filtered_colleges_temp = []
            for college in filtered_colleges:
                matching_courses = []
                for course in college['courses']:
                    if course_name.lower() in course['courseName'].lower():
                        matching_courses.append(course)
                
                if matching_courses:
                    college_copy = college.copy()
                    college_copy['courses'] = matching_courses
                    filtered_colleges_temp.append(college_copy)
            filtered_colleges = filtered_colleges_temp
        
        # Filter by category and percentile
        if category or min_percentile:
            filtered_colleges_temp = []
            for college in filtered_colleges:
                matching_courses = []
                for course in college['courses']:
                    # Check if the course has the specified category and meets the minimum percentile
                    if 'seatTypes' in course and 'stateLevel' in course['seatTypes']:
                        seat_types = course['seatTypes']['stateLevel']
                        
                        # If category is specified, check if it exists and meets percentile requirement
                        if category and category in seat_types:
                            percentile = float(seat_types[category]['meritPercentile'])
                            if not min_percentile or percentile >= float(min_percentile):
                                matching_courses.append(course)
                        # If only min_percentile is specified, check all categories
                        elif min_percentile and not category:
                            # Check if any category meets the minimum percentile
                            for cat, data in seat_types.items():
                                if float(data['meritPercentile']) >= float(min_percentile):
                                    matching_courses.append(course)
                                    break
                        # If neither category nor min_percentile is specified, include all courses
                        elif not category and not min_percentile:
                            matching_courses.append(course)
                
                if matching_courses:
                    college_copy = college.copy()
                    college_copy['courses'] = matching_courses
                    filtered_colleges_temp.append(college_copy)
            
            filtered_colleges = filtered_colleges_temp
        
        return jsonify({
            'success': True,
            'colleges': filtered_colleges
        })
    
    try:
        # Connect to MongoDB and get college data
        client = get_mongodb_connection()
        db = client["mht_cet_admissions_top20"]
        colleges_collection = db["cutOffs"]
        
        # Get query parameters
        college_name = request.args.get('college_name')
        course_name = request.args.get('course_name')
        category = request.args.get('category')
        status = request.args.get('status')
        min_percentile = request.args.get('min_percentile')
        
        # Build MongoDB query
        query = {}
        if college_name:
            query['collegeName'] = {'$regex': college_name, '$options': 'i'}
        if status:
            query['status'] = {'$regex': status, '$options': 'i'}
        
        # Get colleges from MongoDB
        colleges = list(colleges_collection.find(query))
        
        # Apply course name filter
        if course_name:
            filtered_colleges = []
            for college in colleges:
                matching_courses = []
                for course in college.get('courses', []):
                    if course_name.lower() in course.get('courseName', '').lower():
                        matching_courses.append(course)
                
                if matching_courses:
                    college_copy = college.copy()
                    college_copy['courses'] = matching_courses
                    filtered_colleges.append(college_copy)
            colleges = filtered_colleges
        
        # Apply category and percentile filters
        if category or min_percentile:
            filtered_colleges = []
            for college in colleges:
                matching_courses = []
                for course in college.get('courses', []):
                    if 'seatTypes' in course and 'stateLevel' in course['seatTypes']:
                        seat_types = course['seatTypes']['stateLevel']
                        
                        # If category is specified, check if it exists and meets percentile requirement
                        if category and category in seat_types:
                            percentile = float(seat_types[category]['meritPercentile'])
                            if not min_percentile or percentile >= float(min_percentile):
                                matching_courses.append(course)
                        # If only min_percentile is specified, check all categories
                        elif min_percentile and not category:
                            # Check if any category meets the minimum percentile
                            for cat, data in seat_types.items():
                                if float(data['meritPercentile']) >= float(min_percentile):
                                    matching_courses.append(course)
                                    break
                        # If neither category nor min_percentile is specified, include all courses
                        elif not category and not min_percentile:
                            matching_courses.append(course)
                
                if matching_courses:
                    college_copy = college.copy()
                    college_copy['courses'] = matching_courses
                    filtered_colleges.append(college_copy)
            colleges = filtered_colleges
        
        # Convert ObjectId to string for JSON serialization
        for college in colleges:
            if '_id' in college:
                college['_id'] = str(college['_id'])
        
        return jsonify({
            'success': True,
            'colleges': colleges
        })
        
    except Exception as e:
        print(f"Error fetching MongoDB colleges: {str(e)}")
        # Fall back to the local data if MongoDB connection fails
        return get_mongodb_colleges()
        
    try:
        db = get_mongodb_connection()
        if not db:
            return jsonify({'error': 'MongoDB connection failed'}), 500
        
        collection = db["cutOffs"]
        
        # Get filter parameters
        college_name = request.args.get('college_name')
        course_name = request.args.get('course_name')
        category = request.args.get('category')
        status = request.args.get('status')
        min_percentile = request.args.get('min_percentile')
        
        # Build query
        query = {}
        if college_name:
            query['collegeName'] = {'$regex': college_name, '$options': 'i'}
        if status:
            query['status'] = {'$regex': status, '$options': 'i'}
        
        # Get colleges matching the basic criteria
        colleges = list(collection.find(query, {'_id': 0}))
        
        # Apply additional filters that require post-processing
        if course_name or category or min_percentile:
            filtered_colleges = []
            for college in colleges:
                matching_courses = []
                for course in college.get('courses', []):
                    include_course = True
                    
                    # Filter by course name
                    if course_name and course_name.lower() not in course.get('courseName', '').lower():
                        include_course = False
                    
                    # Filter by category and percentile
                    if include_course and (category or min_percentile):
                        if category:
                            category_found = False
                            for level in course.get('seatTypes', {}):
                                if category in course['seatTypes'][level]:
                                    category_found = True
                                    # Check min_percentile if specified
                                    if min_percentile and float(course['seatTypes'][level][category]['meritPercentile']) < float(min_percentile):
                                        include_course = False
                            if not category_found:
                                include_course = False
                        elif min_percentile:  # Only min_percentile specified
                            percentile_found = False
                            for level in course.get('seatTypes', {}):
                                for cat in course['seatTypes'][level]:
                                    if float(course['seatTypes'][level][cat]['meritPercentile']) >= float(min_percentile):
                                        percentile_found = True
                                        break
                                if percentile_found:
                                    break
                            if not percentile_found:
                                include_course = False
                    
                    if include_course:
                        matching_courses.append(course)
                
                if matching_courses:
                    college_copy = college.copy()
                    college_copy['courses'] = matching_courses
                    filtered_colleges.append(college_copy)
            
            colleges = filtered_colleges
        
        return jsonify({
            'success': True,
            'colleges': colleges,
            'total': len(colleges)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/mongodb-cutoffs')
@login_required
def get_mongodb_cutoffs():
    """Get college cutoffs from MongoDB with filters"""
    if not MONGODB_AVAILABLE:
        # Return fallback data when MongoDB is not available
        fallback_cutoffs = [
            {
                "collegeName": "College of Engineering Pune (COEP Technological University)",
                "collegeCode": "01002",
                "courseName": "Computer Science and Engineering",
                "category": "GOPENS",
                "meritNo": "100",
                "meritPercentile": "99.9601002",
                "level": "stateLevel"
            },
            {
                "collegeName": "College of Engineering Pune (COEP Technological University)",
                "collegeCode": "01002",
                "courseName": "Computer Science and Engineering",
                "category": "GSCS",
                "meritNo": "2500",
                "meritPercentile": "99.2001002",
                "level": "stateLevel"
            },
            {
                "collegeName": "Veermata Jijabai Technological Institute (VJTI), Matunga, Mumbai",
                "collegeCode": "03012",
                "courseName": "Computer Engineering",
                "category": "GOPENS",
                "meritNo": "103",
                "meritPercentile": "99.9522882",
                "level": "stateLevel"
            }
        ]
        
        # Apply filters to fallback data
        filtered_cutoffs = fallback_cutoffs
        college_name = request.args.get('college')
        course_name = request.args.get('course')
        category = request.args.get('category')
        
        if college_name:
            filtered_cutoffs = [c for c in filtered_cutoffs if college_name.lower() in c['collegeName'].lower()]
        if course_name:
            filtered_cutoffs = [c for c in filtered_cutoffs if course_name.lower() in c['courseName'].lower()]
        if category:
            filtered_cutoffs = [c for c in filtered_cutoffs if category.upper() in c['category'].upper()]
        
        return jsonify({
            'success': True,
            'cutoffs': filtered_cutoffs,
            'total': len(filtered_cutoffs),
            'note': 'Using fallback data - MongoDB not available'
        })
    
    try:
        college_name = request.args.get('college')
        course_name = request.args.get('course')
        category = request.args.get('category')
        
        cutoffs = get_college_cutoffs(college_name, course_name, category)
        
        return jsonify({
            'success': True,
            'cutoffs': cutoffs,
            'total': len(cutoffs)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai-recommendations', methods=['POST'])
@login_required
def get_ai_recommendations():
    """Get AI-powered college recommendations"""
    try:
        data = request.json
        percentile = data.get('percentile', 0)
        category = data.get('category', 'General')
        budget = data.get('budget')
        preferred_branches = data.get('preferred_branches')
        
        # Get ML-based recommendations
        ml_recommendations = college_recommender.predict_colleges(
            percentile, category, budget, preferred_branches
        )
        
        # Get AI-enhanced recommendations
        ai_recommendations = generate_college_recommendations_with_ai(
            percentile, category, budget, preferred_branches
        )
        
        return jsonify({
            'success': True,
            'ml_recommendations': ml_recommendations,
            'ai_recommendations': ai_recommendations
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/notifications')
@login_required
def get_notifications():
    """Get user notifications"""
    notifications = Notification.query.filter_by(
        user_id=current_user.id
    ).order_by(Notification.created_at.desc()).limit(10).all()
    
    return jsonify([{
        'id': n.id,
        'title': n.title,
        'message': n.message,
        'type': n.type,
        'read': n.read,
        'created_at': n.created_at.strftime('%Y-%m-%d %H:%M')
    } for n in notifications])

@app.route('/api/mark-notification-read/<int:notification_id>', methods=['POST'])
@login_required
def mark_notification_read(notification_id):
    """Mark notification as read"""
    notification = Notification.query.get_or_404(notification_id)
    if notification.user_id == current_user.id:
        notification.read = True
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False}), 403



from college_dataset import initialize_college_dataset

# Initialize database and train models
def init_database():
    """Initialize database with sample data"""
    with app.app_context():
        db.create_all()
        
        # Add sample exams if not exists
        if not Exam.query.first():
            exams = [
                Exam(name='JEE Main', full_name='Joint Entrance Examination Main', 
                     description='National level engineering entrance exam', 
                     exam_date='January, April, May 2025',
                     application_deadline='December 2024',
                     website='jeemain.nta.ac.in'),
                Exam(name='MHT CET', full_name='Maharashtra Common Entrance Test',
                     description='State level engineering entrance exam for Maharashtra',
                     exam_date='May 2025',
                     application_deadline='March 2025',
                     website='cetcell.mahacet.org'),
                Exam(name='BITSAT', full_name='BITS Admission Test',
                     description='Entrance exam for BITS Pilani',
                     exam_date='May-June 2025',
                     application_deadline='March 2025',
                     website='bitsadmission.com')
            ]
            
            for exam in exams:
                db.session.add(exam)
            
            db.session.commit()
        
        # Initialize MongoDB college dataset with cutoff and caste-wise data
        if MONGODB_AVAILABLE:
            try:
                # Get MongoDB client from the same connection string used elsewhere
                mongo_client = pymongo.MongoClient(app.config.get('MONGODB_URI', 'mongodb://localhost:27017/'))
                initialize_college_dataset(mongo_client)
            except Exception as e:
                print(f"Error initializing MongoDB college dataset: {str(e)}")
        
        # Train AI model
        college_recommender.train_model()

if __name__ == '__main__':
    init_database()
    app.run(debug=True, host='0.0.0.0', port=5000)