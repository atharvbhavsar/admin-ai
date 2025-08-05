import pymongo
import random
import os
from datetime import datetime

# Function to initialize MongoDB with college dataset
def initialize_college_dataset(mongo_client):
    try:
        # Get database and collections
        db = mongo_client["admitai"]
        colleges_collection = db["colleges"]
        
        # Check if collection already has data
        if colleges_collection.count_documents({}) > 0:
            print("College dataset already exists. Skipping initialization.")
            return True
        
        # Generate and insert college data with cutoffs, caste-wise data, placements, etc.
        colleges_data = generate_college_data()
        
        # Insert the data
        colleges_collection.insert_many(colleges_data)
        
        print(f"Successfully added {len(colleges_data)} colleges to the database.")
        return True
    except Exception as e:
        print(f"Error in initialize_college_dataset: {str(e)}")
        return False

def generate_college_data():
    """
    Generate comprehensive data for 30 colleges including cutoffs, caste-wise data,
    placements, and other information.
    """
    return [
        {
            "_id": "1",
            "college_name": "College of Engineering Pune (COEP Technological University)",
            "collegeCode": "01002",
            "location": "Pune, Maharashtra",
            "established": 1854,
            "type": "Government Autonomous",
            "accreditation": "NAAC 'A+'",
            "website": "www.coep.org.in",
            "nirf_rank": 43,
            "facilities": ["Library", "Sports Complex", "Hostels", "Cafeteria", "Research Labs", "Auditorium"],
            "placement": {
                "highest_package": 44.14,  # LPA
                "average_package": 12.5,   # LPA
                "placement_percentage": 92,
                "top_recruiters": ["Microsoft", "Google", "Amazon", "Goldman Sachs", "Morgan Stanley"]
            },
            "type": "Public Technical University",
            "accreditation": "NAAC A++",
            "website": "www.iitb.ac.in",
            "nirf_rank": 3,
            "facilities": ["Library", "Sports Complex", "Hostels", "Research Labs", "Cafeteria"],
            "placement": {
                "highest_package": "1.5 Crore",
                "average_package": "25 LPA",
                "placement_percentage": 98,
                "top_recruiters": ["Google", "Microsoft", "Amazon", "Facebook", "Goldman Sachs"]
            },
            "contact": {
                "email": "registrar@iitb.ac.in",
                "phone": "+91-22-25722545",
                "address": "IIT Bombay, Powai, Mumbai, Maharashtra 400076"
            },
            "status": "active"
        },
        {
            "_id": "2",
            "college_name": "College of Engineering, Pune",
            "location": "Pune, Maharashtra",
            "established": 1854,
            "type": "Government Autonomous Institute",
            "accreditation": "NAAC A+",
            "website": "www.coep.org.in",
            "nirf_rank": 45,
            "facilities": ["Library", "Sports Complex", "Hostels", "Research Labs", "Cafeteria"],
            "placement": {
                "highest_package": "54 LPA",
                "average_package": "12 LPA",
                "placement_percentage": 92,
                "top_recruiters": ["TCS", "Infosys", "Wipro", "Microsoft", "Amazon"]
            },
            "contact": {
                "email": "director@coep.ac.in",
                "phone": "+91-20-25507000",
                "address": "Wellesley Rd, Shivajinagar, Pune, Maharashtra 411005"
            },
            "status": "active"
        },
        {
            "_id": "3",
            "college_name": "Veermata Jijabai Technological Institute",
            "location": "Mumbai, Maharashtra",
            "established": 1887,
            "type": "Government Aided Autonomous Institute",
            "accreditation": "NAAC A+",
            "website": "www.vjti.ac.in",
            "nirf_rank": 65,
            "facilities": ["Library", "Sports Complex", "Hostels", "Research Labs", "Cafeteria"],
            "placement": {
                "highest_package": "45 LPA",
                "average_package": "10.5 LPA",
                "placement_percentage": 90,
                "top_recruiters": ["TCS", "Infosys", "Wipro", "Microsoft", "Amazon"]
            },
            "contact": {
                "email": "director@vjti.ac.in",
                "phone": "+91-22-24198101",
                "address": "H R Mahajani Marg, Matunga, Mumbai, Maharashtra 400019"
            },
            "status": "active"
        },
        {
            "_id": "4",
            "college_name": "Sardar Patel Institute of Technology",
            "location": "Mumbai, Maharashtra",
            "established": 1995,
            "type": "Private Autonomous Institute",
            "accreditation": "NAAC A+",
            "website": "www.spit.ac.in",
            "nirf_rank": 101,
            "facilities": ["Library", "Sports Complex", "Hostels", "Research Labs", "Cafeteria"],
            "placement": {
                "highest_package": "42 LPA",
                "average_package": "11 LPA",
                "placement_percentage": 95,
                "top_recruiters": ["TCS", "Infosys", "Wipro", "Microsoft", "Amazon"]
            },
            "contact": {
                "email": "principal@spit.ac.in",
                "phone": "+91-22-26707440",
                "address": "Bhavans Campus, Munshi Nagar, Andheri West, Mumbai, Maharashtra 400058"
            },
            "status": "active"
        },
        {
            "_id": "5",
            "college_name": "Pune Institute of Computer Technology",
            "location": "Pune, Maharashtra",
            "established": 1983,
            "type": "Private Autonomous Institute",
            "accreditation": "NAAC A+",
            "website": "www.pict.edu",
            "nirf_rank": 120,
            "facilities": ["Library", "Sports Complex", "Hostels", "Research Labs", "Cafeteria"],
            "placement": {
                "highest_package": "40 LPA",
                "average_package": "9.5 LPA",
                "placement_percentage": 92,
                "top_recruiters": ["TCS", "Infosys", "Wipro", "Microsoft", "Amazon"]
            },
            "contact": {
                "email": "principal@pict.edu",
                "phone": "+91-20-24371101",
                "address": "Survey No. 27, Near Bharati Vidyapeeth, Dhankawadi, Pune, Maharashtra 411043"
            },
            "status": "active"
        },
        {
            "_id": "6",
            "college_name": "Walchand College of Engineering",
            "location": "Sangli, Maharashtra",
            "established": 1947,
            "type": "Government Aided Autonomous Institute",
            "accreditation": "NAAC A",
            "website": "www.walchandsangli.ac.in",
            "nirf_rank": 150,
            "facilities": ["Library", "Sports Complex", "Hostels", "Research Labs", "Cafeteria"],
            "placement": {
                "highest_package": "30 LPA",
                "average_package": "7.5 LPA",
                "placement_percentage": 85,
                "top_recruiters": ["TCS", "Infosys", "Wipro", "L&T", "Cognizant"]
            },
            "contact": {
                "email": "director@walchandsangli.ac.in",
                "phone": "+91-233-2300383",
                "address": "Vishrambag, Sangli, Maharashtra 416415"
            },
            "status": "active"
        },
        {
            "_id": "7",
            "college_name": "Government College of Engineering, Amravati",
            "location": "Amravati, Maharashtra",
            "established": 1964,
            "type": "Government Institute",
            "accreditation": "NAAC A",
            "website": "www.gcoea.ac.in",
            "nirf_rank": 180,
            "facilities": ["Library", "Sports Complex", "Hostels", "Research Labs", "Cafeteria"],
            "placement": {
                "highest_package": "18 LPA",
                "average_package": "6 LPA",
                "placement_percentage": 80,
                "top_recruiters": ["TCS", "Infosys", "Wipro", "L&T", "Cognizant"]
            },
            "contact": {
                "email": "principal@gcoea.ac.in",
                "phone": "+91-721-2660360",
                "address": "Kathora Naka, Amravati, Maharashtra 444604"
            },
            "status": "active"
        },
        {
            "_id": "8",
            "college_name": "Vishwakarma Institute of Technology",
            "location": "Pune, Maharashtra",
            "established": 1983,
            "type": "Private Autonomous Institute",
            "accreditation": "NAAC A+",
            "website": "www.vit.edu",
            "nirf_rank": 130,
            "facilities": ["Library", "Sports Complex", "Hostels", "Research Labs", "Cafeteria"],
            "placement": {
                "highest_package": "35 LPA",
                "average_package": "8.5 LPA",
                "placement_percentage": 90,
                "top_recruiters": ["TCS", "Infosys", "Wipro", "Microsoft", "Amazon"]
            },
            "contact": {
                "email": "director@vit.edu",
                "phone": "+91-20-24202180",
                "address": "666, Upper Indiranagar, Bibwewadi, Pune, Maharashtra 411037"
            },
            "status": "active"
        },
        {
            "_id": "9",
            "college_name": "K. J. Somaiya College of Engineering",
            "location": "Mumbai, Maharashtra",
            "established": 1983,
            "type": "Private Autonomous Institute",
            "accreditation": "NAAC A+",
            "website": "www.kjsce.somaiya.edu",
            "nirf_rank": 140,
            "facilities": ["Library", "Sports Complex", "Hostels", "Research Labs", "Cafeteria"],
            "placement": {
                "highest_package": "38 LPA",
                "average_package": "9 LPA",
                "placement_percentage": 92,
                "top_recruiters": ["TCS", "Infosys", "Wipro", "Microsoft", "Amazon"]
            },
            "contact": {
                "email": "principal.kjsce@somaiya.edu",
                "phone": "+91-22-66449191",
                "address": "Vidyavihar, Mumbai, Maharashtra 400077"
            },
            "status": "active"
        },
        {
            "_id": "10",
            "college_name": "Maharashtra Institute of Technology",
            "location": "Pune, Maharashtra",
            "established": 1983,
            "type": "Private Institute",
            "accreditation": "NAAC A",
            "website": "www.mitpune.com",
            "nirf_rank": 160,
            "facilities": ["Library", "Sports Complex", "Hostels", "Research Labs", "Cafeteria"],
            "placement": {
                "highest_package": "28 LPA",
                "average_package": "7 LPA",
                "placement_percentage": 85,
                "top_recruiters": ["TCS", "Infosys", "Wipro", "L&T", "Cognizant"]
            },
            "contact": {
                "email": "director@mitpune.edu.in",
                "phone": "+91-20-30273400",
                "address": "S.No.124, Paud Road, Kothrud, Pune, Maharashtra 411038"
            },
            "status": "active"
        },
        {
            "_id": "11",
            "college_name": "Bharati Vidyapeeth College of Engineering",
            "location": "Pune, Maharashtra",
            "established": 1983,
            "type": "Private Institute",
            "accreditation": "NAAC A",
            "website": "www.bvucoepune.edu.in",
            "nirf_rank": 170,
            "facilities": ["Library", "Sports Complex", "Hostels", "Research Labs", "Cafeteria"],
            "placement": {
                "highest_package": "25 LPA",
                "average_package": "6.5 LPA",
                "placement_percentage": 82,
                "top_recruiters": ["TCS", "Infosys", "Wipro", "L&T", "Cognizant"]
            },
            "contact": {
                "email": "principal@bvucoep.edu.in",
                "phone": "+91-20-24107390",
                "address": "Katraj, Pune, Maharashtra 411043"
            },
            "status": "active"
        },
        {
            "_id": "12",
            "college_name": "Government College of Engineering, Karad",
            "location": "Karad, Maharashtra",
            "established": 1960,
            "type": "Government Institute",
            "accreditation": "NAAC A",
            "website": "www.gcekarad.ac.in",
            "nirf_rank": 190,
            "facilities": ["Library", "Sports Complex", "Hostels", "Research Labs", "Cafeteria"],
            "placement": {
                "highest_package": "16 LPA",
                "average_package": "5.5 LPA",
                "placement_percentage": 78,
                "top_recruiters": ["TCS", "Infosys", "Wipro", "L&T", "Cognizant"]
            },
            "contact": {
                "email": "principal@gcekarad.ac.in",
                "phone": "+91-2164-271711",
                "address": "Vidyanagar, Karad, Satara, Maharashtra 415124"
            },
            "status": "active"
        },
        {
            "_id": "13",
            "college_name": "Shri Guru Gobind Singhji Institute of Engineering and Technology",
            "location": "Nanded, Maharashtra",
            "established": 1981,
            "type": "Government Aided Autonomous Institute",
            "accreditation": "NAAC A",
            "website": "www.sggs.ac.in",
            "nirf_rank": 175,
            "facilities": ["Library", "Sports Complex", "Hostels", "Research Labs", "Cafeteria"],
            "placement": {
                "highest_package": "20 LPA",
                "average_package": "6 LPA",
                "placement_percentage": 80,
                "top_recruiters": ["TCS", "Infosys", "Wipro", "L&T", "Cognizant"]
            },
            "contact": {
                "email": "director@sggs.ac.in",
                "phone": "+91-2462-269234",
                "address": "SGGS Institute of Engineering and Technology, Vishnupuri, Nanded, Maharashtra 431606"
            },
            "status": "active"
        },
        {
            "_id": "14",
            "college_name": "Dr. Babasaheb Ambedkar Technological University",
            "location": "Lonere, Maharashtra",
            "established": 1989,
            "type": "State University",
            "accreditation": "NAAC A",
            "website": "www.dbatu.ac.in",
            "nirf_rank": 185,
            "facilities": ["Library", "Sports Complex", "Hostels", "Research Labs", "Cafeteria"],
            "placement": {
                "highest_package": "18 LPA",
                "average_package": "5.8 LPA",
                "placement_percentage": 75,
                "top_recruiters": ["TCS", "Infosys", "Wipro", "L&T", "Cognizant"]
            },
            "contact": {
                "email": "registrar@dbatu.ac.in",
                "phone": "+91-2140-275142",
                "address": "Lonere, Raigad, Maharashtra 402103"
            },
            "status": "active"
        },
        {
            "_id": "15",
            "college_name": "Government College of Engineering, Aurangabad",
            "location": "Aurangabad, Maharashtra",
            "established": 1960,
            "type": "Government Institute",
            "accreditation": "NAAC A",
            "website": "www.geca.ac.in",
            "nirf_rank": 195,
            "facilities": ["Library", "Sports Complex", "Hostels", "Research Labs", "Cafeteria"],
            "placement": {
                "highest_package": "15 LPA",
                "average_package": "5.5 LPA",
                "placement_percentage": 75,
                "top_recruiters": ["TCS", "Infosys", "Wipro", "L&T", "Cognizant"]
            },
            "contact": {
                "email": "principal@geca.ac.in",
                "phone": "+91-240-2366111",
                "address": "Railway Station Road, Osmanpura, Aurangabad, Maharashtra 431005"
            },
            "status": "active"
        },
        {
            "_id": "16",
            "college_name": "Pimpri Chinchwad College of Engineering",
            "location": "Pune, Maharashtra",
            "established": 1999,
            "type": "Private Institute",
            "accreditation": "NAAC A",
            "website": "www.pccoepune.com",
            "nirf_rank": 200,
            "facilities": ["Library", "Sports Complex", "Hostels", "Research Labs", "Cafeteria"],
            "placement": {
                "highest_package": "22 LPA",
                "average_package": "6 LPA",
                "placement_percentage": 80,
                "top_recruiters": ["TCS", "Infosys", "Wipro", "L&T", "Cognizant"]
            },
            "contact": {
                "email": "principal@pccoepune.org",
                "phone": "+91-20-27653168",
                "address": "Sector 26, Pradhikaran, Nigdi, Pune, Maharashtra 411044"
            },
            "status": "active"
        },
        {
            "_id": "17",
            "college_name": "Sinhgad College of Engineering",
            "location": "Pune, Maharashtra",
            "established": 1996,
            "type": "Private Institute",
            "accreditation": "NAAC A",
            "website": "www.sinhgad.edu",
            "nirf_rank": 210,
            "facilities": ["Library", "Sports Complex", "Hostels", "Research Labs", "Cafeteria"],
            "placement": {
                "highest_package": "20 LPA",
                "average_package": "5.8 LPA",
                "placement_percentage": 78,
                "top_recruiters": ["TCS", "Infosys", "Wipro", "L&T", "Cognizant"]
            },
            "contact": {
                "email": "principal.scoe@sinhgad.edu",
                "phone": "+91-20-24357033",
                "address": "S. No. 44/1, Vadgaon Budruk, Off Sinhgad Road, Pune, Maharashtra 411041"
            },
            "status": "active"
        },
        {
            "_id": "18",
            "college_name": "D.Y. Patil College of Engineering",
            "location": "Pune, Maharashtra",
            "established": 1984,
            "type": "Private Institute",
            "accreditation": "NAAC A",
            "website": "www.dypcoe.ac.in",
            "nirf_rank": 220,
            "facilities": ["Library", "Sports Complex", "Hostels", "Research Labs", "Cafeteria"],
            "placement": {
                "highest_package": "18 LPA",
                "average_package": "5.5 LPA",
                "placement_percentage": 75,
                "top_recruiters": ["TCS", "Infosys", "Wipro", "L&T", "Cognizant"]
            },
            "contact": {
                "email": "principal@dypcoe.ac.in",
                "phone": "+91-20-27653311",
                "address": "Sector 29, Nigdi Pradhikaran, Akurdi, Pune, Maharashtra 411044"
            },
            "status": "active"
        },
        {
            "_id": "19",
            "college_name": "Army Institute of Technology",
            "location": "Pune, Maharashtra",
            "established": 1994,
            "type": "Private Institute",
            "accreditation": "NAAC A",
            "website": "www.aitpune.edu.in",
            "nirf_rank": 165,
            "facilities": ["Library", "Sports Complex", "Hostels", "Research Labs", "Cafeteria"],
            "placement": {
                "highest_package": "26 LPA",
                "average_package": "7 LPA",
                "placement_percentage": 85,
                "top_recruiters": ["TCS", "Infosys", "Wipro", "Microsoft", "Amazon"]
            },
            "contact": {
                "email": "director@aitpune.edu.in",
                "phone": "+91-20-27157534",
                "address": "Dighi Hills, Alandi Road, Pune, Maharashtra 411015"
            },
            "status": "active"
        },
        {
            "_id": "20",
            "college_name": "International Institute of Information Technology",
            "location": "Pune, Maharashtra",
            "established": 2013,
            "type": "Private Institute",
            "accreditation": "NAAC A",
            "website": "www.isquareit.edu.in",
            "nirf_rank": 155,
            "facilities": ["Library", "Sports Complex", "Hostels", "Research Labs", "Cafeteria"],
            "placement": {
                "highest_package": "32 LPA",
                "average_package": "8 LPA",
                "placement_percentage": 88,
                "top_recruiters": ["TCS", "Infosys", "Wipro", "Microsoft", "Amazon"]
            },
            "contact": {
                "email": "director@isquareit.edu.in",
                "phone": "+91-20-66759509",
                "address": "P-14, Rajiv Gandhi Infotech Park, Phase 1, Hinjawadi, Pune, Maharashtra 411057"
            },
            "status": "active"
        },
        {
            "_id": "21",
            "college_name": "Ramrao Adik Institute of Technology",
            "location": "Navi Mumbai, Maharashtra",
            "established": 1983,
            "type": "Private Institute",
            "accreditation": "NAAC A",
            "website": "www.rait.ac.in",
            "nirf_rank": 225,
            "facilities": ["Library", "Sports Complex", "Hostels", "Research Labs", "Cafeteria"],
            "placement": {
                "highest_package": "18 LPA",
                "average_package": "5.5 LPA",
                "placement_percentage": 75,
                "top_recruiters": ["TCS", "Infosys", "Wipro", "L&T", "Cognizant"]
            },
            "contact": {
                "email": "principal@rait.ac.in",
                "phone": "+91-22-27709507",
                "address": "Dr. D.Y. Patil Vidyanagar, Sector 7, Nerul, Navi Mumbai, Maharashtra 400706"
            },
            "status": "active"
        },
        {
            "_id": "22",
            "college_name": "Fr. Conceicao Rodrigues College of Engineering",
            "location": "Mumbai, Maharashtra",
            "established": 1984,
            "type": "Private Institute",
            "accreditation": "NAAC A",
            "website": "www.frcrce.ac.in",
            "nirf_rank": 230,
            "facilities": ["Library", "Sports Complex", "Hostels", "Research Labs", "Cafeteria"],
            "placement": {
                "highest_package": "17 LPA",
                "average_package": "5.2 LPA",
                "placement_percentage": 72,
                "top_recruiters": ["TCS", "Infosys", "Wipro", "L&T", "Cognizant"]
            },
            "contact": {
                "email": "principal@frcrce.ac.in",
                "phone": "+91-22-26700058",
                "address": "Agnel Technical Education Complex, Sector 9-A, Vashi, Navi Mumbai, Maharashtra 400703"
            },
            "status": "active"
        },
        {
            "_id": "23",
            "college_name": "Vishwakarma Institute of Information Technology",
            "location": "Pune, Maharashtra",
            "established": 2002,
            "type": "Private Institute",
            "accreditation": "NAAC A",
            "website": "www.viit.ac.in",
            "nirf_rank": 235,
            "facilities": ["Library", "Sports Complex", "Hostels", "Research Labs", "Cafeteria"],
            "placement": {
                "highest_package": "16 LPA",
                "average_package": "5 LPA",
                "placement_percentage": 70,
                "top_recruiters": ["TCS", "Infosys", "Wipro", "L&T", "Cognizant"]
            },
            "contact": {
                "email": "principal@viit.ac.in",
                "phone": "+91-20-26950200",
                "address": "Survey No. 3/4, Kondhwa (Budruk), Pune, Maharashtra 411048"
            },
            "status": "active"
        },
        {
            "_id": "24",
            "college_name": "Pillai College of Engineering",
            "location": "Navi Mumbai, Maharashtra",
            "established": 1999,
            "type": "Private Institute",
            "accreditation": "NAAC A",
            "website": "www.pce.ac.in",
            "nirf_rank": 240,
            "facilities": ["Library", "Sports Complex", "Hostels", "Research Labs", "Cafeteria"],
            "placement": {
                "highest_package": "15 LPA",
                "average_package": "4.8 LPA",
                "placement_percentage": 68,
                "top_recruiters": ["TCS", "Infosys", "Wipro", "L&T", "Cognizant"]
            },
            "contact": {
                "email": "principal@pce.ac.in",
                "phone": "+91-22-27481247",
                "address": "Dr. K. M. Vasudevan Pillai's Campus, Sector 16, New Panvel, Navi Mumbai, Maharashtra 410206"
            },
            "status": "active"
        },
        {
            "_id": "25",
            "college_name": "Don Bosco Institute of Technology",
            "location": "Mumbai, Maharashtra",
            "established": 2001,
            "type": "Private Institute",
            "accreditation": "NAAC A",
            "website": "www.dbit.in",
            "nirf_rank": 245,
            "facilities": ["Library", "Sports Complex", "Hostels", "Research Labs", "Cafeteria"],
            "placement": {
                "highest_package": "14 LPA",
                "average_package": "4.5 LPA",
                "placement_percentage": 65,
                "top_recruiters": ["TCS", "Infosys", "Wipro", "L&T", "Cognizant"]
            },
            "contact": {
                "email": "principal@dbit.in",
                "phone": "+91-22-28933386",
                "address": "Premier Automobiles Road, Kurla West, Mumbai, Maharashtra 400070"
            },
            "status": "active"
        },
        {
            "_id": "26",
            "college_name": "Terna Engineering College",
            "location": "Navi Mumbai, Maharashtra",
            "established": 1991,
            "type": "Private Institute",
            "accreditation": "NAAC A",
            "website": "www.ternaengg.ac.in",
            "nirf_rank": 250,
            "facilities": ["Library", "Sports Complex", "Hostels", "Research Labs", "Cafeteria"],
            "placement": {
                "highest_package": "13 LPA",
                "average_package": "4.2 LPA",
                "placement_percentage": 62,
                "top_recruiters": ["TCS", "Infosys", "Wipro", "L&T", "Cognizant"]
            },
            "contact": {
                "email": "principal@ternaengg.ac.in",
                "phone": "+91-22-27789308",
                "address": "Plot No. 12, Sector 22, Nerul, Navi Mumbai, Maharashtra 400706"
            },
            "status": "active"
        },
        {
            "_id": "27",
            "college_name": "Rajiv Gandhi Institute of Technology",
            "location": "Mumbai, Maharashtra",
            "established": 1993,
            "type": "Government Institute",
            "accreditation": "NAAC A",
            "website": "www.rgit.ac.in",
            "nirf_rank": 255,
            "facilities": ["Library", "Sports Complex", "Hostels", "Research Labs", "Cafeteria"],
            "placement": {
                "highest_package": "12 LPA",
                "average_package": "4 LPA",
                "placement_percentage": 60,
                "top_recruiters": ["TCS", "Infosys", "Wipro", "L&T", "Cognizant"]
            },
            "contact": {
                "email": "principal@rgit.ac.in",
                "phone": "+91-22-28042934",
                "address": "Juhu Versova Link Road, Versova, Andheri West, Mumbai, Maharashtra 400053"
            },
            "status": "active"
        },
        {
            "_id": "28",
            "college_name": "Vidyalankar Institute of Technology",
            "location": "Mumbai, Maharashtra",
            "established": 1999,
            "type": "Private Institute",
            "accreditation": "NAAC A",
            "website": "www.vit.edu.in",
            "nirf_rank": 260,
            "facilities": ["Library", "Sports Complex", "Hostels", "Research Labs", "Cafeteria"],
            "placement": {
                "highest_package": "11 LPA",
                "average_package": "3.8 LPA",
                "placement_percentage": 58,
                "top_recruiters": ["TCS", "Infosys", "Wipro", "L&T", "Cognizant"]
            },
            "contact": {
                "email": "principal@vit.edu.in",
                "phone": "+91-22-24161126",
                "address": "Vidyalankar College Marg, Wadala East, Mumbai, Maharashtra 400037"
            },
            "status": "active"
        },
        {
            "_id": "29",
            "college_name": "Atharva College of Engineering",
            "location": "Mumbai, Maharashtra",
            "established": 1999,
            "type": "Private Institute",
            "accreditation": "NAAC A",
            "website": "www.atharvacoe.ac.in",
            "nirf_rank": 265,
            "facilities": ["Library", "Sports Complex", "Hostels", "Research Labs", "Cafeteria"],
            "placement": {
                "highest_package": "10 LPA",
                "average_package": "3.5 LPA",
                "placement_percentage": 55,
                "top_recruiters": ["TCS", "Infosys", "Wipro", "L&T", "Cognizant"]
            },
            "contact": {
                "email": "principal@atharvacoe.ac.in",
                "phone": "+91-22-28840707",
                "address": "Malad Marve Road, Charkop Naka, Malad West, Mumbai, Maharashtra 400095"
            },
            "status": "active"
        },
        {
            "_id": "30",
            "college_name": "Datta Meghe College of Engineering",
            "location": "Navi Mumbai, Maharashtra",
            "established": 1988,
            "type": "Private Institute",
            "accreditation": "NAAC A",
            "website": "www.dmce.ac.in",
            "nirf_rank": 270,
            "facilities": ["Library", "Sports Complex", "Hostels", "Research Labs", "Cafeteria"],
            "placement": {
                "highest_package": "9 LPA",
                "average_package": "3.2 LPA",
                "placement_percentage": 52,
                "top_recruiters": ["TCS", "Infosys", "Wipro", "L&T", "Cognizant"]
            },
            "contact": {
                "email": "principal@dmce.ac.in",
                "phone": "+91-22-27481247",
                "address": "Sector 3, Airoli, Navi Mumbai, Maharashtra 400708"
            },
            "status": "active"
        }
    ]
    
    # Insert colleges data
    colleges_collection.insert_many(colleges_data)
    
    # Generate cutoff data for each college
    cutoffs_data = []
    
    # Define courses
    courses = [
        "Computer Science and Engineering",
        "Information Technology",
        "Electronics and Communication Engineering",
        "Electrical Engineering",
        "Mechanical Engineering",
        "Civil Engineering",
        "Chemical Engineering",
        "Artificial Intelligence and Data Science"
    ]
    
    # Define categories
    categories = ["OPEN", "OBC", "SC", "ST", "EWS", "SEBC", "VJNT", "SBC"]
    
    # Generate cutoff data for each college
    for college in colleges_data:
        college_id = college["_id"]
        college_name = college["college_name"]
        
        # Determine number of courses for this college (between 4 and 8)
        num_courses = random.randint(4, 8)
        selected_courses = random.sample(courses, num_courses)
        
        for course in selected_courses:
            # Base percentile for this course at this college
            base_percentile = random.uniform(70, 99)
            
            for category in categories:
                # Adjust percentile based on category
                if category == "OPEN":
                    percentile = base_percentile
                elif category == "EWS":
                    percentile = base_percentile - random.uniform(0.5, 2)
                elif category == "OBC":
                    percentile = base_percentile - random.uniform(2, 5)
                elif category == "SEBC" or category == "VJNT" or category == "SBC":
                    percentile = base_percentile - random.uniform(5, 8)
                elif category == "SC":
                    percentile = base_percentile - random.uniform(8, 12)
                else:  # ST
                    percentile = base_percentile - random.uniform(12, 15)
                
                # Ensure percentile is not below 45
                percentile = max(45, percentile)
                
                # Calculate rank based on percentile
                rank = int((100 - percentile) * 1000)
                
                # Create cutoff entry
                cutoff_entry = {
                    "college_id": college_id,
                    "college_name": college_name,
                    "course_name": course,
                    "category": category,
                    "percentile": round(percentile, 2),
                    "rank": rank,
                    "year": 2023,
                    "status": "active"
                }
                
                cutoffs_data.append(cutoff_entry)
    
    # Insert cutoffs data
    cutoffs_collection.insert_many(cutoffs_data)
    
    return len(colleges_data), len(cutoffs_data)

# Function to update MongoDB integration file
def update_mongodb_integration():
    # Add code to update mongodb_integration.py with functions to access the new dataset
    pass

# Main function to be called from app.py
def setup_college_dataset():
    try:
        # Connect to MongoDB
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        
        # Initialize dataset
        num_colleges, num_cutoffs = initialize_college_dataset(client)
        
        # Update integration file
        update_mongodb_integration()
        
        return True, f"Successfully added {num_colleges} colleges and {num_cutoffs} cutoff records"
    except Exception as e:
        return False, f"Error setting up college dataset: {str(e)}"

if __name__ == "__main__":
    success, message = setup_college_dataset()
    print(message)