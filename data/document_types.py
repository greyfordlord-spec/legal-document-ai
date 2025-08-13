from typing import Dict, List, Any
from config.settings import DOCUMENT_TYPES

# Questions and field definitions for each document type
DOCUMENT_QUESTIONS = {
    "residential_lease": [
        {
            "id": "landlord_name",
            "question": "What is the landlord's full name?",
            "type": "text",
            "required": True
        },
        {
            "id": "tenant_name",
            "question": "What is the tenant's full name?",
            "type": "text",
            "required": True
        },
        {
            "id": "property_address",
            "question": "What is the property address?",
            "type": "text",
            "required": True
        },
        {
            "id": "rent_amount",
            "question": "What is the monthly rent amount? (Enter amount and currency, e.g., 1500 USD)",
            "type": "text",
            "required": True
        },
        {
            "id": "security_deposit",
            "question": "What is the security deposit amount? (Enter amount and currency, e.g., 2000 USD)",
            "type": "text",
            "required": True
        },
        {
            "id": "lease_start_date",
            "question": "When does the lease start? (Enter 'today' or a specific date like 2024-01-15)",
            "type": "date",
            "required": True
        },
        {
            "id": "lease_end_date",
            "question": "When does the lease end? (Enter a specific date like 2024-12-31)",
            "type": "date",
            "required": True
        },
        {
            "id": "utilities_included",
            "question": "Are utilities included in the rent? (yes/no)",
            "type": "boolean",
            "required": True
        },
        {
            "id": "pets_allowed",
            "question": "Are pets allowed? (yes/no)",
            "type": "boolean",
            "required": True
        },
        {
            "id": "target_country",
            "question": "What country is this lease for? (e.g., 'United States', 'Germany', 'United Kingdom', 'Spain') - This helps me localize the document for your jurisdiction",
            "type": "text",
            "required": True
        }
    ],
    "nda": [
        {
            "id": "disclosing_party",
            "question": "What is the name of the company/person sharing confidential information?",
            "type": "text",
            "required": True
        },
        {
            "id": "receiving_party",
            "question": "What is the name of the company/person receiving confidential information?",
            "type": "text",
            "required": True
        },
        {
            "id": "confidential_information",
            "question": "What type of confidential information will be shared? (e.g., business plans, customer data, trade secrets, technical specifications)",
            "type": "text",
            "required": True
        },
        {
            "id": "purpose",
            "question": "What is the business purpose of sharing this information? (e.g., potential partnership, service evaluation, due diligence)",
            "type": "text",
            "required": True
        },
        {
            "id": "effective_date",
            "question": "When should this NDA become effective? (Enter 'today' or a specific date like 2024-01-15)",
            "type": "date",
            "required": True
        },
        {
            "id": "duration",
            "question": "How long should the confidentiality obligations last? (e.g., '5 years', '10 years', 'indefinitely')",
            "type": "text",
            "required": True
        },
        {
            "id": "target_country",
            "question": "What country is this NDA for? (e.g., 'United States', 'Germany', 'United Kingdom', 'Spain') - This helps me localize the document for your jurisdiction",
            "type": "text",
            "required": True
        }
    ],
    "b2b_contract": {
        "EN": [
            {
                "id": "client_name",
                "question": "What is the client's company name?",
                "type": "text",
                "required": True
            },
            {
                "id": "service_provider_name",
                "question": "What is the service provider's company name?",
                "type": "text",
                "required": True
            },
            {
                "id": "service_description",
                "question": "What services will be provided? (Describe the main services in detail)",
                "type": "text",
                "required": True
            },
            {
                "id": "contract_value",
                "question": "What is the total contract value? (Enter the amount in currency, e.g., 50000 USD)",
                "type": "text",
                "required": True
            },
            {
                "id": "payment_terms",
                "question": "What are the payment terms? (e.g., '50% upfront, 50% upon completion', 'net 30 days', 'monthly installments')",
                "type": "text",
                "required": True
            },
            {
                "id": "start_date",
                "question": "When does the contract start? (Enter 'today' or a specific date like 2024-01-15)",
                "type": "date",
                "required": True
            },
            {
                "id": "end_date",
                "question": "When does the contract end? (Enter a specific date like 2024-12-31 or 'ongoing')",
                "type": "date",
                "required": True
            }
        ],
        "DE": [
            {
                "id": "client_name",
                "question": "Wie lautet der Firmenname des Kunden?",
                "type": "text",
                "required": True
            },
            {
                "id": "service_provider_name",
                "question": "Wie lautet der Firmenname des Dienstleisters?",
                "type": "text",
                "required": True
            },
            {
                "id": "service_description",
                "question": "Welche Dienstleistungen werden erbracht? (Beschreiben Sie die Hauptdienstleistungen im Detail)",
                "type": "text",
                "required": True
            },
            {
                "id": "contract_value",
                "question": "Wie hoch ist der Gesamtwert des Vertrags? (Geben Sie den Betrag in Währung ein, z.B. 50000 EUR)",
                "type": "text",
                "required": True
            },
            {
                "id": "payment_terms",
                "question": "Wie lauten die Zahlungsbedingungen? (z.B. '50% im Voraus, 50% bei Fertigstellung', 'netto 30 Tage', 'monatliche Raten')",
                "type": "text",
                "required": True
            },
            {
                "id": "start_date",
                "question": "Wann beginnt der Vertrag? (Geben Sie 'heute' oder ein spezifisches Datum wie 2024-01-15 ein)",
                "type": "date",
                "required": True
            },
            {
                "id": "end_date",
                "question": "Wann endet der Vertrag? (Geben Sie ein spezifisches Datum wie 2024-12-31 oder 'laufend' ein)",
                "type": "date",
                "required": True
            }
        ]
    },
    "nda": [
        {
            "id": "disclosing_party",
            "question": "What is the name of the company/person sharing confidential information?",
            "type": "text",
            "required": True
        },
        {
            "id": "receiving_party",
            "question": "What is the name of the company/person receiving confidential information?",
            "type": "text",
            "required": True
        },
        {
            "id": "confidential_information",
            "question": "What type of confidential information will be shared? (e.g., business plans, customer data, trade secrets, technical specifications)",
            "type": "text",
            "required": True
        },
        {
            "id": "purpose",
            "question": "What is the business purpose of sharing this information? (e.g., potential partnership, service evaluation, due diligence)",
            "type": "text",
            "required": True
        },
        {
            "id": "effective_date",
            "question": "When should this NDA become effective? (Enter 'today' or a specific date like 2024-01-15)",
            "type": "date",
            "required": True
        },
        {
            "id": "duration",
            "question": "How long should the confidentiality obligations last? (e.g., '5 years', '10 years', 'indefinitely')",
            "type": "text",
            "required": True
        },
        {
            "id": "target_country",
            "question": "What country is this NDA for? (e.g., 'United States', 'Germany', 'United Kingdom', 'Spain') - This helps me localize the document for your jurisdiction",
            "type": "text",
            "required": True
        }
    ],
    "power_of_attorney": [
        {
            "id": "principal_name",
            "question": "What is the full name of the principal (the person granting the power)?",
            "type": "text",
            "required": True
        },
        {
            "id": "agent_name",
            "question": "What is the full name of the agent (the person receiving the power)?",
            "type": "text",
            "required": True
        },
        {
            "id": "power_type",
            "question": "What type of power of attorney is this? (e.g., 'general', 'limited', 'durable', 'healthcare')",
            "type": "text",
            "required": True
        },
        {
            "id": "effective_date",
            "question": "When should this power of attorney become effective? (Enter 'today' or a specific date like 2024-01-15)",
            "type": "date",
            "required": True
        },
        {
            "id": "expiration_date",
            "question": "When should this power of attorney expire? (Enter a specific date like 2024-12-31 or 'never')",
            "type": "date",
            "required": True
        },
        {
            "id": "specific_powers",
            "question": "What specific powers are being granted? (e.g., 'financial decisions', 'healthcare decisions', 'real estate transactions')",
            "type": "text",
            "required": True
        },
        {
            "id": "target_country",
            "question": "What country is this power of attorney for? (e.g., 'United States', 'Germany', 'United Kingdom', 'Spain') - This helps me localize the document for your jurisdiction",
            "type": "text",
            "required": True
        }
    ],
    "employment_contract": [
        {
            "id": "employee_name",
            "question": "What is the full name of the employee?",
            "type": "text",
            "required": True
        },
        {
            "id": "employer_name",
            "question": "What is the name of the employer/company?",
            "type": "text",
            "required": True
        },
        {
            "id": "job_title",
            "question": "What is the employee's job title? (e.g., 'Software Engineer', 'Marketing Manager', 'Sales Representative')",
            "type": "text",
            "required": True
        },
        {
            "id": "start_date",
            "question": "When does the employment start? (Enter 'today' or a specific date like 2024-01-15)",
            "type": "date",
            "required": True
        },
        {
            "id": "salary",
            "question": "What is the annual salary? (Enter the amount in currency, e.g., 75000 USD)",
            "type": "text",
            "required": True
        },
        {
            "id": "work_schedule",
            "question": "What is the work schedule? (e.g., '40 hours per week', '9 AM to 5 PM Monday-Friday', 'flexible hours')",
            "type": "text",
            "required": True
        },
        {
            "id": "probation_period",
            "question": "What is the probation period? (e.g., '3 months', '6 months', '90 days')",
            "type": "text",
            "required": True
        },
        {
            "id": "target_country",
            "question": "What country is this employment contract for? (e.g., 'United States', 'Germany', 'United Kingdom', 'Spain') - This helps me localize the document for your jurisdiction",
            "type": "text",
            "required": True
        }
    ],
    "meeting_minutes": [
        {
            "id": "meeting_title",
            "question": "What is the title/purpose of the meeting? (e.g., 'Board of Directors Meeting', 'Project Review', 'Quarterly Planning')",
            "type": "text",
            "required": True
        },
        {
            "id": "meeting_date",
            "question": "When did the meeting take place? (Enter 'today' or a specific date like 2024-01-15)",
            "type": "date",
            "required": True
        },
        {
            "id": "meeting_time",
            "question": "What time did the meeting start and end? (e.g., '2:00 PM to 4:00 PM', '09:00 to 11:30')",
            "type": "text",
            "required": True
        },
        {
            "id": "attendees",
            "question": "Who attended the meeting? (List names separated by commas, e.g., 'John Smith, Jane Doe, Mike Johnson' or 'Board of Directors')",
            "type": "text",
            "required": True
        },
        {
            "id": "chairperson",
            "question": "Who chaired/led the meeting? (Enter the name of the meeting leader)",
            "type": "text",
            "required": True
        },
        {
            "id": "key_decisions",
            "question": "What key decisions were made during the meeting? (Summarize the main decisions and outcomes)",
            "type": "text",
            "required": True
        },
        {
            "id": "next_meeting",
            "question": "When is the next meeting scheduled? (Enter a specific date like 2024-02-15 or 'TBD' if not scheduled)",
            "type": "date",
            "required": True
        },
        {
            "id": "target_country",
            "question": "What country is this meeting for? (e.g., 'United States', 'Germany', 'United Kingdom', 'Spain') - This helps me localize the document for your jurisdiction",
            "type": "text",
            "required": True
        }
    ]
}

def get_document_questions(document_type: str, language: str = "EN") -> List[Dict[str, Any]]:
    """Get questions for a specific document type and language."""
    # Now all document types use English questions by default
    return DOCUMENT_QUESTIONS.get(document_type, [])

def get_document_type_info(document_type: str, language: str = "EN") -> Dict[str, str]:
    """Get document type information for a specific language."""
    doc_info = DOCUMENT_TYPES.get(document_type, {})
    return {
        "name": doc_info.get("name", document_type),
        "description": doc_info.get("description", ""),
        "localization_support": doc_info.get("localization_support", [])
    }

def get_all_document_types(language: str = "EN") -> Dict[str, Dict[str, str]]:
    """Get all document types with their names and descriptions for a specific language."""
    result = {}
    for doc_type, doc_info in DOCUMENT_TYPES.items():
        result[doc_type] = {
            "name": doc_info["name"],
            "description": doc_info["description"],
            "localization_support": doc_info.get("localization_support", [])
        }
    return result
