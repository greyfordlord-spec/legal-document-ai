from typing import Dict, Any, Optional
from jinja2 import Environment, FileSystemLoader, Template
import os

class DocumentGenerator:
    """Generates legal documents using templates and collected data."""
    
    def __init__(self):
        """Initialize document generator with template environment."""
        # Set up Jinja2 environment
        template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates', 'document_templates')
        self.env = Environment(loader=FileSystemLoader(template_dir))
        
        # Document templates (fallback if files don't exist)
        self.templates = {
            "residential_lease": {
                "EN": self._get_residential_lease_template_en(),
                "DE": self._get_residential_lease_template_de()
            },
            "nda": {
                "EN": self._get_nda_template_en(),
                "DE": self._get_nda_template_de()
            },
            "b2b_contract": {
                "EN": self._get_b2b_contract_template_en(),
                "DE": self._get_b2b_contract_template_de()
            }
        }
    
    def generate_document(self, document_type: str, data: Dict[str, Any], language: str = "EN") -> str:
        """
        Generate a document using the specified template and data.
        
        Args:
            document_type: Type of document to generate
            data: Collected data for document generation
            language: Language for document (EN or DE)
            
        Returns:
            Generated document as string
        """
        try:
            # Check if localization is needed
            target_country = data.get("target_country", "").lower()
            
            if target_country and target_country not in ["united states", "us", "usa", "america"]:
                # Load localization research if available
                localization_context = self._load_localization_context(document_type, target_country)
                if localization_context:
                    # Enhance data with localization insights
                    data["localization_context"] = localization_context
                    data["target_country"] = target_country.title()
            
            # Always use English template for consistency (localization handled in content)
            try:
                template_file = f"{document_type}_en.j2"
                template = self.env.get_template(template_file)
            except:
                # Fallback to built-in template
                template_content = self.templates.get(document_type, {}).get("EN", "")
                if not template_content:
                    return f"Template not found for document type: {document_type}"
                
                template = Template(template_content)
            
            # Process data for template
            processed_data = self._process_data_for_template(data, document_type, language)
            
            # Generate document
            try:
                document = template.render(**processed_data)
                return document
            except Exception as e:
                return f"Error generating document: {str(e)}"
                
        except Exception as e:
            return f"Error generating document: {str(e)}"
    
    def _process_data_for_template(self, data: Dict[str, Any], document_type: str, language: str) -> Dict[str, Any]:
        """Process and format data for template rendering."""
        processed_data = data.copy()
        
        # Add common formatting
        processed_data["language"] = language
        processed_data["document_type"] = document_type
        
        # Format dates if present
        date_fields = ["lease_start_date", "lease_end_date", "effective_date", "start_date", "end_date"]
        for field in date_fields:
            if field in processed_data:
                processed_data[f"{field}_formatted"] = self._format_date(processed_data[field], language)
        
        # Format currency amounts
        currency_fields = ["rent_amount", "security_deposit", "contract_value"]
        for field in currency_fields:
            if field in processed_data:
                processed_data[f"{field}_formatted"] = self._format_currency(processed_data[field], language)
        
        # Process boolean fields
        boolean_fields = ["utilities_included", "pets_allowed"]
        for field in boolean_fields:
            if field in processed_data:
                processed_data[f"{field}_formatted"] = self._format_boolean(processed_data[field], language)
        
        return processed_data
    
    def _load_localization_context(self, document_type: str, country: str) -> Optional[Dict]:
        """Load localization research context for document generation."""
        try:
            import glob
            import json
            
            # Look for research files
            pattern = f"research_data/localization_research_{document_type}_{country}_*.json"
            files = glob.glob(pattern)
            
            if files:
                # Get the most recent file
                latest_file = max(files, key=lambda x: os.path.getctime(x))
                
                with open(latest_file, 'r', encoding='utf-8') as f:
                    research_data = json.load(f)
                
                return {
                    "legal_requirements": research_data.get("legal_requirements", []),
                    "template_structure": research_data.get("template_structure", []),
                    "key_clauses": research_data.get("key_clauses", []),
                    "compliance_notes": research_data.get("compliance_notes", []),
                    "sources": research_data.get("sources", [])
                }
            
            return None
            
        except Exception as e:
            print(f"Error loading localization context: {e}")
            return None
    
    def _format_date(self, date_str: str, language: str) -> str:
        """Format date string for display."""
        try:
            from datetime import datetime
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            if language == "DE":
                return date_obj.strftime("%d.%m.%Y")
            else:
                return date_obj.strftime("%B %d, %Y")
        except:
            return date_str
    
    def _format_currency(self, amount: str, language: str) -> str:
        """Format currency amount for display."""
        try:
            amount_float = float(amount)
            if language == "DE":
                return f"{amount_float:,.2f} €"
            else:
                return f"${amount_float:,.2f}"
        except:
            return amount
    
    def _format_boolean(self, value: str, language: str) -> str:
        """Format boolean value for display."""
        value_lower = value.lower().strip()
        positive_responses = ["yes", "y", "ja", "j", "true", "1"]
        
        if value_lower in positive_responses:
            return "Yes" if language == "EN" else "Ja"
        else:
            return "No" if language == "EN" else "Nein"
    
    def _get_residential_lease_template_en(self) -> str:
        """Get English residential lease template."""
        return """
RESIDENTIAL LEASE AGREEMENT

This Residential Lease Agreement (the "Lease") is entered into on {{ lease_start_date_formatted }} by and between:

LANDLORD: {{ landlord_name }}
TENANT: {{ tenant_name }}

PROPERTY ADDRESS: {{ property_address }}

1. TERM OF LEASE
   This lease shall commence on {{ lease_start_date_formatted }} and terminate on {{ lease_end_date_formatted }}.

2. RENT
   The monthly rent shall be {{ rent_amount_formatted }} per month, due on the first day of each month.

3. SECURITY DEPOSIT
   Tenant shall pay a security deposit of {{ security_deposit_formatted }} upon signing this lease.

4. UTILITIES
   {% if utilities_included_formatted == "Yes" %}
   Utilities are included in the rent.
   {% else %}
   Tenant is responsible for all utilities.
   {% endif %}

5. PETS
   {% if pets_allowed_formatted == "Yes" %}
   Pets are allowed with written permission from landlord.
   {% else %}
   No pets are allowed on the premises.
   {% endif %}

6. MAINTENANCE
   Landlord shall be responsible for major repairs and maintenance. Tenant shall be responsible for minor maintenance and keeping the premises clean.

7. TERMINATION
   Either party may terminate this lease with 30 days written notice.

8. GOVERNING LAW
   This lease shall be governed by the laws of the jurisdiction where the property is located.

SIGNATURES:

Landlord: ___________________________ Date: ________________

Tenant: ___________________________ Date: ________________
"""
    
    def _get_residential_lease_template_de(self) -> str:
        """Get German residential lease template."""
        return """
WOHNUNGSMIETVERTRAG

Dieser Wohnungsmietvertrag (der "Vertrag") wird am {{ lease_start_date_formatted }} zwischen folgenden Parteien geschlossen:

VERMIETER: {{ landlord_name }}
MIETER: {{ tenant_name }}

OBJEKTADRESSE: {{ property_address }}

1. MIETDAUER
   Dieser Mietvertrag beginnt am {{ lease_start_date_formatted }} und endet am {{ lease_end_date_formatted }}.

2. MIETE
   Die monatliche Miete beträgt {{ rent_amount_formatted }} pro Monat, fällig am ersten Tag jedes Monats.

3. KAUTION
   Der Mieter zahlt eine Kaution in Höhe von {{ security_deposit_formatted }} bei Unterzeichnung dieses Vertrags.

4. NEBENKOSTEN
   {% if utilities_included_formatted == "Ja" %}
   Nebenkosten sind in der Miete enthalten.
   {% else %}
   Der Mieter ist für alle Nebenkosten verantwortlich.
   {% endif %}

5. HAUSTIERE
   {% if pets_allowed_formatted == "Ja" %}
   Haustiere sind mit schriftlicher Genehmigung des Vermieters erlaubt.
   {% else %}
   Haustiere sind auf dem Grundstück nicht erlaubt.
   {% endif %}

6. INSTANDHALTUNG
   Der Vermieter ist für größere Reparaturen und Wartung verantwortlich. Der Mieter ist für kleinere Wartungsarbeiten und Sauberkeit verantwortlich.

7. KÜNDIGUNG
   Jede Partei kann diesen Vertrag mit 30 Tagen schriftlicher Kündigung beenden.

8. GELTENDES RECHT
   Dieser Vertrag unterliegt den Gesetzen der Gerichtsbarkeit, in der sich das Objekt befindet.

UNTERSCHRIFTEN:

Vermieter: ___________________________ Datum: ________________

Mieter: ___________________________ Datum: ________________
"""
    
    def _get_nda_template_en(self) -> str:
        """Get English NDA template."""
        return """
NON-DISCLOSURE AGREEMENT

This Non-Disclosure Agreement (the "Agreement") is entered into on {{ effective_date_formatted }} by and between:

DISCLOSING PARTY: {{ disclosing_party }}
RECEIVING PARTY: {{ receiving_party }}

1. CONFIDENTIAL INFORMATION
   The disclosing party will share the following confidential information: {{ confidential_information }}

2. PURPOSE
   The purpose of sharing this information is: {{ purpose }}

3. CONFIDENTIALITY OBLIGATIONS
   The receiving party agrees to:
   - Keep all confidential information strictly confidential
   - Use the information only for the stated purpose
   - Not disclose the information to any third party
   - Return or destroy all confidential information upon request

4. DURATION
   This confidentiality obligation shall remain in effect for {{ duration }} years from the effective date.

5. GOVERNING LAW
   This agreement shall be governed by the laws of the jurisdiction where the disclosing party is located.

SIGNATURES:

Disclosing Party: ___________________________ Date: ________________

Receiving Party: ___________________________ Date: ________________
"""
    
    def _get_nda_template_de(self) -> str:
        """Get German NDA template."""
        return """
GEHEIMHALTUNGSVEREINBARUNG

Diese Geheimhaltungsvereinbarung (die "Vereinbarung") wird am {{ effective_date_formatted }} zwischen folgenden Parteien geschlossen:

OFFENLEGENDE PARTEI: {{ disclosing_party }}
EMPFANGENDE PARTEI: {{ receiving_party }}

1. VERTRAULICHE INFORMATIONEN
   Die offenlegende Partei wird folgende vertrauliche Informationen teilen: {{ confidential_information }}

2. ZWECK
   Der Zweck der Weitergabe dieser Informationen ist: {{ purpose }}

3. VERTRAULICHKEITSVERPFLICHTUNGEN
   Die empfangende Partei stimmt zu:
   - Alle vertraulichen Informationen streng vertraulich zu behandeln
   - Die Informationen nur für den angegebenen Zweck zu verwenden
   - Die Informationen nicht an Dritte weiterzugeben
   - Alle vertraulichen Informationen auf Anfrage zurückzugeben oder zu vernichten

4. DAUER
   Diese Vertraulichkeitsverpflichtung bleibt {{ duration }} Jahre ab dem Wirksamkeitsdatum in Kraft.

5. GELTENDES RECHT
   Diese Vereinbarung unterliegt den Gesetzen der Gerichtsbarkeit, in der sich die offenlegende Partei befindet.

UNTERSCHRIFTEN:

Offenlegende Partei: ___________________________ Datum: ________________

Empfangende Partei: ___________________________ Datum: ________________
"""
    
    def _get_b2b_contract_template_en(self) -> str:
        """Get English B2B contract template."""
        return """
BUSINESS-TO-BUSINESS CONTRACT

This Business-to-Business Contract (the "Contract") is entered into on {{ start_date_formatted }} by and between:

CLIENT: {{ client_name }}
SERVICE PROVIDER: {{ service_provider_name }}

1. SERVICES
   The service provider shall provide the following services: {{ service_description }}

2. CONTRACT VALUE
   The total contract value is {{ contract_value_formatted }}.

3. PAYMENT TERMS
   Payment terms: {{ payment_terms }}

4. CONTRACT PERIOD
   This contract shall commence on {{ start_date_formatted }} and terminate on {{ end_date_formatted }}.

5. DELIVERABLES
   The service provider shall deliver all agreed-upon deliverables within the specified timeframe.

6. CONFIDENTIALITY
   Both parties agree to maintain confidentiality of any proprietary information shared during the course of this contract.

7. TERMINATION
   Either party may terminate this contract with 30 days written notice.

8. GOVERNING LAW
   This contract shall be governed by the laws of the jurisdiction where the service provider is located.

SIGNATURES:

Client: ___________________________ Date: ________________

Service Provider: ___________________________ Date: ________________
"""
    
    def _get_b2b_contract_template_de(self) -> str:
        """Get German B2B contract template."""
        return """
B2B-VERTRAG

Dieser B2B-Vertrag (der "Vertrag") wird am {{ start_date_formatted }} zwischen folgenden Parteien geschlossen:

KUNDE: {{ client_name }}
DIENSTLEISTER: {{ service_provider_name }}

1. DIENSTLEISTUNGEN
   Der Dienstleister erbringt folgende Dienstleistungen: {{ service_description }}

2. VERTRAGSWERT
   Der Gesamtwert des Vertrags beträgt {{ contract_value_formatted }}.

3. ZAHLUNGSBEDINGUNGEN
   Zahlungsbedingungen: {{ payment_terms }}

4. VERTRAGSDAUER
   Dieser Vertrag beginnt am {{ start_date_formatted }} und endet am {{ end_date_formatted }}.

5. LEISTUNGEN
   Der Dienstleister liefert alle vereinbarten Leistungen innerhalb des festgelegten Zeitrahmens.

6. VERTRAULICHKEIT
   Beide Parteien stimmen zu, die Vertraulichkeit aller während der Laufzeit dieses Vertrags geteilten proprietären Informationen zu wahren.

7. KÜNDIGUNG
   Jede Partei kann diesen Vertrag mit 30 Tagen schriftlicher Kündigung beenden.

8. GELTENDES RECHT
   Dieser Vertrag unterliegt den Gesetzen der Gerichtsbarkeit, in der sich der Dienstleister befindet.

UNTERSCHRIFTEN:

Kunde: ___________________________ Datum: ________________

Dienstleister: ___________________________ Datum: ________________
"""
