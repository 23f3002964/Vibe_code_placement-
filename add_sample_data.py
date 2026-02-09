from app import app, db, User, Student, Company
from werkzeug.security import generate_password_hash

def add_sample_data():
    with app.app_context():
        # Check if sample data already exists
        if User.query.first():
            print("Sample data already exists in the database.")
            return
        
        # Create a sample student user and profile
        student_user = User(
            email='student@example.com',
            user_type='student'
        )
        student_user.set_password('password123')
        
        student_profile = Student(
            name='John Doe',
            student_id='STD001',
            course='Computer Science',
            year_of_study='3',
            user=student_user
        )
        
        # Create a sample company user and profile
        company_user = User(
            email='company@example.com',
            user_type='company'
        )
        company_user.set_password('password123')
        
        company_profile = Company(
            company_name='Tech Corp',
            contact_person='Jane Smith',
            phone='+1234567890',
            website='https://techcorp.com',
            industry='technology',
            description='A leading technology company specializing in software development.',
            user=company_user
        )
        
        # Add to session and commit
        db.session.add(student_user)
        db.session.add(student_profile)
        db.session.add(company_user)
        db.session.add(company_profile)
        
        db.session.commit()
        print("Sample data added successfully!")

if __name__ == '__main__':
    add_sample_data()