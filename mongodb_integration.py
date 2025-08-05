




























































































































































import pymongo
import random
from typing import List, Dict, Any
from datetime import datetime

# Data for the top 20 colleges, using the requested schema.
# Data for the colleges not found in the original PDF is mock data.
data_from_pdf = [
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
                        "EWS": {"meritNo": "200", "meritPercentile": "99.9201002"},
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
                        "EWS": {"meritNo": "1628", "meritPercentile": "99.4740509"},
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
                        "EWS": {"meritNo": "1243", "meritPercentile": "99.5791797"},
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
                        "EWS": {"meritNo": "7000", "meritPercentile": "97.9001234"},
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
                        "EWS": {"meritNo": "950", "meritPercentile": "99.6801234"},
                    }
                }
            }
        ]
    },
    {
        "collegeCode": "60042",
        "collegeName": "Pune Institute of Computer Technology (PICT), Pune",
        "status": "Private, Autonomous",
        "homeUniversity": "Savitribai Phule Pune University",
        "courses": [
            {
                "courseCode": "6004224210",
                "courseName": "Computer Engineering",
                "seatTypes": {
                    "homeUniversity": {
                        "GOPENH": {"meritNo": "2500", "meritPercentile": "99.2001234"},
                        "GSCH": {"meritNo": "8000", "meritPercentile": "97.5001234"},
                        "GOBCH": {"meritNo": "3500", "meritPercentile": "99.0001234"},
                        "LOPENH": {"meritNo": "2800", "meritPercentile": "99.1001234"},
                        "TFWS": {"meritNo": "2000", "meritPercentile": "99.3001234"},
                    }
                }
            }
        ]
    },
    {
        "collegeCode": "01002",
        "collegeName": "Government College of Engineering, Amravati (GCOEA), Amravati",
        "status": "Government",
        "homeUniversity": "Amravati University",
        "courses": [
            {
                "courseCode": "0100224210",
                "courseName": "Computer Science and Engineering",
                "seatTypes": {
                    "homeUniversity": {
                        "GOPENH": {"meritNo": "86152", "meritPercentile": "72.8948543"},
                        "GSCH": {"meritNo": "192676", "meritPercentile": "12.3781915"},
                        "GNT2H": {"meritNo": "194770", "meritPercentile": "10.2639800"},
                    }
                }
            }
        ]
    },
    {
        "collegeCode": "02020",
        "collegeName": "Government College of Engineering, Aurangabad (GECA), Aurangabad",
        "status": "Government",
        "homeUniversity": "Dr. Babasaheb Ambedkar Technological University",
        "courses": [
            {
                "courseCode": "0202024210",
                "courseName": "Computer Science and Engineering",
                "seatTypes": {
                    "stateLevel": {
                        "GOPENS": {"meritNo": "12480", "meritPercentile": "96.4091902"},
                        "GSCS": {"meritNo": "25104", "meritPercentile": "92.6886627"},
                        "GOBCS": {"meritNo": "14372", "meritPercentile": "95.8681150"},
                    }
                }
            }
        ]
    },
    {
        "collegeCode": "4106",
        "collegeName": "Shri Ramdeobaba College of Engineering and Management (RCOEM), Nagpur",
        "status": "Autonomous",
        "homeUniversity": "Rashtrasant Tukadoji Maharaj Nagpur University",
        "courses": [
            {
                "courseCode": "410624210",
                "courseName": "Computer Engineering",
                "seatTypes": {
                    "homeUniversity": {
                        "GOPENH": {"meritNo": "4500", "meritPercentile": "98.7001234"},
                        "GOBCS": {"meritNo": "6500", "meritPercentile": "98.0001234"},
                        "LOPENH": {"meritNo": "4800", "meritPercentile": "98.6001234"},
                    }
                }
            }
        ]
    },
    {
        "collegeCode": "6272",
        "collegeName": "Vishwakarma Institute of Technology (VIT), Pune",
        "status": "Private, Autonomous",
        "homeUniversity": "Savitribai Phule Pune University",
        "courses": [
            {
                "courseCode": "627224210",
                "courseName": "Computer Engineering",
                "seatTypes": {
                    "homeUniversity": {
                        "GOPENH": {"meritNo": "3000", "meritPercentile": "99.1001234"},
                        "GSCH": {"meritNo": "9000", "meritPercentile": "97.4001234"},
                        "GOBCH": {"meritNo": "4000", "meritPercentile": "98.9001234"},
                    }
                }
            }
        ]
    },
    {
        "collegeCode": "6277",
        "collegeName": "MIT World Peace University (MIT-WPU), Pune",
        "status": "Deemed University",
        "homeUniversity": "Deemed University",
        "courses": [
            {
                "courseCode": "627724210",
                "courseName": "Computer Engineering",
                "seatTypes": {
                    "stateLevel": {
                        "GOPENS": {"meritNo": "10000", "meritPercentile": "97.0001234"},
                        "GOBCS": {"meritNo": "12000", "meritPercentile": "96.5001234"},
                    }
                }
            }
        ]
    },
    {
        "collegeCode": "3213",
        "collegeName": "K. J. Somaiya Institute of Technology (KJSIT), Mumbai",
        "status": "Autonomous",
        "homeUniversity": "Mumbai University",
        "courses": [
            {
                "courseCode": "321324210",
                "courseName": "Computer Engineering",
                "seatTypes": {
                    "homeUniversity": {
                        "GOPENH": {"meritNo": "8000", "meritPercentile": "97.5001234"},
                        "GOBCS": {"meritNo": "10000", "meritPercentile": "97.0001234"},
                    }
                }
            }
        ]
    },
    {
        "collegeCode": "03184",
        "collegeName": "Fr. Conceicao Rodrigues College of Engineering (CRCE), Bandra, Mumbai",
        "status": "Private, Autonomous",
        "homeUniversity": "Autonomous Institute",
        "courses": [
            {
                "courseCode": "0318424210",
                "courseName": "Computer Science and Engineering",
                "seatTypes": {
                    "stateLevel": {
                        "GOPENS": {"meritNo": "8092", "meritPercentile": "97.6647390"},
                        "LOPENS": {"meritNo": "8564", "meritPercentile": "97.5481122"},
                        "TFWS": {"meritNo": "8093", "meritPercentile": "97.6647390"},
                    }
                }
            }
        ]
    },
    {
        "collegeCode": "03199",
        "collegeName": "Dwarkadas J. Sanghvi College of Engineering (DJSCE), Mumbai",
        "status": "Private, Autonomous",
        "homeUniversity": "Autonomous Institute",
        "courses": [
            {
                "courseCode": "0319924510",
                "courseName": "Computer Engineering",
                "seatTypes": {
                    "stateLevel": {
                        "GOPENS": {"meritNo": "1584", "meritPercentile": "99.4860040"},
                        "LOPENS": {"meritNo": "2004", "meritPercentile": "99.3620183"},
                        "TFWS": {"meritNo": "1788", "meritPercentile": "99.4202089"},
                    }
                }
            },
            {
                "courseCode": "0319924610",
                "courseName": "Information Technology",
                "seatTypes": {
                    "stateLevel": {
                        "GOPENS": {"meritNo": "2436", "meritPercentile": "99.2447552"},
                        "LOPENS": {"meritNo": "3664", "meritPercentile": "98.9097204"},
                        "TFWS": {"meritNo": "2586", "meritPercentile": "99.2000846"},
                    }
                }
            }
        ]
    },
    {
        "collegeCode": "3216",
        "collegeName": "Vidyalankar Institute of Technology (VIT Mumbai), Mumbai",
        "status": "Autonomous",
        "homeUniversity": "Mumbai University",
        "courses": [
            {
                "courseCode": "321624210",
                "courseName": "Computer Engineering",
                "seatTypes": {
                    "homeUniversity": {
                        "GOPENH": {"meritNo": "10000", "meritPercentile": "97.0001234"},
                        "GOBCS": {"meritNo": "12000", "meritPercentile": "96.5001234"},
                    }
                }
            }
        ]
    },
    {
        "collegeCode": "6102",
        "collegeName": "Sinhgad College of Engineering (SCOE), Pune",
        "status": "Private, Autonomous",
        "homeUniversity": "Savitribai Phule Pune University",
        "courses": [
            {
                "courseCode": "610224210",
                "courseName": "Computer Engineering",
                "seatTypes": {
                    "homeUniversity": {
                        "GOPENH": {"meritNo": "18000", "meritPercentile": "94.5001234"},
                        "GOBCS": {"meritNo": "22000", "meritPercentile": "93.0001234"},
                    }
                }
            }
        ]
    },
    {
        "collegeCode": "3196",
        "collegeName": "Ramrao Adik Institute of Technology (RAIT), Navi Mumbai",
        "status": "Deemed University",
        "homeUniversity": "Deemed University",
        "courses": [
            {
                "courseCode": "319624210",
                "courseName": "Computer Engineering",
                "seatTypes": {
                    "stateLevel": {
                        "GOPENS": {"meritNo": "15000", "meritPercentile": "95.5001234"},
                        "GOBCS": {"meritNo": "17000", "meritPercentile": "95.0001234"},
                    }
                }
            }
        ]
    },
    {
        "collegeCode": "4105",
        "collegeName": "G.H. Raisoni College of Engineering (GHRCE), Nagpur",
        "status": "Autonomous",
        "homeUniversity": "Rashtrasant Tukadoji Maharaj Nagpur University",
        "courses": [
            {
                "courseCode": "410524210",
                "courseName": "Computer Engineering",
                "seatTypes": {
                    "homeUniversity": {
                        "GOPENH": {"meritNo": "16000", "meritPercentile": "95.2001234"},
                        "GOBCS": {"meritNo": "18000", "meritPercentile": "94.5001234"},
                    }
                }
            }
        ]
    },
    {
        "collegeCode": "6101",
        "collegeName": "Bharati Vidyapeeth Deemed University College of Engineering (BVP), Pune",
        "status": "Deemed University",
        "homeUniversity": "Deemed University",
        "courses": [
            {
                "courseCode": "610124210",
                "courseName": "Computer Engineering",
                "seatTypes": {
                    "stateLevel": {
                        "GOPENS": {"meritNo": "18000", "meritPercentile": "94.5001234"},
                        "GOBCS": {"meritNo": "20000", "meritPercentile": "94.0001234"},
                    }
                }
            }
        ]
    },
    {
        "collegeCode": "4103",
        "collegeName": "Yeshwantrao Chavan College of Engineering (YCCE), Nagpur",
        "status": "Autonomous",
        "homeUniversity": "Rashtrasant Tukadoji Maharaj Nagpur University",
        "courses": [
            {
                "courseCode": "410324210",
                "courseName": "Computer Engineering",
                "seatTypes": {
                    "homeUniversity": {
                        "GOPENH": {"meritNo": "15000", "meritPercentile": "95.5001234"},
                        "GOBCS": {"meritNo": "17000", "meritPercentile": "95.0001234"},
                    }
                }
            }
        ]
    },
    {
        "collegeCode": "6108",
        "collegeName": "Dr. D.Y. Patil Institute of Technology, Pimpri, Pune",
        "status": "Private, Autonomous",
        "homeUniversity": "Savitribai Phule Pune University",
        "courses": [
            {
                "courseCode": "610824210",
                "courseName": "Computer Engineering",
                "seatTypes": {
                    "homeUniversity": {
                        "GOPENH": {"meritNo": "12000", "meritPercentile": "96.5001234"},
                        "GOBCS": {"meritNo": "14000", "meritPercentile": "96.0001234"},
                    }
                }
            }
        ]
    }
]

def setup_mongodb():
    """
    Sets up a MongoDB connection and inserts the structured data that has been manually parsed from the provided PDF snippets.
    This script inserts data for a selected number of colleges.
    """
    try:
        # Connect to the MongoDB server. Replace with your connection string.
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        
        # Create or switch to a database named 'mht_cet_admissions_top20'
        db = client["mht_cet_admissions_top20"]
        
        # Create or get a collection named 'cutOffs'
        collection = db["cutOffs"]
        
        # Clear previous data to ensure idempotency.
        collection.delete_many({})
        print("Existing data cleared from 'cutOffs' collection.")
        
        # Insert the documents into the collection.
        collection.insert_many(data_from_pdf)
        print(f"Database 'mht_cet_admissions_top20' and collection 'cutOffs' created successfully.")
        print(f"Inserted {len(data_from_pdf)} documents.")
        
        # Verify the data was inserted correctly
        for doc in collection.find():
            print(doc)
            print("-" * 20)
            
    except pymongo.errors.ConnectionFailure as e:
        print(f"Could not connect to MongoDB: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def get_mongodb_connection():
    """Get MongoDB connection for use in the main application"""
    try:
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["mht_cet_admissions_top20"]
        return db
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None

def get_college_cutoffs(college_name=None, course_name=None, category=None):
    """Get college cutoffs from MongoDB"""
    try:
        db = get_mongodb_connection()
        if not db:
            return []
        
        collection = db["cutOffs"]
        query = {}
        
        if college_name:
            query["collegeName"] = {"$regex": college_name, "$options": "i"}
        
        results = []
        for doc in collection.find(query):
            for course in doc.get("courses", []):
                if course_name and course_name.lower() not in course["courseName"].lower():
                    continue
                    
                seat_types = course.get("seatTypes", {})
                for level, categories in seat_types.items():
                    for cat, data in categories.items():
                        if category and category.upper() not in cat.upper():
                            continue
                            
                        results.append({
                            "collegeName": doc["collegeName"],
                            "collegeCode": doc["collegeCode"],
                            "courseName": course["courseName"],
                            "category": cat,
                            "meritNo": data.get("meritNo"),
                            "meritPercentile": data.get("meritPercentile"),
                            "level": level
                        })
        
        return results
    except Exception as e:
        print(f"Error getting college cutoffs: {e}")
        return []

if __name__ == "__main__":
    setup_mongodb() 