"""Main application module for the Migrant Health Records application."""
# Imports remain the same

from flask import Flask, render_template, redirect, url_for, flash, request, abort, send_file, session
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from functools import wraps
import qrcode
import io
import os
from datetime import datetime, date

# Import models, forms, and config correctly
from config import Config
from models import db, Migrant, User
from forms import MigrantForm, LoginForm, RegistrationForm, SearchForm

# Get BASE_DIR from config scope for path setup
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# ----------------------------------------------------------------------
# FINAL, COMPLETE TRANSLATIONS DICTIONARY (CRITICAL FOR LANGUAGE FIX)
# ----------------------------------------------------------------------
translations = {
    'en': {
        'app_name': 'Migrant Health Records', 'welcome': 'Welcome to Migrant Health Records', 'search': 'Search', 'add_record': 'Add New Record', 'view': 'View', 'edit': 'Edit', 'delete': 'Delete', 'login': 'Login', 'logout': 'Logout', 'register': 'Register', 'analytics': 'Analytics',
        # Form labels - MUST BE 100% CORRECT FOR TRANSLATION
        'full_name': 'Full Name', 'date_of_birth': 'Date of Birth', 'age': 'Age', 'gender': 'Gender', 'nationality': 'Nationality', 'state_of_origin': 'State of Origin', 'contact_number': 'Contact Number', 'emergency_contact_person': 'Emergency Contact Person', 'emergency_contact_number': 'Emergency Contact Number', 'aadhaar_passport': 'Aadhaar/Passport Number', 'preferred_language': 'Preferred Language', 'literacy_level': 'Literacy Level', 'consent_for_data_sharing': 'Consent for Data Sharing', 'occupation': 'Occupation/Job Role', 'employer_name': 'Employer/Contractor Name', 'employer_contact': 'Employer Contact', 'work_location_district': 'Work Location (District)', 'work_location_pincode': 'Work Location (Pincode)', 'duration_of_stay': 'Duration of Stay in Kerala', 'living_conditions': 'Living Conditions', 'allergies': 'Allergies', 'past_medical_conditions': 'Past Medical Conditions', 'past_surgical_history': 'Past Surgical History', 'family_history': 'Family History', 'immunization_status': 'Immunization Status', 'height_cm': 'Height (cm)', 'weight_kg': 'Weight (kg)', 'blood_group': 'Blood Group', 'vital_signs': 'Vital Signs', 'current_medications': 'Current Medications', 'ongoing_treatment': 'Ongoing Treatment', 'infectious_disease_screening': 'Infectious Disease Screening', 'health_condition': 'Health Condition', 'last_checkup': 'Last Checkup', 'healthcare_facility': 'Healthcare Facility Name', 'doctor_name': 'Doctor/Health Worker Name', 'symptoms_presented': 'Symptoms Presented', 'diagnosis': 'Diagnosis', 'prescriptions_medicines': 'Prescriptions/Medicines Given', 'lab_results': 'Lab Test Results', 'vaccination_records': 'Vaccination Records', 'disease_alerts': 'Disease Alerts', 'contact_tracing_info': 'Contact Tracing Info', 'referral_notes': 'Referral Notes', 'follow_up_date': 'Follow-up Due Date', 'save': 'Save', 'search_by_name': 'Search by Name', 'search_by_gender': 'Search by Gender', 'search_by_health': 'Search by Health', 'search_by_contact': 'Search by Contact', 'search_by_id': 'Search by ID'
    },
    'hi': {
        'app_name': 'प्रवासी स्वास्थ्य रिकॉर्ड', 'welcome': 'प्रवासी स्वास्थ्य रिकॉर्ड में आपका स्वागत है', 'search': 'खोज', 'add_record': 'नया रिकॉर्ड जोड़ें', 'view': 'देखें', 'edit': 'संपादित करें', 'delete': 'हटाएं', 'login': 'लॉगिन', 'logout': 'लॉगआउट', 'register': 'पंजीकरण', 'analytics': 'विश्लेषिकी',
        'full_name': 'पूरा नाम', 'date_of_birth': 'जन्म तिथि', 'age': 'आयु', 'gender': 'लिंग', 'nationality': 'राष्ट्रीयता', 'state_of_origin': 'मूल राज्य', 'contact_number': 'संपर्क संख्या', 'emergency_contact_person': 'आपातकालीन संपर्क व्यक्ति', 'emergency_contact_number': 'आपातकालीन संपर्क संख्या', 'aadhaar_passport': 'आधार/पासपोर्ट संख्या', 'preferred_language': 'पसंदीदा भाषा', 'literacy_level': 'साक्षरता स्तर', 'consent_for_data_sharing': 'डेटा साझा करने के लिए सहमति', 'occupation': 'पेशा/नौकरी', 'employer_name': 'नियोक्ता/ठेकेदार का नाम', 'employer_contact': 'नियोक्ता संपर्क', 'work_location_district': 'कार्यस्थल (जिला)', 'work_location_pincode': 'कार्यस्थल (पिनकोड)', 'duration_of_stay': 'केरल में रहने की अवधि', 'living_conditions': 'रहने की स्थिति', 'allergies': 'एलर्जी', 'past_medical_conditions': 'पिछली चिकित्सा स्थितियाँ', 'past_surgical_history': 'पिछला सर्जिकल इतिहास', 'family_history': 'पारिवारिक इतिहास', 'immunization_status': 'टीकाकरण स्थिति', 'height_cm': 'ऊंचाई (सेमी)', 'weight_kg': 'वजन (किलो)', 'blood_group': 'रक्त समूह', 'vital_signs': 'महत्वपूर्ण संकेत', 'current_medications': 'वर्तमान दवाएं', 'ongoing_treatment': 'चल रहा इलाज', 'infectious_disease_screening': 'संक्रामक रोग स्क्रीनिंग', 'health_condition': 'स्वास्थ्य की स्थिति', 'last_checkup': 'अंतिम जांच', 'healthcare_facility': 'स्वास्थ्य सुविधा का नाम', 'doctor_name': 'डॉक्टर/स्वास्थ्य कार्यकर्ता का नाम', 'symptoms_presented': 'प्रस्तुत लक्षण', 'diagnosis': 'निदान', 'prescriptions_medicines': 'दवाएं/नुस्खे', 'lab_results': 'लैब परीक्षण परिणाम', 'vaccination_records': 'टीकाकरण रिकॉर्ड', 'disease_alerts': 'रोग अलर्ट', 'contact_tracing_info': 'संपर्क ट्रेसिंग जानकारी', 'referral_notes': 'रेफरल नोट्स', 'follow_up_date': 'अनुवर्ती तिथि', 'save': 'सहेजें', 'search_by_name': 'नाम से खोजें', 'search_by_gender': 'लिंग से खोजें', 'search_by_health': 'स्वास्थ्य से खोजें', 'search_by_contact': 'संपर्क से खोजें', 'search_by_id': 'आईडी से खोजें'
    },
    'ml': {
        'app_name': 'കുടിയേറ്റ ആരോഗ്യ രേഖകൾ', 'welcome': 'കുടിയേറ്റ ആരോഗ്യ രേഖകളിലേക്ക് സ്വാഗതം', 'search': 'തിരയുക', 'add_record': 'പുതിയ രേഖ ചേർക്കുക', 'view': 'കാണുക', 'edit': 'എഡിറ്റ് ചെയ്യുക', 'delete': 'ഇല്ലാതാക്കുക', 'login': 'ലോഗിൻ', 'logout': 'ലോഗൗട്ട്', 'register': 'രജിസ്റ്റർ', 'analytics': 'വിശകലനം',
        'full_name': 'പൂർണ്ണമായ പേര്', 'date_of_birth': 'ജനനത്തീയതി', 'age': 'പ്രായം', 'gender': 'ലിംഗഭേദം', 'nationality': 'ദേശീയത', 'state_of_origin': 'സ്വദേശം', 'contact_number': 'ബന്ധപ്പെടാനുള്ള നമ്പർ', 'emergency_contact_person': 'അടിയന്തര ബന്ധപ്പെടാനുള്ള വ്യക്തി', 'emergency_contact_number': 'അടിയന്തര ബന്ധപ്പെടാനുള്ള നമ്പർ', 'aadhaar_passport': 'ആധാർ/പാസ്‌പോർട്ട് നമ്പർ', 'preferred_language': 'ഇഷ്ടപ്പെട്ട ഭാഷ', 'literacy_level': 'സാക്ഷരത നിലവാരം', 'consent_for_data_sharing': 'ഡാറ്റ പങ്കിടുന്നതിനുള്ള അനുമതി', 'occupation': 'തൊഴിൽ', 'employer_name': 'തൊഴിലുടമയുടെ പേര്', 'employer_contact': 'തൊഴിലുടമയുടെ ബന്ധപ്പെടാനുള്ള നമ്പർ', 'work_location_district': 'ജോലിസ്ഥലം (ജില്ല)', 'work_location_pincode': 'ജോലിസ്ഥലം (പിൻകോഡ്)', 'duration_of_stay': 'കേരളത്തിൽ താമസിക്കുന്ന കാലയളവ്', 'living_conditions': 'താമസ സൗകര്യങ്ങൾ', 'allergies': 'അലർജികൾ', 'past_medical_conditions': 'മുൻകാല രോഗങ്ങൾ', 'past_surgical_history': 'മുൻകാല സർജറി ചരിത്രം', 'family_history': 'കുടുംബ ചരിത്രം', 'immunization_status': 'പ്രതിരോധ കുത്തിവയ്പ്പ് നിലവാരം', 'height_cm': 'ഉയരം (സെ.മീ.)', 'weight_kg': 'തൂക്കം (കിലോ.)', 'blood_group': 'രക്തഗ്രൂപ്പ്', 'vital_signs': 'പ്രധാന അടയാളങ്ങൾ', 'current_medications': 'നിലവിലെ മരുന്നുകൾ', 'ongoing_treatment': 'തുടരുന്ന ചികിത്സ', 'infectious_disease_screening': 'സാംക്രമിക രോഗ പരിശോധന', 'health_condition': 'ആരോഗ്യസ്ഥിതി', 'last_checkup': 'അവസാന പരിശോധന', 'healthcare_facility': 'ആരോഗ്യ കേന്ദ്രം', 'doctor_name': 'ഡോക്ടറുടെ/ആരോഗ്യ പ്രവർത്തകന്റെ പേര്', 'symptoms_presented': 'അവതരിപ്പിച്ച ലക്ഷണങ്ങൾ', 'diagnosis': 'രോഗനിർണയം', 'prescriptions_medicines': 'ചികിത്സാ കുറിപ്പുകൾ', 'lab_results': 'ലാബ് പരിശോധനാ ഫലങ്ങൾ', 'vaccination_records': 'വാക്‌സിനേഷൻ രേഖകൾ', 'disease_alerts': 'രോഗ അലേർട്ടുകൾ', 'contact_tracing_info': 'ബന്ധപ്പെടാനുള്ള വിവരങ്ങൾ', 'referral_notes': 'റഫറൽ കുറിപ്പുകൾ', 'follow_up_date': 'തുടർ പരിശോധന തീയതി', 'save': 'സേവ് ചെയ്യുക', 'search_by_name': 'പേര് തിരയുക', 'search_by_gender': 'ലിംഗം തിരയുക', 'search_by_health': 'ആരോഗ്യം തിരയുക', 'search_by_contact': 'ബന്ധപ്പെടാനുള്ള നമ്പർ തിരയുക', 'search_by_id': 'ഐഡി തിരയുക'
    },
    'ta': {
        'app_name': 'புலம்பெயர்ந்தோர் சுகாதார பதிவுகள்', 'welcome': 'புலம்பெயர்ந்தோர் சுகாதார பதிவுகளுக்கு வரவேற்கிறோம்', 'search': 'தேடு', 'add_record': 'புதிய பதிவைச் சேர்க்கவும்', 'view': 'பார்க்க', 'edit': 'திருத்து', 'delete': 'அழி', 'login': 'உள்நுழைய', 'logout': 'வெளியேறு', 'register': 'பதிவு செய்யுங்கள்', 'analytics': 'பகுப்பாய்வு',
        'full_name': 'முழு பெயர்', 'date_of_birth': 'பிறந்த தேதி', 'age': 'வயது', 'gender': 'பாலினம்', 'nationality': 'தேசிய இனத்தவர்', 'state_of_origin': 'சொந்த மாநிலம்', 'contact_number': 'தொடர்பு எண்', 'emergency_contact_person': 'அவசர தொடர்பு நபர்', 'emergency_contact_number': 'அவசர தொடர்பு எண்', 'aadhaar_passport': 'ஆதார்/கடவுச்சீட்டு எண்', 'preferred_language': 'விருப்பமான மொழி', 'literacy_level': 'கல்வி நிலை', 'consent_for_data_sharing': 'தரவு பகிர்வுக்கான ஒப்புதல்', 'occupation': 'தொழில்', 'employer_name': 'வேலை செய்யும் இடம்', 'employer_contact': 'வேலை செய்யும் இடத்தின் தொடர்பு', 'work_location_district': 'பணிபுரியும் இடம் (மாவட்டம்)', 'work_location_pincode': 'பணிபுரியும் இடம் (PIN)', 'duration_of_stay': 'கேரளாவில் தங்கிய காலம்', 'living_conditions': 'தங்கும் நிலை', 'allergies': 'ஒவ்வாமை', 'past_medical_conditions': 'முந்தைய மருத்துவ நிலைகள்', 'past_surgical_history': 'முந்தைய அறுவை சிகிச்சை வரலாறு', 'family_history': 'குடும்ப வரலாறு', 'immunization_status': 'நோய் எதிர்ப்பு நிலை', 'height_cm': 'உயரம் (செ.மீ.)', 'weight_kg': 'எடை (கி.கி.)', 'blood_group': 'இரத்த வகை', 'vital_signs': 'முக்கிய அறிகுறிகள்', 'current_medications': 'தற்போதைய மருந்துகள்', 'ongoing_treatment': 'தொடர் சிகிச்சை', 'infectious_disease_screening': 'தொற்றுநோய் ஸ்கிரீனிங்', 'health_condition': 'ஆரோக்கிய நிலை', 'last_checkup': 'கடைசி சோதனை', 'healthcare_facility': 'சுகாதார வசதியின் பெயர்', 'doctor_name': 'மருத்துவர்/சுகாதார பணியாளர் பெயர்', 'symptoms_presented': 'அறிகுறிகள்', 'diagnosis': 'நோய் கண்டறிதல்', 'prescriptions_medicines': 'மருந்துகள்', 'lab_results': 'ஆய்வக முடிவுகள்', 'vaccination_records': 'தடுப்பூசி பதிவுகள்', 'disease_alerts': 'நோய் எச்சரிக்கைகள்', 'contact_tracing_info': 'தொடர்பு தடமறிதல் தகவல்', 'referral_notes': 'பரிந்துரை குறிப்புகள்', 'follow_up_date': 'தொடர் தேதி', 'save': 'சேமி', 'search_by_name': 'பெயர் தேடு', 'search_by_gender': 'பாலினம் தேடு', 'search_by_health': 'ஆரோக்கியம் தேடு', 'search_by_contact': 'தொடர்பு தேடு', 'search_by_id': 'ஐடி தேடு'
    },
    'bn': {
        'app_name': 'অভিবাসী স্বাস্থ্য রেকর্ড', 'welcome': 'অভিবাসী স্বাস্থ্য রেকর্ডে স্বাগতম', 'search': 'অনুসন্ধান', 'add_record': 'নতুন রেকর্ড যোগ করুন', 'view': 'দেখুন', 'edit': 'সম্পাদনা করুন', 'delete': 'মুছুন', 'login': 'লগইন', 'logout': 'লগআউট', 'register': 'নিবন্ধন', 'analytics': 'বিশ্লেষণ',
        'full_name': 'পূর্ণ নাম', 'date_of_birth': 'জন্ম তারিখ', 'age': 'বয়স', 'gender': 'লিঙ্গ', 'nationality': 'জাতীয়তা', 'state_of_origin': 'উৎপত্তি রাজ্য', 'contact_number': 'যোগাযোগ নম্বর', 'emergency_contact_person': 'জরুরি যোগাযোগ ব্যক্তি', 'emergency_contact_number': 'জরুরি যোগাযোগ নম্বর', 'aadhaar_passport': 'আধার/পাসপোর্ট নম্বর', 'preferred_language': 'পছন্দের ভাষা', 'literacy_level': 'সাক্ষরতার স্তর', 'consent_for_data_sharing': 'ডেটা শেয়ার করার জন্য সম্মতি', 'occupation': 'পেশা', 'employer_name': 'নিয়োগকর্তার নাম', 'employer_contact': 'নিয়োগকর্তার যোগাযোগ', 'work_location_district': 'কাজের অবস্থান (জেলা)', 'work_location_pincode': 'কাজের অবস্থান (পিনকোড)', 'duration_of_stay': 'কেরালাতে থাকার সময়কাল', 'living_conditions': 'জীবনযাত্রার অবস্থা', 'allergies': 'অ্যালার্জি', 'past_medical_conditions': 'অতীতের চিকিৎসার অবস্থা', 'past_surgical_history': 'অতীতের সার্জারীর ইতিহাস', 'family_history': 'পারিবারিক ইতিহাস', 'immunization_status': 'টিকাদান অবস্থা', 'height_cm': 'উচ্চতা (সেমি)', 'weight_kg': 'ওজন (কেজি)', 'blood_group': 'রক্তের গ্রুপ', 'vital_signs': 'গুরুত্বপূর্ণ লক্ষণ', 'current_medications': 'বর্তমান ঔষধ', 'ongoing_treatment': 'চলমান চিকিৎসা', 'infectious_disease_screening': 'সংক্রামক রোগের স্ক্রিনিং', 'health_condition': 'স্বাস্থ্য অবস্থা', 'last_checkup': 'শেষ চেকআপ', 'healthcare_facility': 'স্বাস্থ্য সুবিধার নাম', 'doctor_name': 'ডাক্তার/স্বাস্থ্য কর্মীর নাম', 'symptoms_presented': 'উপস্থাপিত লক্ষণ', 'diagnosis': 'রোগ নির্ণয়', 'prescriptions_medicines': 'প্রেসক্রিপশন/ঔষধ', 'lab_results': 'ল্যাব পরীক্ষার ফলাফল', 'vaccination_records': 'টিকাকরণের রেকর্ড', 'disease_alerts': 'রোগ সতর্কতা', 'contact_tracing_info': 'যোগাযোগ ট্রেসিং তথ্য', 'referral_notes': 'রেফারেল নোট', 'follow_up_date': 'ফলো-আপ তারিখ', 'save': 'সংরক্ষণ করুন', 'search_by_name': 'নাম অনুসন্ধান', 'search_by_gender': 'লিঙ্গ অনুসন্ধান', 'search_by_health': 'স্বাস্থ্য অনুসন্ধান', 'search_by_contact': 'যোগাযোগ অনুসন্ধান', 'search_by_id': 'আইডি অনুসন্ধান'
    }
}

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize DB + Migration
db.init_app(app)
migrate = Migrate(app, db)

# Initialize Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Ensure tables exist (quick fix if migrations are not run)
with app.app_context():
    try:
        db.create_all()
    except Exception:
        # Ignore error if tables already exist or if app is not fully configured yet
        pass

# Set default language
app.config['DEFAULT_LANGUAGE'] = 'en'

# Decorator definition
def admin_required(f):
    """Decorator for routes that require admin access."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('You need admin privileges to access this page.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Context processor (remains the same)
@app.context_processor
def inject_translations():
    lang = session.get('language', app.config['DEFAULT_LANGUAGE'])
    return dict(t=translations.get(lang, translations['en']))

# Route to change language (remains the same)
@app.route("/language/<lang_code>")
def change_language(lang_code):
    if lang_code in translations:
        session['language'] = lang_code
    else:
        session['language'] = app.config['DEFAULT_LANGUAGE']
    return redirect(request.referrer or url_for('index'))

@app.route("/analytics")
@login_required
def analytics():
    """Analytics dashboard for migrant health data"""
    analytics_data = get_analytics_data()
    return render_template(
        "analytics.html",
        title="Analytics Dashboard",
        analytics=analytics_data
    )

# Analytics helper functions (remains the same)
def get_analytics_data():
    """Generate analytics data for the dashboard"""
    analytics = {}
    analytics['total_migrants'] = Migrant.query.count()
    gender_data = db.session.query(
        Migrant.gender, 
        db.func.count(Migrant.id)
    ).group_by(Migrant.gender).all()
    analytics['gender_distribution'] = {
        'labels': [g[0] if g[0] else 'Unknown' for g in gender_data],
        'data': [g[1] for g in gender_data]
    }
    nationality_data = db.session.query(
        Migrant.nationality, 
        db.func.count(Migrant.id)
    ).group_by(Migrant.nationality).order_by(db.func.count(Migrant.id).desc()).limit(5).all()
    analytics['nationality_distribution'] = {
        'labels': [n[0] if n[0] else 'Unknown' for n in nationality_data],
        'data': [n[1] for n in nationality_data]
    }
    health_data = db.session.query(
        Migrant.health_condition, 
        db.func.count(Migrant.id)
    ).group_by(Migrant.health_condition).all()
    analytics['health_distribution'] = {
        'labels': [h[0] if h[0] else 'Unknown' for h in health_data],
        'data': [h[1] for h in health_data]
    }
    age_ranges = [
        ('0-18', 0, 18),
        ('19-30', 19, 30),
        ('31-45', 31, 45),
        ('46-60', 46, 60),
        ('60+', 61, 200)
    ]
    age_data = []
    age_labels = []
    for label, min_age, max_age in age_ranges:
        count = Migrant.query.filter(Migrant.age >= min_age, Migrant.age <= max_age).count()
        age_data.append(count)
        age_labels.append(label)
    analytics['age_distribution'] = {
        'labels': age_labels,
        'data': age_data
    }
    occupation_data = db.session.query(
        Migrant.occupation, 
        db.func.count(Migrant.id)
    ).group_by(Migrant.occupation).order_by(db.func.count(Migrant.id).desc()).limit(5).all()
    analytics['occupation_distribution'] = {
        'labels': [o[0] if o[0] else 'Unknown' for o in occupation_data],
        'data': [o[1] for o in occupation_data]
    }
    return analytics

# User loader (remains the same)
@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login."""
    return User.query.get(int(user_id))

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    search_form = SearchForm()
    query = Migrant.query
    search_term = request.args.get('q') or (search_form.search_term.data if request.method == 'POST' and search_form.validate_on_submit() else None)
    filter_by = request.args.get('by') or (search_form.filter_by.data if request.method == 'POST' and search_form.validate_on_submit() else None)
    if search_term:
        if filter_by == "name":
            query = query.filter(Migrant.name.ilike(f"%{search_term}%"))
        elif filter_by == "gender":
            query = query.filter(Migrant.gender.ilike(f"%{search_term}%"))
        elif filter_by == "health_condition":
            query = query.filter(Migrant.health_condition.ilike(f"%{search_term}%"))
        elif filter_by == "contact":
            query = query.filter(Migrant.contact.ilike(f"%{search_term}%"))
        elif filter_by == "id":
            try:
                query = query.filter(Migrant.id == int(search_term))
            except ValueError:
                query = query.filter(False)
    migrants = query.order_by(Migrant.id.desc()).all()
    return render_template("index.html", migrants=migrants, search_form=search_form)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        # Hardcoded admin login for quick testing (as requested)
        if form.username.data == "Admin" and form.password.data == "admin@123":
            user = User.query.filter_by(username="Admin").first()
            if not user:
                # Create the Admin user if it doesn't exist
                user = User(username="Admin", email="admin@example.com", role="admin")
                user.set_password("admin@123")
                db.session.add(user)
                db.session.commit()
            flash(f"Welcome back, {user.username}!", "success")
            login_user(user)
        else:
            # Check database for registered user (healthcare workers)
            user = User.query.filter_by(username=form.username.data).first()
            if user is None or not user.check_password(form.password.data):
                flash("Invalid username or password", "danger")
                return redirect(url_for("login"))
            login_user(user)
            flash(f"Welcome back, {user.username}!", "success")
            
        next_page = request.args.get("next")
        if not next_page or not next_page.startswith("/"):
            next_page = url_for("index")
        return redirect(next_page)
        
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, role=form.role.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f"User {form.username.data} has been registered!", "success")
        return redirect(url_for("index"))
    return render_template("register.html", form=form)

# Add route (fixed to use WTForms data directly)
@app.route("/add", methods=["GET", "POST"])
@login_required
def add_migrant():
    form = MigrantForm()
    if form.validate_on_submit():
        try:
            # Data conversion is handled safely by WTForms FloatField/DateField now
            migrant = Migrant(
                name=form.name.data,
                age=form.age.data,
                gender=form.gender.data,
                date_of_birth=form.date_of_birth.data,
                nationality=form.nationality.data,
                state_of_origin=form.state_of_origin.data,
                contact=form.contact.data,
                emergency_contact_name=form.emergency_contact_name.data,
                emergency_contact_number=form.emergency_contact_number.data,
                aadhaar_passport=form.aadhaar_passport.data,
                preferred_language=form.preferred_language.data,
                literacy_level=form.literacy_level.data,
                data_sharing_consent=form.data_sharing_consent.data, # Boolean field data is boolean
                occupation=form.occupation.data,
                employer_name=form.employer_name.data,
                employer_contact=form.employer_contact.data,
                work_location_district=form.work_location_district.data,
                work_location_pincode=form.work_location_pincode.data,
                duration_of_stay=form.duration_of_stay.data,
                living_conditions=form.living_conditions.data,
                allergies=form.allergies.data,
                past_medical_conditions=form.past_medical_conditions.data,
                past_surgical_history=form.past_surgical_history.data,
                family_history=form.family_history.data,
                immunization_status=form.immunization_status.data,
                height=form.height.data, # FloatField gives None/Float
                weight=form.weight.data, # FloatField gives None/Float
                blood_group=form.blood_group.data,
                vital_signs=form.vital_signs.data,
                current_medications=form.current_medications.data,
                ongoing_treatment=form.ongoing_treatment.data,
                infectious_disease_screening=form.infectious_disease_screening.data,
                health_condition=form.health_condition.data,
                last_checkup=form.last_checkup.data,
                healthcare_facility=form.healthcare_facility.data,
                doctor_name=form.doctor_name.data,
                symptoms=form.symptoms.data,
                diagnosis=form.diagnosis.data,
                prescriptions=form.prescriptions.data,
                lab_results=form.lab_results.data,
                vaccination_records=form.vaccination_records.data,
                disease_alerts=form.disease_alerts.data,
                contact_tracing_info=form.contact_tracing_info.data,
                referral_notes=form.referral_notes.data,
                follow_up_date=form.follow_up_date.data,
            )
            if migrant.height and migrant.weight:
                migrant.calculate_bmi()
            db.session.add(migrant)
            db.session.commit()
            flash("Migrant record added successfully!", "success")
            return redirect(url_for("index"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error adding migrant record: {str(e)}", "danger")
            # print(e) # You can uncomment this line to debug specific SQL/DB errors
            
    return render_template("add_migrant.html", form=form, title="Add Migrant")

# Edit route (fixed to use WTForms data directly)
@app.route("/edit/<int:migrant_id>", methods=["GET", "POST"])
@login_required
def edit_migrant(migrant_id):
    migrant = Migrant.query.get_or_404(migrant_id)
    form = MigrantForm(obj=migrant)
    if form.validate_on_submit():
        try:
            migrant.name = form.name.data
            migrant.age = form.age.data
            migrant.gender = form.gender.data
            migrant.date_of_birth = form.date_of_birth.data
            migrant.nationality = form.nationality.data
            migrant.state_of_origin = form.state_of_origin.data
            migrant.contact = form.contact.data
            migrant.emergency_contact_name = form.emergency_contact_name.data
            migrant.emergency_contact_number = form.emergency_contact_number.data
            migrant.aadhaar_passport = form.aadhaar_passport.data
            migrant.preferred_language = form.preferred_language.data
            migrant.literacy_level = form.literacy_level.data
            migrant.data_sharing_consent = form.data_sharing_consent.data
            migrant.occupation = form.occupation.data
            migrant.employer_name = form.employer_name.data
            migrant.employer_contact = form.employer_contact.data
            migrant.work_location_district = form.work_location_district.data
            migrant.work_location_pincode = form.work_location_pincode.data
            migrant.duration_of_stay = form.duration_of_stay.data
            migrant.living_conditions = form.living_conditions.data
            migrant.allergies = form.allergies.data
            migrant.past_medical_conditions = form.past_medical_conditions.data
            migrant.past_surgical_history = form.past_surgical_history.data
            migrant.family_history = form.family_history.data
            migrant.immunization_status = form.immunization_status.data
            migrant.height = form.height.data
            migrant.weight = form.weight.data
            migrant.blood_group = form.blood_group.data
            migrant.vital_signs = form.vital_signs.data
            migrant.current_medications = form.current_medications.data
            migrant.ongoing_treatment = form.ongoing_treatment.data
            migrant.infectious_disease_screening = form.infectious_disease_screening.data
            migrant.health_condition = form.health_condition.data
            migrant.last_checkup = form.last_checkup.data
            migrant.healthcare_facility = form.healthcare_facility.data
            migrant.doctor_name = form.doctor_name.data
            migrant.symptoms = form.symptoms.data
            migrant.diagnosis = form.diagnosis.data
            migrant.prescriptions = form.prescriptions.data
            migrant.lab_results = form.lab_results.data
            migrant.vaccination_records = form.vaccination_records.data
            migrant.disease_alerts = form.disease_alerts.data
            migrant.contact_tracing_info = form.contact_tracing_info.data
            migrant.referral_notes = form.referral_notes.data
            migrant.follow_up_date = form.follow_up_date.data
            if migrant.height and migrant.weight:
                migrant.calculate_bmi()
            db.session.commit()
            flash("Migrant record updated successfully!", "success")
            return redirect(url_for("index"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error updating migrant record: {str(e)}", "danger")
    return render_template("edit_migrant.html", form=form, migrant=migrant, title="Edit Migrant")

@app.route("/view/<int:migrant_id>")
@login_required
def view_migrant(migrant_id):
    migrant = Migrant.query.get_or_404(migrant_id)
    qr_code_url = url_for('get_migrant_qr', migrant_id=migrant.id, _external=True)
    return render_template("view_migrant.html", migrant=migrant, title="View Migrant", qr_code_url=qr_code_url)

@app.route("/qrcode/<int:migrant_id>")
@login_required
def get_migrant_qr(migrant_id):
    migrant = Migrant.query.get_or_404(migrant_id)
    qr_data = f"ID: {migrant.id}\nName: {migrant.name}\nAge: {migrant.age}\nGender: {migrant.gender}"
    if migrant.contact:
        qr_data += f"\nContact: {migrant.contact}"
    if migrant.health_condition:
        qr_data += f"\nHealth Status: {migrant.health_condition}"
    if migrant.blood_group:
        qr_data += f"\nBlood Group: {migrant.blood_group}"
    view_url = url_for('view_migrant', migrant_id=migrant.id, _external=True)
    qr_data += f"\n\nView full record: {view_url}"
    img = qrcode.make(qr_data)
    buffer = io.BytesIO()
    img.save(buffer, 'PNG')
    buffer.seek(0)
    return send_file(buffer, mimetype='image/png')

@app.route("/__debug_paths")
def __debug_paths():
    return {
        "BASE_DIR": BASE_DIR,
        "template_folder": app.template_folder,
        "static_folder": app.static_folder,
        "cwd": os.getcwd(),
        "templates_list": os.listdir(app.template_folder) if os.path.isdir(app.template_folder) else "missing",
    }