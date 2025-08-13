import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))

# Application Settings
DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "EN")  # EN or DE
MAX_CONVERSATION_LENGTH = int(os.getenv("MAX_CONVERSATION_LENGTH", "50"))

# Document Export Settings
DEFAULT_EXPORT_FORMAT = os.getenv("DEFAULT_EXPORT_FORMAT", "docx")  # docx or pdf
EXPORT_FOLDER = os.getenv("EXPORT_FOLDER", "exports")

# UI Settings
STREAMLIT_THEME = {
    "primaryColor": "#3b82f6",  # Bright blue
    "backgroundColor": "#0f172a",  # Dark blue-black
    "secondaryBackgroundColor": "#1e293b",  # Darker blue-gray
    "textColor": "#ffffff",  # Pure white
    "font": "Inter, system-ui, sans-serif"
}

# Supported Languages
SUPPORTED_LANGUAGES = {
    "EN": "English",
    "DE": "Deutsch", 
    "ES": "Español",
    "PT": "Português",
    "PL": "Polski",
    "UK": "Українська",
    "AR": "العربية",
    "TR": "Türkçe"
}

# Document Types Configuration
DOCUMENT_TYPES = {
    "residential_lease": {
        "name": "Residential Lease Agreement",
        "description": "Standard residential lease agreement with all necessary clauses",
        "localization_support": ["DE", "US", "UK", "ES", "FR", "IT", "PL", "UK", "CA", "AU"]
    },
    "nda": {
        "name": "Non-Disclosure Agreement (NDA)",
        "description": "Confidentiality agreement for business relationships",
        "localization_support": ["DE", "US", "UK", "ES", "FR", "IT", "PL", "UK", "CA", "AU", "JP", "SG"]
    },
    "b2b_contract": {
        "name": "Business-to-Business Contract",
        "description": "Professional service and partnership agreements",
        "localization_support": ["DE", "US", "UK", "ES", "FR", "IT", "PL", "UK", "CA", "AU", "BR", "MX"]
    },
    "power_of_attorney": {
        "name": "Power of Attorney",
        "description": "Legal authorization documents",
        "localization_support": ["DE", "US", "UK", "ES", "FR", "IT", "PL", "UK", "CA", "AU"]
    },
    "employment_contract": {
        "name": "Employment Contract",
        "description": "Standard employment agreements",
        "localization_support": ["DE", "US", "UK", "ES", "FR", "IT", "PL", "UK", "CA", "AU", "BR", "MX"]
    },
    "meeting_minutes": {
        "name": "Meeting Minutes / Resolutions",
        "description": "Corporate meeting documentation",
        "localization_support": ["DE", "US", "UK", "ES", "FR", "IT", "PL", "UK", "CA", "AU"]
    }
}
