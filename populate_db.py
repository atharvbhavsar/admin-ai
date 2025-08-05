#!/usr/bin/env python3
"""
Database Population Script for AdmitAI College Finder
This script populates the database with sample data for testing and demonstration.
"""

from app import app, db, Exam, College, Cutoff, Branch, Scholarship, ImportantDate
from datetime import datetime
from mongodb_integration import setup_mongodb

def populate_database():
    """Populate the database with sample data"""
    # Clear existing data
    db.session.query(ImportantDate).delete()
    db.session.query(Scholarship).delete()
    db.session.query(Cutoff).delete()
    db.session.query(Branch).delete()
    db.session.query(College).delete()
    db.session.query(Exam).delete()
    db.session.commit()
    
    # Add exams
    exams = [
        Exam(name='MHT-CET', full_name='Maharashtra Common Entrance Test', 
             description='State-level entrance exam for engineering and pharmacy courses in Maharashtra',
             website='https://cetcell.mahacet.org/',
             exam_date=datetime(2023, 5, 15),
             registration_start=datetime(2023, 2, 1),
             registration_end=datetime(2023, 3, 15),
             result_date=datetime(2023, 6, 10)),
        Exam(name='JEE Main', full_name='Joint Entrance Examination Main',
             description='National level entrance exam for admission to engineering colleges across India',
             website='https://jeemain.nta.nic.in/',
             exam_date=datetime(2023, 4, 10),
             registration_start=datetime(2023, 1, 15),
             registration_end=datetime(2023, 2, 28),
             result_date=datetime(2023, 5, 5)),
        Exam(name='NEET', full_name='National Eligibility cum Entrance Test',
             description='National level entrance exam for admission to medical colleges in India',
             website='https://neet.nta.nic.in/',
             exam_date=datetime(2023, 5, 7),
             registration_start=datetime(2023, 2, 10),
             registration_end=datetime(2023, 3, 25),
             result_date=datetime(2023, 6, 15))
    ]
    
    for exam in exams:
        db.session.add(exam)
    db.session.commit()
    
    # Add colleges
    colleges = [
        # Top Engineering Colleges
        College(name='College of Engineering, Pune (COEP)', city='Pune', state='Maharashtra',
                type='Government Autonomous', established=1854, website='https://www.coep.org.in/',
                nirf_ranking=15, accreditation='A+', campus_area=37, has_hostel=True,
                placement_percentage=95, average_package=12.5, highest_package=43.3,
                description='One of the oldest and most prestigious engineering colleges in India.'),
        College(name='Veermata Jijabai Technological Institute (VJTI)', city='Mumbai', state='Maharashtra',
                type='Government Aided Autonomous', established=1887, website='https://www.vjti.ac.in/',
                nirf_ranking=27, accreditation='A+', campus_area=45, has_hostel=True,
                placement_percentage=92, average_package=10.8, highest_package=39.5,
                description='Premier technological institute with excellent industry connections.'),
        College(name='Sardar Patel Institute of Technology (SPIT)', city='Mumbai', state='Maharashtra',
                type='Private Autonomous', established=1995, website='https://www.spit.ac.in/',
                nirf_ranking=42, accreditation='A', campus_area=18, has_hostel=True,
                placement_percentage=90, average_package=11.2, highest_package=35.0,
                description='Known for its excellent computer science and IT programs.'),
        College(name='Pune Institute of Computer Technology (PICT)', city='Pune', state='Maharashtra',
                type='Private', established=1983, website='https://www.pict.edu/',
                nirf_ranking=55, accreditation='A', campus_area=15, has_hostel=True,
                placement_percentage=88, average_package=9.5, highest_package=32.0,
                description='Specialized institute focused on computer technology education.'),
        College(name='Walchand College of Engineering, Sangli', city='Sangli', state='Maharashtra',
                type='Government Aided Autonomous', established=1947, website='https://www.walchandsangli.ac.in/',
                nirf_ranking=68, accreditation='A', campus_area=90, has_hostel=True,
                placement_percentage=85, average_package=8.2, highest_package=28.5,
                description='One of the oldest engineering colleges in Maharashtra with a large campus.'),
        College(name='K. J. Somaiya College of Engineering', city='Mumbai', state='Maharashtra',
                type='Private Autonomous', established=1983, website='https://kjsce.somaiya.edu/',
                nirf_ranking=72, accreditation='A', campus_area=65, has_hostel=True,
                placement_percentage=87, average_package=9.8, highest_package=30.0,
                description='Part of the prestigious Somaiya Vidyavihar complex with modern facilities.'),
        College(name='Vishwakarma Institute of Technology (VIT)', city='Pune', state='Maharashtra',
                type='Private Autonomous', established=1983, website='https://www.vit.edu/',
                nirf_ranking=75, accreditation='A+', campus_area=60, has_hostel=True,
                placement_percentage=86, average_package=8.9, highest_package=29.5,
                description='Known for its industry-oriented curriculum and strong alumni network.'),
        College(name='Maharashtra Institute of Technology (MIT)', city='Pune', state='Maharashtra',
                type='Private', established=1983, website='https://www.mitpune.com/',
                nirf_ranking=82, accreditation='A', campus_area=125, has_hostel=True,
                placement_percentage=84, average_package=8.5, highest_package=27.0,
                description='Large campus with diverse engineering programs and good infrastructure.'),
        College(name='Bharati Vidyapeeth College of Engineering', city='Pune', state='Maharashtra',
                type='Private', established=1983, website='https://bvucoepune.edu.in/',
                nirf_ranking=90, accreditation='A', campus_area=40, has_hostel=True,
                placement_percentage=82, average_package=7.8, highest_package=25.0,
                description='Part of Bharati Vidyapeeth Deemed University with strong industry connections.'),
        College(name='Sinhgad College of Engineering', city='Pune', state='Maharashtra',
                type='Private', established=1996, website='https://www.sinhgad.edu/',
                nirf_ranking=95, accreditation='B+', campus_area=110, has_hostel=True,
                placement_percentage=80, average_package=7.2, highest_package=22.0,
                description='Part of the Sinhgad Technical Education Society with a large campus.'),
        
        # Top Medical Colleges
        College(name='Grant Medical College and Sir JJ Hospital', city='Mumbai', state='Maharashtra',
                type='Government', established=1845, website='https://www.gmcjjh.org/',
                nirf_ranking=12, accreditation='A+', campus_area=45, has_hostel=True,
                placement_percentage=98, average_package=15.0, highest_package=None,
                description='One of the oldest and most prestigious medical colleges in India.'),
        College(name='Seth GS Medical College and KEM Hospital', city='Mumbai', state='Maharashtra',
                type='Government', established=1926, website='https://www.kem.edu/',
                nirf_ranking=15, accreditation='A+', campus_area=40, has_hostel=True,
                placement_percentage=97, average_package=14.5, highest_package=None,
                description='Premier medical institution known for its clinical excellence.'),
        College(name='B.J. Medical College', city='Pune', state='Maharashtra',
                type='Government', established=1946, website='https://www.bjmc.edu/',
                nirf_ranking=25, accreditation='A', campus_area=35, has_hostel=True,
                placement_percentage=96, average_package=13.8, highest_package=None,
                description='Renowned medical college affiliated with Sassoon General Hospital.'),
        College(name='Topiwala National Medical College', city='Mumbai', state='Maharashtra',
                type='Government', established=1964, website='https://www.tnmc.edu/',
                nirf_ranking=32, accreditation='A', campus_area=30, has_hostel=True,
                placement_percentage=95, average_package=13.2, highest_package=None,
                description='Well-established medical college with strong clinical training.'),
        College(name='Government Medical College, Nagpur', city='Nagpur', state='Maharashtra',
                type='Government', established=1947, website='https://www.gmcnagpur.gov.in/',
                nirf_ranking=38, accreditation='A', campus_area=42, has_hostel=True,
                placement_percentage=94, average_package=12.8, highest_package=None,
                description='One of the oldest medical colleges in central India with excellent facilities.')
    ]
    
    for college in colleges:
        db.session.add(college)
    db.session.commit()
    
    # Add branches
    branches = [
        # Engineering branches
        Branch(name='Computer Science and Engineering', short_name='CSE', 
               description='Study of computer systems, algorithms, and programming',
               college_id=1, seats=120, fees=125000, duration=4),
        Branch(name='Information Technology', short_name='IT', 
               description='Study of information systems, data management, and software applications',
               college_id=1, seats=60, fees=125000, duration=4),
        Branch(name='Electronics and Communication', short_name='E&TC', 
               description='Study of electronic devices, communication systems, and signal processing',
               college_id=1, seats=120, fees=110000, duration=4),
        Branch(name='Mechanical Engineering', short_name='MECH', 
               description='Study of machines, thermal systems, and manufacturing processes',
               college_id=1, seats=120, fees=100000, duration=4),
        Branch(name='Civil Engineering', short_name='CIVIL', 
               description='Study of design, construction, and maintenance of infrastructure',
               college_id=1, seats=60, fees=90000, duration=4),
        
        Branch(name='Computer Engineering', short_name='CE', 
               description='Study of computer hardware, software, and their integration',
               college_id=2, seats=120, fees=130000, duration=4),
        Branch(name='Information Technology', short_name='IT', 
               description='Study of information systems, data management, and software applications',
               college_id=2, seats=60, fees=130000, duration=4),
        Branch(name='Electronics Engineering', short_name='ETRX', 
               description='Study of electronic circuits, devices, and systems',
               college_id=2, seats=60, fees=115000, duration=4),
        Branch(name='Mechanical Engineering', short_name='MECH', 
               description='Study of machines, thermal systems, and manufacturing processes',
               college_id=2, seats=120, fees=105000, duration=4),
        
        # Add more branches for other colleges...
        
        # Medical branches
        Branch(name='MBBS', short_name='MBBS', 
               description='Bachelor of Medicine and Bachelor of Surgery',
               college_id=11, seats=250, fees=25000, duration=5.5),
        Branch(name='MD Medicine', short_name='MD', 
               description='Doctor of Medicine specialization',
               college_id=11, seats=30, fees=100000, duration=3),
        Branch(name='MS Surgery', short_name='MS', 
               description='Master of Surgery specialization',
               college_id=11, seats=25, fees=100000, duration=3),
        
        Branch(name='MBBS', short_name='MBBS', 
               description='Bachelor of Medicine and Bachelor of Surgery',
               college_id=12, seats=200, fees=25000, duration=5.5),
        Branch(name='MD Pediatrics', short_name='MD Peds', 
               description='Doctor of Medicine in Pediatrics',
               college_id=12, seats=15, fees=120000, duration=3),
        Branch(name='MD Radiology', short_name='MD Rad', 
               description='Doctor of Medicine in Radiology',
               college_id=12, seats=10, fees=150000, duration=3)
    ]
    
    for branch in branches:
        db.session.add(branch)
    db.session.commit()
    
    # Add cutoffs
    cutoffs = [
        # CSE cutoffs for COEP
        Cutoff(college_id=1, branch_id=1, category='OPEN', year=2022, round=1, opening_rank=1, closing_rank=150),
        Cutoff(college_id=1, branch_id=1, category='OBC', year=2022, round=1, opening_rank=151, closing_rank=300),
        Cutoff(college_id=1, branch_id=1, category='SC', year=2022, round=1, opening_rank=301, closing_rank=600),
        Cutoff(college_id=1, branch_id=1, category='ST', year=2022, round=1, opening_rank=601, closing_rank=900),
        Cutoff(college_id=1, branch_id=1, category='OPEN', year=2021, round=1, opening_rank=1, closing_rank=180),
        Cutoff(college_id=1, branch_id=1, category='OBC', year=2021, round=1, opening_rank=181, closing_rank=350),
        
        # IT cutoffs for COEP
        Cutoff(college_id=1, branch_id=2, category='OPEN', year=2022, round=1, opening_rank=151, closing_rank=300),
        Cutoff(college_id=1, branch_id=2, category='OBC', year=2022, round=1, opening_rank=301, closing_rank=450),
        Cutoff(college_id=1, branch_id=2, category='SC', year=2022, round=1, opening_rank=451, closing_rank=750),
        Cutoff(college_id=1, branch_id=2, category='ST', year=2022, round=1, opening_rank=751, closing_rank=1050),
        
        # CE cutoffs for VJTI
        Cutoff(college_id=2, branch_id=6, category='OPEN', year=2022, round=1, opening_rank=1, closing_rank=200),
        Cutoff(college_id=2, branch_id=6, category='OBC', year=2022, round=1, opening_rank=201, closing_rank=400),
        Cutoff(college_id=2, branch_id=6, category='SC', year=2022, round=1, opening_rank=401, closing_rank=700),
        Cutoff(college_id=2, branch_id=6, category='ST', year=2022, round=1, opening_rank=701, closing_rank=1000),
        
        # MBBS cutoffs for Grant Medical
        Cutoff(college_id=11, branch_id=16, category='OPEN', year=2022, round=1, opening_rank=1, closing_rank=100),
        Cutoff(college_id=11, branch_id=16, category='OBC', year=2022, round=1, opening_rank=101, closing_rank=250),
        Cutoff(college_id=11, branch_id=16, category='SC', year=2022, round=1, opening_rank=251, closing_rank=500),
        Cutoff(college_id=11, branch_id=16, category='ST', year=2022, round=1, opening_rank=501, closing_rank=750)
    ]
    
    for cutoff in cutoffs:
        db.session.add(cutoff)
    db.session.commit()
    
    # Add scholarships
    scholarships = [
        Scholarship(name='PMSSS J&K', description='Prime Minister\'s Special Scholarship Scheme for J&K Students',
                    eligibility='Students from Jammu and Kashmir', amount=100000, deadline=datetime(2023, 5, 30)),
        Scholarship(name='Central Sector Scholarship', description='Merit-based scholarship for top 20 percentile students',
                    eligibility='Students in top 20 percentile of their board exams', amount=75000, deadline=datetime(2023, 6, 15)),
        Scholarship(name='Post Matric Scholarship', description='Scholarship for SC/ST/OBC students',
                    eligibility='SC/ST/OBC students with family income below 2.5 lakhs', amount=50000, deadline=datetime(2023, 7, 10)),
        Scholarship(name='AICTE Pragati Scholarship', description='Scholarship for girl students in technical education',
                    eligibility='Girl students in AICTE approved institutions', amount=50000, deadline=datetime(2023, 6, 30)),
        Scholarship(name='Maharashtra State Scholarship', description='State government scholarship for meritorious students',
                    eligibility='Maharashtra domicile students with 80% or above in HSC', amount=25000, deadline=datetime(2023, 7, 25))
    ]
    
    for scholarship in scholarships:
        db.session.add(scholarship)
    db.session.commit()
    
    # Add important dates
    important_dates = [
        ImportantDate(title='MHT-CET Registration Starts', date=datetime(2023, 2, 1), 
                     description='Online registration for MHT-CET 2023 begins'),
        ImportantDate(title='MHT-CET Registration Ends', date=datetime(2023, 3, 15), 
                     description='Last date to register for MHT-CET 2023'),
        ImportantDate(title='MHT-CET Admit Card Release', date=datetime(2023, 4, 30), 
                     description='Download admit cards for MHT-CET 2023'),
        ImportantDate(title='MHT-CET Exam', date=datetime(2023, 5, 15), 
                     description='MHT-CET 2023 examination day'),
        ImportantDate(title='MHT-CET Result Declaration', date=datetime(2023, 6, 10), 
                     description='Results for MHT-CET 2023 will be announced'),
        ImportantDate(title='CAP Round 1 Registration', date=datetime(2023, 6, 20), 
                     description='Registration for Centralized Admission Process Round 1'),
        ImportantDate(title='CAP Round 1 Allotment', date=datetime(2023, 7, 5), 
                     description='Seat allotment for CAP Round 1'),
        ImportantDate(title='CAP Round 2 Registration', date=datetime(2023, 7, 15), 
                     description='Registration for Centralized Admission Process Round 2'),
        ImportantDate(title='CAP Round 2 Allotment', date=datetime(2023, 7, 25), 
                     description='Seat allotment for CAP Round 2'),
        ImportantDate(title='CAP Round 3 Registration', date=datetime(2023, 8, 5), 
                     description='Registration for Centralized Admission Process Round 3'),
        ImportantDate(title='CAP Round 3 Allotment', date=datetime(2023, 8, 15), 
                     description='Seat allotment for CAP Round 3'),
        ImportantDate(title='Spot Round Registration', date=datetime(2023, 8, 25), 
                     description='Registration for Spot Round admissions'),
        ImportantDate(title='Academic Session Begins', date=datetime(2023, 9, 1), 
                     description='Start of academic year 2023-24 for engineering colleges')
    ]
    
    for date in important_dates:
        db.session.add(date)
    db.session.commit()
    
    print("✅ Database populated successfully!")
    print(f"📚 Added {len(exams)} exams")
    print(f"🏫 Added {len(colleges)} colleges")
    print(f"🎓 Added {len(branches)} branches")
    print(f"📊 Added {len(cutoffs)} cutoffs")
    print(f"💰 Added {len(scholarships)} scholarships")
    print(f"📅 Added {len(important_dates)} important dates")

# Add MongoDB setup function
def setup_mongodb_data():
    """Initialize MongoDB with college data"""
    setup_mongodb()
    print("MongoDB initialized with college data successfully!")

if __name__ == "__main__":
    # Uncomment the line below to populate SQLite database
    # populate_database()
    
    # Initialize MongoDB with college data
    setup_mongodb_data()