from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)  # 'student' or 'company' or 'admin'
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    student_profile = db.relationship('Student', backref='user', uselist=False, cascade='all, delete-orphan')
    company_profile = db.relationship('Company', backref='user', uselist=False, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_student(self):
        return self.user_type == 'student'
    
    def is_company(self):
        return self.user_type == 'company'
    
    def is_admin_role(self):
        return self.is_admin

class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    student_id = db.Column(db.String(50), unique=True)
    course = db.Column(db.String(100))
    year_of_study = db.Column(db.String(20))
    phone = db.Column(db.String(20))
    resume_url = db.Column(db.String(255))
    skills = db.Column(db.Text)
    cgpa = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    applications = db.relationship('Application', backref='student', lazy=True)

class Company(db.Model):
    __tablename__ = 'companies'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    contact_person = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    website = db.Column(db.String(100))
    industry = db.Column(db.String(50))
    description = db.Column(db.Text)
    established_year = db.Column(db.Integer)
    company_size = db.Column(db.String(20))  # Small, Medium, Large
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    jobs = db.relationship('Job', backref='company', lazy=True)

class Job(db.Model):
    __tablename__ = 'jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text)
    location = db.Column(db.String(100))
    salary_min = db.Column(db.Integer)  # Minimum salary in INR
    salary_max = db.Column(db.Integer)  # Maximum salary in INR
    job_type = db.Column(db.String(20))  # Full-time, Part-time, Internship
    experience_required = db.Column(db.String(20))
    posted_date = db.Column(db.DateTime, default=datetime.utcnow)
    deadline = db.Column(db.Date)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    applications = db.relationship('Application', backref='job', lazy=True)

class Application(db.Model):
    __tablename__ = 'applications'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    cover_letter = db.Column(db.Text)
    resume_url = db.Column(db.String(255))
    status = db.Column(db.String(20), default='pending')  # pending, accepted, rejected
    applied_date = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_date = db.Column(db.DateTime)
    
    # Ensure a student can only apply to a job once
    __table_args__ = (db.UniqueConstraint('student_id', 'job_id'),)