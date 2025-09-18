from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), default="healthcare_worker")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
    def is_admin(self):
        return self.role == "admin"

    def __repr__(self):
        return f"<User {self.username}>"

class Migrant(db.Model):
    __tablename__ = "migrants"
    # 1. Personal Information
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=True) 
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    nationality = db.Column(db.String(50), nullable=True)
    state_of_origin = db.Column(db.String(50), nullable=True)
    contact = db.Column(db.String(20), nullable=False)
    emergency_contact_name = db.Column(db.String(100), nullable=True)
    emergency_contact_number = db.Column(db.String(20), nullable=True)
    aadhaar_passport = db.Column(db.String(50), nullable=True, unique=True)
    preferred_language = db.Column(db.String(30), nullable=True)
    literacy_level = db.Column(db.String(30), nullable=True)
    data_sharing_consent = db.Column(db.Boolean, default=False)
    
    # 2. Work Information
    occupation = db.Column(db.String(100), nullable=True)
    employer_name = db.Column(db.String(100), nullable=True)
    employer_contact = db.Column(db.String(20), nullable=True)
    work_location_district = db.Column(db.String(50), nullable=True)
    work_location_pincode = db.Column(db.String(10), nullable=True)
    duration_of_stay = db.Column(db.String(50), nullable=True)
    living_conditions = db.Column(db.String(50), nullable=True)
    
    # 3. Health History
    allergies = db.Column(db.Text, nullable=True)
    past_medical_conditions = db.Column(db.Text, nullable=True)
    past_surgical_history = db.Column(db.Text, nullable=True)
    family_history = db.Column(db.Text, nullable=True)
    immunization_status = db.Column(db.Text, nullable=True)
    
    # 4. Current Health Status
    height = db.Column(db.Float, nullable=True)
    weight = db.Column(db.Float, nullable=True)
    bmi = db.Column(db.Float, nullable=True)
    blood_group = db.Column(db.String(5), nullable=True)
    vital_signs = db.Column(db.Text, nullable=True)
    current_medications = db.Column(db.Text, nullable=True)
    ongoing_treatment = db.Column(db.Text, nullable=True)
    infectious_disease_screening = db.Column(db.Text, nullable=True)
    health_condition = db.Column(db.String(200), nullable=True)
    
    # 5. Visit & Medical Records
    last_checkup = db.Column(db.Date, nullable=True)
    healthcare_facility = db.Column(db.String(100), nullable=True)
    doctor_name = db.Column(db.String(100), nullable=True)
    symptoms = db.Column(db.Text, nullable=True)
    diagnosis = db.Column(db.Text, nullable=True)
    prescriptions = db.Column(db.Text, nullable=True)
    lab_results = db.Column(db.Text, nullable=True)
    vaccination_records = db.Column(db.Text, nullable=True)
    
    # 7. Public Health / Surveillance
    disease_alerts = db.Column(db.Text, nullable=True)
    contact_tracing_info = db.Column(db.Text, nullable=True)
    referral_notes = db.Column(db.Text, nullable=True)
    follow_up_date = db.Column(db.Date, nullable=True)
    qr_code = db.Column(db.String(255), nullable=True)

    def calculate_bmi(self):
        """Calculate BMI if height and weight are available."""
        if self.height and self.weight and self.height > 0:
            self.bmi = round(self.weight / ((self.height/100) ** 2), 2)
            return self.bmi
        return None