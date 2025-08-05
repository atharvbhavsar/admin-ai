import requests
import json

def test_chatbot():
    """Test the chatbot functionality"""
    
    # Test data
    test_message = "What are the cutoffs for COEP Computer Science?"
    
    # Simulate a POST request to the chatbot endpoint
    url = "http://localhost:5000/chatbot"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'message': test_message
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("Chatbot Response:")
            print(result.get('response', 'No response'))
        else:
            print(f"Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Make sure the Flask app is running.")
    except Exception as e:
        print(f"Error: {e}")

def test_mongodb_colleges():
    """Test the MongoDB colleges endpoint"""
    
    url = "http://localhost:5000/api/mongodb-colleges"
    
    try:
        response = requests.get(url)
        print(f"\nMongoDB Colleges Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("MongoDB Colleges Response:")
            print(f"Success: {result.get('success')}")
            print(f"Total Colleges: {result.get('total')}")
            if 'note' in result:
                print(f"Note: {result.get('note')}")
        else:
            print(f"Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Make sure the Flask app is running.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Testing AdmitAI Chatbot and MongoDB Integration...")
    print("=" * 50)
    
    test_chatbot()
    test_mongodb_colleges()
    
    print("\n" + "=" * 50)
    print("Test completed!") 