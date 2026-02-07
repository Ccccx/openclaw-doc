#!/usr/bin/env python3
"""
Health Manager Skill - Initialization Script
Sets up the necessary directory structure and default configurations.
"""

import os
import json
import datetime

# Define the health data directory path
HEALTH_DATA_DIR = os.path.expanduser("~/.moltbot/health_data")

def create_health_directories():
    """Create the necessary directory structure for health data."""
    directories = [
        HEALTH_DATA_DIR,
        os.path.join(HEALTH_DATA_DIR, "profiles"),
        os.path.join(HEALTH_DATA_DIR, "records"),
        os.path.join(HEALTH_DATA_DIR, "reports"),
        os.path.join(HEALTH_DATA_DIR, "logs")
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")

def create_default_config():
    """Create a default configuration file."""
    config_path = os.path.join(HEALTH_DATA_DIR, "config.json")
    
    if not os.path.exists(config_path):
        default_config = {
            "version": "1.0",
            "created_at": datetime.datetime.now().isoformat(),
            "privacy_level": "high",  # high, medium, low
            "data_retention_days": 365,
            "backup_enabled": True,
            "backup_frequency_days": 7,
            "units": {
                "weight": "kg",  # kg or lbs
                "height": "cm",  # cm or inches
                "temperature": "celsius"  # celsius or fahrenheit
            }
        }
        
        with open(config_path, 'w') as f:
            json.dump(default_config, f, indent=2)
        print(f"Created default config: {config_path}")

def create_sample_profile():
    """Create a sample profile template."""
    profile_template = {
        "personal_info": {
            "name": "",
            "age": None,
            "gender": "",
            "height": None,
            "weight": None,
            "blood_type": "",
            "allergies": [],
            "chronic_conditions": [],
            "medications": []
        },
        "emergency_contacts": [],
        "health_goals": [],
        "last_updated": datetime.datetime.now().isoformat()
    }
    
    template_path = os.path.join(HEALTH_DATA_DIR, "profiles", "template.json")
    if not os.path.exists(template_path):
        with open(template_path, 'w') as f:
            json.dump(profile_template, f, indent=2)
        print(f"Created profile template: {template_path}")

if __name__ == "__main__":
    print("Initializing Health Manager Skill...")
    create_health_directories()
    create_default_config()
    create_sample_profile()
    print("Health Manager Skill initialization complete!")