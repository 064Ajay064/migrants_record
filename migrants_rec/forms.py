"""Form definitions for the Migrant Health Records application."""

from flask_wtf import FlaskForm
from wtforms import (
    StringField, IntegerField, SubmitField,
    SelectField, PasswordField, FloatField, BooleanField, DateField
)
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional

class LoginForm(FlaskForm):
    """Form for user login."""
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class RegistrationForm(FlaskForm):
    """Form for user registration."""
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    role = SelectField("Role", choices=[("admin", "Admin"), ("healthcare_worker", "Healthcare Worker")])
    submit = SubmitField("Register")

class SearchForm(FlaskForm):
    """Form for searching migrant records."""
    search_term = StringField("Search", validators=[Length(max=100)])
    filter_by = SelectField("Filter By", choices=[
        ("name", "Name"), ("gender", "Gender"), ("health_condition", "Health Condition"),
        ("contact", "Contact"), ("id", "ID")
    ])
    submit = SubmitField("Search")

class MigrantForm(FlaskForm):
    """Form for adding and editing migrant records."""

    # Personal Information (Core Required Fields)
    name = StringField("Full Name", validators=[DataRequired(), Length(min=2, max=100)])
    age = IntegerField("Age", validators=[DataRequired()])
    gender = SelectField("Gender", choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")], validators=[DataRequired()])
    contact = StringField("Contact Number", validators=[DataRequired(), Length(min=5, max=20)])
    
    # Personal Information (Optional/Auxiliary Fields)
    date_of_birth = DateField("Date of Birth", format='%Y-%m-%d', validators=[Optional()]) 
    nationality = StringField("Nationality", validators=[Optional(), Length(max=50)])
    state_of_origin = StringField("State of Origin", validators=[Optional(), Length(max=50)])
    emergency_contact_name = StringField("Emergency Contact Person", validators=[Optional(), Length(max=100)])
    emergency_contact_number = StringField("Emergency Contact Number", validators=[Optional(), Length(max=20)])
    aadhaar_passport = StringField("Aadhaar/Passport Number", validators=[Optional(), Length(max=50)])
    preferred_language = SelectField("Preferred Language", choices=[("English", "English"), ("Malayalam", "Malayalam"), ("Hindi", "Hindi"), ("Bengali", "Bengali"), ("Tamil", "Tamil"), ("Odiya", "Odiya"), ("Other", "Other")], validators=[Optional()])
    literacy_level = SelectField("Literacy Level", choices=[("Illiterate", "Illiterate"), ("Basic", "Basic"), ("Intermediate", "Intermediate"), ("Advanced", "Advanced")], validators=[Optional()])
    data_sharing_consent = BooleanField("Consent for Data Sharing")
    
    # Work Information (All Optional in models)
    occupation = StringField("Occupation/Job Role", validators=[Optional(), Length(max=100)])
    employer_name = StringField("Employer/Contractor Name", validators=[Optional(), Length(max=100)])
    employer_contact = StringField("Employer Contact", validators=[Optional(), Length(max=20)])
    work_location_district = StringField("Work Location (District)", validators=[Optional(), Length(max=50)])
    work_location_pincode = StringField("Work Location (Pincode)", validators=[Optional(), Length(max=10)])
    duration_of_stay = StringField("Duration of Stay in Kerala", validators=[Optional(), Length(max=50)])
    living_conditions = SelectField("Living Conditions", choices=[("Hostel", "Hostel"), ("Shared Housing", "Shared Housing"), ("Camp", "Camp"), ("Individual Rental", "Individual Rental"), ("Other", "Other")], validators=[Optional()])
    
    # Health History & Status (All Optional)
    allergies = StringField("Allergies (Food, Drug, Environmental)", validators=[Optional(), Length(max=500)])
    past_medical_conditions = StringField("Past Medical Conditions", validators=[Optional(), Length(max=500)])
    past_surgical_history = StringField("Past Surgical History", validators=[Optional(), Length(max=500)])
    family_history = StringField("Family History", validators=[Optional(), Length(max=500)])
    immunization_status = StringField("Immunization Status", validators=[Optional(), Length(max=500)])
    height = FloatField("Height (cm)", validators=[Optional()])
    weight = FloatField("Weight (kg)", validators=[Optional()])
    blood_group = SelectField("Blood Group", choices=[("", "Select Blood Group"), ("A+", "A+"), ("A-", "A-"), ("B+", "B+"), ("B-", "B-"), ("AB+", "AB+"), ("AB-", "AB-"), ("O+", "O+"), ("O-", "O-"), ("Unknown", "Unknown")], validators=[Optional()])
    vital_signs = StringField("Vital Signs (BP, Pulse, Temp, SpO₂)", validators=[Optional()])
    current_medications = StringField("Current Medications", validators=[Optional(), Length(max=500)])
    ongoing_treatment = StringField("Ongoing Treatment", validators=[Optional(), Length(max=500)])
    infectious_disease_screening = StringField("Infectious Disease Screening", validators=[Optional(), Length(max=500)])
    health_condition = StringField("Health Condition", validators=[Optional(), Length(max=200)])
    
    # Visit & Medical Records (All Optional)
    last_checkup = DateField("Last Checkup", format='%Y-%m-%d', validators=[Optional()])
    healthcare_facility = StringField("Healthcare Facility Name", validators=[Optional(), Length(max=100)])
    doctor_name = StringField("Doctor/Health Worker Name", validators=[Optional(), Length(max=100)])
    symptoms = StringField("Symptoms Presented", validators=[Optional(), Length(max=500)])
    diagnosis = StringField("Diagnosis", validators=[Optional(), Length(max=500)])
    prescriptions = StringField("Prescriptions/Medicines Given", validators=[Optional(), Length(max=500)])
    lab_results = StringField("Lab Test Results", validators=[Optional(), Length(max=500)])
    vaccination_records = StringField("Vaccination Records", validators=[Optional(), Length(max=500)])
    
    # Public Health / Surveillance (All Optional)
    disease_alerts = StringField("Disease Alerts", validators=[Optional(), Length(max=500)])
    contact_tracing_info = StringField("Contact Tracing Info", validators=[Optional(), Length(max=500)])
    referral_notes = StringField("Referral Notes", validators=[Optional(), Length(max=500)])
    follow_up_date = DateField("Follow-up Due Date", format='%Y-%m-%d', validators=[Optional()])
    
    submit = SubmitField("Save")