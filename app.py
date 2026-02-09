from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from config import config
from models import db, User, Student, Company, Job, Application
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import os

app = Flask(__name__)
app.config.from_object(config['default'])

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    """Home page for the placement portal"""
    return render_template('index.html')

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

# Single login route for all user types
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Unified login page for all users"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Find user by email
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')
            
            # Redirect based on user type
            if user.is_admin_role():
                return redirect(url_for('admin'))
            elif user.is_student():
                return redirect(url_for('students'))
            elif user.is_company():
                return redirect(url_for('companies'))
            else:
                # Fallback to home if user type is unknown
                return redirect(url_for('home'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('auth/login.html')

@app.route('/register')
def register():
    """Registration selection page"""
    return render_template('register.html')

@app.route('/register/student', methods=['GET', 'POST'])
def student_register():
    """Student registration page"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        student_id = request.form.get('student_id')
        course = request.form.get('course')
        year = request.form.get('year')
        
        # Check if passwords match
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('auth/student_register.html')
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered', 'error')
            return render_template('auth/student_register.html')
        
        # Create new user
        user = User(email=email, user_type='student')
        user.set_password(password)
        
        # Create student profile
        student = Student(
            name=name,
            student_id=student_id,
            course=course,
            year_of_study=year,
            user=user
        )
        
        try:
            db.session.add(user)
            db.session.add(student)
            db.session.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Registration failed: {str(e)}', 'error')
    
    return render_template('auth/student_register.html')

@app.route('/register/company', methods=['GET', 'POST'])
def company_register():
    """Company registration page"""
    if request.method == 'POST':
        company_name = request.form.get('company_name')
        contact_person = request.form.get('contact_person')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        phone = request.form.get('phone')
        website = request.form.get('website')
        industry = request.form.get('industry')
        description = request.form.get('description')
        
        # Check if passwords match
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('auth/company_register.html')
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered', 'error')
            return render_template('auth/company_register.html')
        
        # Create new user
        user = User(email=email, user_type='company')
        user.set_password(password)
        
        # Create company profile
        company = Company(
            company_name=company_name,
            contact_person=contact_person,
            phone=phone,
            website=website,
            industry=industry,
            description=description,
            user=user
        )
        
        try:
            db.session.add(user)
            db.session.add(company)
            db.session.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Registration failed: {str(e)}', 'error')
    
    return render_template('auth/company_register.html')

@app.route('/logout')
def logout():
    """Logout route"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/students')
@login_required
def students():
    """Students dashboard"""
    if not current_user.is_student():
        flash('Access denied', 'error')
        return redirect(url_for('home'))
    
    student = current_user.student_profile
    return render_template('students.html', student=student)

@app.route('/companies')
@login_required
def companies():
    """Companies page"""
    if not current_user.is_company():
        flash('Access denied', 'error')
        return redirect(url_for('home'))
    
    company = current_user.company_profile
    return render_template('companies.html', company=company)

@app.route('/jobs')
def jobs():
    """Jobs listing page"""
    return render_template('jobs.html')

@app.route('/admin')
@login_required
def admin():
    """Admin dashboard"""
    if not current_user.is_admin_role():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('home'))
    
    # Get counts for dashboard
    total_students = Student.query.count()
    total_companies = Company.query.count()
    total_jobs = Job.query.count()
    total_applications = Application.query.count()
    
    return render_template('admin.html', 
                          total_students=total_students,
                          total_companies=total_companies,
                          total_jobs=total_jobs,
                          total_applications=total_applications)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)