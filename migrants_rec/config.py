"""Configuration settings for the Migrant Health Records application."""

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "your_secret_key_here"  # CHANGE THIS FOR DEPLOYMENT
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "migrant_records.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False