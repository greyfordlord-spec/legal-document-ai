import os
from typing import Dict, List, Any, Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from config.settings import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_TEMPERATURE

class AIEngine:
    """AI engine for handling LLM interactions."""
    
    def __init__(self):
        """Initialize the AI engine with OpenAI configuration."""
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required. Please set it in your .env file.")
        
        self.llm = ChatOpenAI(
            model=OPENAI_MODEL,
            temperature=OPENAI_TEMPERATURE,
            api_key=OPENAI_API_KEY
        )
        
        # System prompts for different conversation states
        self.system_prompts = {
            "greeting": {
                "EN": """You are a professional legal document assistant. Your role is to help users generate legal documents through a conversational interface. 
                Be friendly, professional, and guide users through the document generation process step by step.
                Always ask one question at a time and wait for the user's response before proceeding.""",
                "DE": """Sie sind ein professioneller Assistent für rechtliche Dokumente. Ihre Aufgabe ist es, Benutzern bei der Erstellung rechtlicher Dokumente durch eine Gesprächsoberfläche zu helfen.
                Seien Sie freundlich, professionell und führen Sie Benutzer Schritt für Schritt durch den Dokumentenerstellungsprozess.
                Stellen Sie immer nur eine Frage auf einmal und warten Sie auf die Antwort des Benutzers, bevor Sie fortfahren."""
            },
            "document_selection": {
                "EN": """You are helping the user select a legal document type. Present the available options clearly and ask which type they would like to generate.""",
                "DE": """Sie helfen dem Benutzer bei der Auswahl eines rechtlichen Dokumenttyps. Präsentieren Sie die verfügbaren Optionen klar und fragen Sie, welchen Typ sie generieren möchten."""
            },
            "information_gathering": {
                "EN": """You are collecting information for document generation. Ask specific questions one at a time to gather all required information. 
                Be clear about what information is needed and why. Validate user responses when appropriate.""",
                "DE": """Sie sammeln Informationen für die Dokumentenerstellung. Stellen Sie spezifische Fragen einzeln, um alle erforderlichen Informationen zu sammeln.
                Seien Sie klar darüber, welche Informationen benötigt werden und warum. Validieren Sie Benutzerantworten, wenn es angebracht ist."""
            },
            "document_generation": {
                "EN": """You are generating a legal document based on the collected information. Create a professional, well-formatted document that follows legal standards and best practices. If localization context is provided, adapt the document for the target jurisdiction and incorporate country-specific legal requirements.""",
                "DE": """Sie erstellen ein rechtliches Dokument basierend auf den gesammelten Informationen. Erstellen Sie ein professionelles, gut formatiertes Dokument, das rechtlichen Standards und bewährten Praktiken entspricht. Falls Lokalisierungskontext bereitgestellt wird, passen Sie das Dokument für die Zielgerichtsbarkeit an und integrieren Sie länderspezifische rechtliche Anforderungen."""
            }
        }
    
    def get_response(self, 
                    user_message: str, 
                    conversation_history: List[Dict[str, str]], 
                    state: str = "greeting",
                    language: str = "EN",
                    context: Optional[Dict[str, Any]] = None) -> str:
        """
        Get AI response based on user message and conversation state.
        
        Args:
            user_message: The user's input message
            conversation_history: List of previous messages in format [{"role": "user/assistant", "content": "message"}]
            state: Current conversation state (greeting, document_selection, information_gathering, document_generation)
            language: Language for response (EN or DE)
            context: Additional context information (document type, collected data, etc.)
        
        Returns:
            AI response string
        """
        # Build system prompt
        system_prompt = self.system_prompts.get(state, self.system_prompts["greeting"]).get(language, self.system_prompts["greeting"]["EN"])
        
        # Add context-specific instructions
        if context:
            if state == "document_selection":
                doc_types = context.get("document_types", {})
                system_prompt += f"\n\nAvailable document types:\n"
                for doc_id, doc_info in doc_types.items():
                    system_prompt += f"- {doc_info['name']}: {doc_info['description']}\n"
                system_prompt += "\nAsk the user which document type they would like to generate."
            
            elif state == "information_gathering":
                current_question = context.get("current_question", "")
                collected_data = context.get("collected_data", {})
                system_prompt += f"\n\nCurrent question: {current_question}"
                if collected_data:
                    system_prompt += f"\nCollected information so far: {collected_data}"
                system_prompt += "\nAsk the current question and wait for the user's response."
            
            elif state == "document_generation":
                doc_type = context.get("document_type", "")
                collected_data = context.get("collected_data", {})
                system_prompt += f"\n\nDocument type: {doc_type}"
                system_prompt += f"\nCollected data: {collected_data}"
                system_prompt += "\nGenerate a professional legal document using the provided template and data."
        
        # Build messages
        messages = [SystemMessage(content=system_prompt)]
        
        # Add conversation history
        for msg in conversation_history[-10:]:  # Keep last 10 messages for context
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            else:
                messages.append(SystemMessage(content=msg["content"]))
        
        # Add current user message
        messages.append(HumanMessage(content=user_message))
        
        try:
            # Get response from LLM
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            error_msg = {
                "EN": f"I apologize, but I encountered an error: {str(e)}. Please try again.",
                "DE": f"Entschuldigung, aber es ist ein Fehler aufgetreten: {str(e)}. Bitte versuchen Sie es erneut."
            }
            return error_msg.get(language, error_msg["EN"])
    
    def validate_response(self, user_input: str, expected_type: str, language: str = "EN") -> tuple[bool, str]:
        """
        Validate user input based on expected type.
        
        Args:
            user_input: User's input to validate
            expected_type: Expected data type (text, number, date, boolean)
            language: Language for error messages
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not user_input.strip():
            return False, "Input cannot be empty."
        
        if expected_type == "number":
            try:
                float(user_input)
                return True, ""
            except ValueError:
                return False, "Please enter a valid number."
        
        elif expected_type == "date":
            # Simple date validation (YYYY-MM-DD format)
            import re
            date_pattern = r'^\d{4}-\d{2}-\d{2}$'
            if not re.match(date_pattern, user_input):
                return False, "Please enter date in YYYY-MM-DD format."
            return True, ""
        
        elif expected_type == "boolean":
            positive_responses = ["yes", "y", "ja", "j", "true", "1"] if language == "EN" else ["ja", "j", "yes", "y", "true", "1"]
            negative_responses = ["no", "n", "nein", "false", "0"] if language == "EN" else ["nein", "n", "no", "false", "0"]
            
            user_input_lower = user_input.lower().strip()
            if user_input_lower in positive_responses + negative_responses:
                return True, ""
            else:
                return False, f"Please answer with {'yes/no' if language == 'EN' else 'ja/nein'}."
        
        # For text type, any non-empty input is valid
        return True, ""
