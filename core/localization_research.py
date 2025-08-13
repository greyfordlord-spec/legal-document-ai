import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
import re
from typing import Dict, List, Optional, Tuple
import json
import time

class LocalizationResearchEngine:
    """
    Engine for researching country-specific legal document requirements
    and templates from the internet.
    """
    
    def __init__(self):
        self.search_engine = DDGS()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def research_country_requirements(self, document_type: str, country: str) -> Dict[str, any]:
        """
        Research legal requirements for a specific document type in a specific country.
        
        Args:
            document_type: Type of document (e.g., 'nda', 'employment_contract')
            country: Target country (e.g., 'Germany', 'United States')
            
        Returns:
            Dictionary containing research findings
        """
        print(f"🔍 Researching {document_type} requirements for {country}...")
        
        research_results = {
            "country": country,
            "document_type": document_type,
            "legal_requirements": [],
            "template_structure": [],
            "key_clauses": [],
            "compliance_notes": [],
            "sources": [],
            "last_updated": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Search queries for different aspects
        search_queries = self._generate_search_queries(document_type, country)
        
        for query_type, query in search_queries.items():
            print(f"   Searching: {query}")
            results = self._search_web(query)
            
            if results:
                if query_type == "legal_requirements":
                    research_results["legal_requirements"] = self._extract_legal_requirements(results)
                elif query_type == "template_structure":
                    research_results["template_structure"] = self._extract_template_structure(results)
                elif query_type == "key_clauses":
                    research_results["key_clauses"] = self._extract_key_clauses(results)
                elif query_type == "compliance":
                    research_results["compliance_notes"] = self._extract_compliance_notes(results)
                
                # Add sources
                for result in results[:3]:  # Top 3 sources
                    if result.get('link') not in [s['url'] for s in research_results["sources"]]:
                        research_results["sources"].append({
                            "url": result.get('link', ''),
                            "title": result.get('title', ''),
                            "snippet": result.get('body', '')[:200] + "..."
                        })
        
        return research_results
    
    def _generate_search_queries(self, document_type: str, country: str) -> Dict[str, str]:
        """Generate search queries for different research aspects."""
        
        # Document type mappings
        doc_mappings = {
            "nda": {
                "legal_requirements": f"{country} NDA legal requirements confidentiality agreement law",
                "template_structure": f"{country} NDA template structure format example",
                "key_clauses": f"{country} NDA mandatory clauses legal requirements",
                "compliance": f"{country} NDA compliance legal standards regulations"
            },
            "employment_contract": {
                "legal_requirements": f"{country} employment contract law legal requirements",
                "template_structure": f"{country} employment contract template format",
                "key_clauses": f"{country} employment contract mandatory terms clauses",
                "compliance": f"{country} employment law compliance requirements"
            },
            "residential_lease": {
                "legal_requirements": f"{country} residential lease law legal requirements",
                "template_structure": f"{country} residential lease agreement template",
                "key_clauses": f"{country} residential lease mandatory clauses terms",
                "compliance": f"{country} rental law compliance requirements"
            },
            "b2b_contract": {
                "legal_requirements": f"{country} business contract law legal requirements",
                "template_structure": f"{country} business contract template format",
                "key_clauses": f"{country} business contract mandatory clauses",
                "compliance": f"{country} business law compliance requirements"
            },
            "power_of_attorney": {
                "legal_requirements": f"{country} power of attorney legal requirements",
                "template_structure": f"{country} power of attorney template format",
                "key_clauses": f"{country} power of attorney mandatory clauses",
                "compliance": f"{country} power of attorney compliance law"
            },
            "meeting_minutes": {
                "legal_requirements": f"{country} meeting minutes legal requirements corporate law",
                "template_structure": f"{country} meeting minutes template format",
                "key_clauses": f"{country} meeting minutes mandatory elements",
                "compliance": f"{country} corporate meeting compliance requirements"
            }
        }
        
        return doc_mappings.get(document_type, {
            "legal_requirements": f"{country} {document_type} legal requirements",
            "template_structure": f"{country} {document_type} template format",
            "key_clauses": f"{country} {document_type} mandatory clauses",
            "compliance": f"{country} {document_type} compliance requirements"
        })
    
    def _search_web(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search the web using DuckDuckGo."""
        try:
            results = []
            search_results = self.search_engine.text(query, max_results=max_results)
            
            for result in search_results:
                results.append({
                    'title': result.get('title', ''),
                    'body': result.get('body', ''),
                    'link': result.get('link', '')
                })
            
            return results
        except Exception as e:
            print(f"   Search error: {e}")
            return []
    
    def _extract_legal_requirements(self, search_results: List[Dict]) -> List[str]:
        """Extract legal requirements from search results."""
        requirements = []
        
        for result in search_results:
            text = result.get('body', '').lower()
            
            # Look for requirement indicators
            requirement_indicators = [
                'required', 'mandatory', 'must include', 'shall contain',
                'legal requirement', 'obligatory', 'essential', 'necessary'
            ]
            
            for indicator in requirement_indicators:
                if indicator in text:
                    # Extract sentences containing requirements
                    sentences = re.split(r'[.!?]', result.get('body', ''))
                    for sentence in sentences:
                        if indicator in sentence.lower() and len(sentence.strip()) > 20:
                            requirements.append(sentence.strip())
                            break
        
        return list(set(requirements))[:10]  # Remove duplicates, limit to 10
    
    def _extract_template_structure(self, search_results: List[Dict]) -> List[str]:
        """Extract template structure information from search results."""
        structure_info = []
        
        for result in search_results:
            text = result.get('body', '').lower()
            
            # Look for structure indicators
            structure_indicators = [
                'section', 'clause', 'paragraph', 'article', 'part',
                'structure', 'format', 'template', 'outline', 'layout'
            ]
            
            for indicator in structure_indicators:
                if indicator in text:
                    sentences = re.split(r'[.!?]', result.get('body', ''))
                    for sentence in sentences:
                        if indicator in sentence.lower() and len(sentence.strip()) > 20:
                            structure_info.append(sentence.strip())
                            break
        
        return list(set(structure_info))[:10]
    
    def _extract_key_clauses(self, search_results: List[Dict]) -> List[str]:
        """Extract key clauses information from search results."""
        clauses_info = []
        
        for result in search_results:
            text = result.get('body', '').lower()
            
            # Look for clause indicators
            clause_indicators = [
                'clause', 'provision', 'term', 'condition', 'stipulation',
                'agreement', 'obligation', 'right', 'duty', 'liability'
            ]
            
            for indicator in clause_indicators:
                if indicator in text:
                    sentences = re.split(r'[.!?]', result.get('body', ''))
                    for sentence in sentences:
                        if indicator in sentence.lower() and len(sentence.strip()) > 20:
                            clauses_info.append(sentence.strip())
                            break
        
        return list(set(clauses_info))[:10]
    
    def _extract_compliance_notes(self, search_results: List[Dict]) -> List[str]:
        """Extract compliance information from search results."""
        compliance_info = []
        
        for result in search_results:
            text = result.get('body', '').lower()
            
            # Look for compliance indicators
            compliance_indicators = [
                'compliance', 'regulation', 'law', 'statute', 'code',
                'legal standard', 'regulatory', 'statutory', 'legislation'
            ]
            
            for indicator in compliance_indicators:
                if indicator in text:
                    sentences = re.split(r'[.!?]', result.get('body', ''))
                    for sentence in sentences:
                        if indicator in sentence.lower() and len(sentence.strip()) > 20:
                            compliance_info.append(sentence.strip())
                            break
        
        return list(set(compliance_info))[:10]
    
    def get_localized_document_guidance(self, document_type: str, country: str) -> str:
        """
        Get comprehensive guidance for creating a localized document.
        
        Args:
            document_type: Type of document
            country: Target country
            
        Returns:
            Formatted guidance string
        """
        research = self.research_country_requirements(document_type, country)
        
        guidance = f"""
🌍 **LOCALIZATION RESEARCH FOR {country.upper()} - {document_type.upper().replace('_', ' ').title()}**

📋 **Legal Requirements:**
"""
        
        if research["legal_requirements"]:
            for req in research["legal_requirements"][:5]:
                guidance += f"• {req}\n"
        else:
            guidance += "• No specific legal requirements found\n"
        
        guidance += f"\n📄 **Template Structure:**\n"
        
        if research["template_structure"]:
            for struct in research["template_structure"][:5]:
                guidance += f"• {struct}\n"
        else:
            guidance += "• Standard template structure recommended\n"
        
        guidance += f"\n⚖️ **Key Clauses:**\n"
        
        if research["key_clauses"]:
            for clause in research["key_clauses"][:5]:
                guidance += f"• {clause}\n"
        else:
            guidance += "• Standard clauses recommended\n"
        
        guidance += f"\n✅ **Compliance Notes:**\n"
        
        if research["compliance_notes"]:
            for note in research["compliance_notes"][:5]:
                guidance += f"• {note}\n"
        else:
            guidance += "• General compliance standards apply\n"
        
        guidance += f"\n📚 **Sources:**\n"
        
        for source in research["sources"][:3]:
            guidance += f"• {source['title']}: {source['url']}\n"
        
        guidance += f"\n⏰ **Research completed:** {research['last_updated']}"
        
        return guidance
    
    def save_research_results(self, research_results: Dict, filename: str = None):
        """Save research results to a JSON file."""
        if not filename:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"localization_research_{research_results['document_type']}_{research_results['country']}_{timestamp}.json"
        
        with open(f"research_data/{filename}", 'w', encoding='utf-8') as f:
            json.dump(research_results, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Research results saved to: {filename}")
