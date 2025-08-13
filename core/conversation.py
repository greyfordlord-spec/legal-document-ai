from typing import Dict, List, Any, Optional
from enum import Enum
from data.document_types import get_document_questions, get_all_document_types
from core.ai_engine import AIEngine

class ConversationState(Enum):
    """Enumeration of conversation states."""
    GREETING = "greeting"
    DOCUMENT_SELECTION = "document_selection"
    INFORMATION_GATHERING = "information_gathering"
    LOCALIZATION_RESEARCH = "localization_research"
    DOCUMENT_GENERATION = "document_generation"
    COMPLETED = "completed"

class ConversationManager:
    """Manages conversation flow and state for document generation."""
    
    def __init__(self, language: str = "EN"):
        """Initialize conversation manager."""
        self.language = language
        self.ai_engine = AIEngine()
        self.state = ConversationState.GREETING
        self.conversation_history = []
        self.current_document_type = None
        self.collected_data = {}
        self.current_question_index = 0
        self.document_questions = []
        
        # Greeting messages
        self.greetings = {
            "EN": "Hello! I'm your legal document assistant. I can help you generate professional legal documents including NDAs, contracts, leases, and more. Simply tell me what type of document you need, and I'll guide you through the process step by step. What would you like to create today?",
            "DE": "Hallo! Ich bin Ihr Assistent für rechtliche Dokumente. Ich kann Ihnen bei der Erstellung professioneller rechtlicher Dokumente helfen, einschließlich NDAs, Verträgen, Mietverträgen und mehr. Sagen Sie mir einfach, welche Art von Dokument Sie benötigen, und ich führe Sie Schritt für Schritt durch den Prozess. Was möchten Sie heute erstellen?"
        }
    
    def get_initial_message(self) -> str:
        """Get the initial greeting message."""
        return self.greetings.get(self.language, self.greetings["EN"])
    
    def process_user_message(self, user_message: str) -> tuple[str, bool]:
        """
        Process user message and return AI response.
        
        Args:
            user_message: User's input message
            
        Returns:
            Tuple of (AI response, is_conversation_complete)
        """
        # Add user message to history
        self.conversation_history.append({"role": "user", "content": user_message})
        
        # Process based on current state
        if self.state == ConversationState.GREETING:
            return self._handle_greeting_state(user_message)
        
        elif self.state == ConversationState.DOCUMENT_SELECTION:
            return self._handle_document_selection_state(user_message)
        
        elif self.state == ConversationState.INFORMATION_GATHERING:
            return self._handle_information_gathering_state(user_message)
        
        elif self.state == ConversationState.LOCALIZATION_RESEARCH:
            return self._handle_localization_research_state(user_message)
        elif self.state == ConversationState.DOCUMENT_GENERATION:
            return self._handle_document_generation_state(user_message)
        
        else:
            return "I'm not sure how to proceed. Let me start over.", False
    
    def _handle_greeting_state(self, user_message: str) -> tuple[str, bool]:
        """Handle greeting state - transition to document selection."""
        self.state = ConversationState.DOCUMENT_SELECTION
        
        # Get available document types
        doc_types = get_all_document_types(self.language)
        
        # Generate AI response for document selection
        context = {"document_types": doc_types}
        ai_response = self.ai_engine.get_response(
            user_message, 
            self.conversation_history, 
            "document_selection", 
            self.language, 
            context
        )
        
        self.conversation_history.append({"role": "assistant", "content": ai_response})
        return ai_response, False
    
    def _handle_document_selection_state(self, user_message: str) -> tuple[str, bool]:
        """Handle document selection state."""
        # Try to identify document type from user message
        doc_type = self._identify_document_type(user_message)
        
        if doc_type:
            self.current_document_type = doc_type
            self.document_questions = get_document_questions(doc_type, self.language)
            self.state = ConversationState.INFORMATION_GATHERING
            self.current_question_index = 0
            
            # Get first question
            if self.document_questions:
                first_question = self.document_questions[0]["question"]
                response = f"🎯 **Perfect!** I'll help you create a {self._get_document_name(doc_type)}.\n\nI need to gather some essential information to generate your document. Let me ask you a few questions:\n\n**{first_question}**"
            else:
                response = f"Great! I'll help you create a {self._get_document_name(doc_type)}. Let me generate the document for you."
                self.state = ConversationState.DOCUMENT_GENERATION
            
            self.conversation_history.append({"role": "assistant", "content": response})
            return response, False
        else:
            # Ask for clarification
            doc_types = get_all_document_types(self.language)
            context = {"document_types": doc_types}
            ai_response = self.ai_engine.get_response(
                user_message, 
                self.conversation_history, 
                "document_selection", 
                self.language, 
                context
            )
            
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            return ai_response, False
    
    def _handle_information_gathering_state(self, user_message: str) -> tuple[str, bool]:
        """Handle information gathering state."""
        if self.current_question_index >= len(self.document_questions):
            # All questions answered, move to document generation
            self.state = ConversationState.DOCUMENT_GENERATION
            return self._handle_document_generation_state(user_message)
        
        current_question = self.document_questions[self.current_question_index]
        question_id = current_question["id"]
        question_text = current_question["question"]
        expected_type = current_question["type"]
        
        # Validate user input
        is_valid, error_message = self.ai_engine.validate_response(user_message, expected_type, self.language)
        
        if not is_valid:
            response = f"{error_message}\n\n{question_text}"
            self.conversation_history.append({"role": "assistant", "content": response})
            return response, False
        
        # Store the answer
        self.collected_data[question_id] = user_message
        self.current_question_index += 1
        
        # Check if we have more questions
        if self.current_question_index < len(self.document_questions):
            next_question = self.document_questions[self.current_question_index]["question"]
            response = f"✅ **Got it!** {next_question}"
        else:
            # All questions answered
            self.state = ConversationState.DOCUMENT_GENERATION
            response = "🎉 Perfect! I have gathered all the necessary information for your document. I'm now working on generating your professional legal document. Please hold on while I create it for you..."
        
        self.conversation_history.append({"role": "assistant", "content": response})
        return response, False
    
    def _handle_localization_research_state(self, user_message: str) -> tuple[str, bool]:
        """Handle localization research state."""
        from core.localization_research import LocalizationResearchEngine
        
        # Get target country from collected data
        target_country = self.collected_data.get("target_country", "")
        
        if not target_country:
            # Fallback to standard document generation
            self.state = ConversationState.DOCUMENT_GENERATION
            response = "🎉 Perfect! I have gathered all the necessary information for your document. I'm now working on generating your professional legal document. Please hold on while I create it for you..."
            self.conversation_history.append({"role": "assistant", "content": response})
            return response, False
        
        # Research country-specific requirements
        research_engine = LocalizationResearchEngine()
        
        try:
            # Get localization guidance
            guidance = research_engine.get_localized_document_guidance(
                self.current_document_type, 
                target_country
            )
            
            # Save research results
            research_results = research_engine.research_country_requirements(
                self.current_document_type, 
                target_country
            )
            research_engine.save_research_results(research_results)
            
            # Move to document generation with localization context
            self.state = ConversationState.DOCUMENT_GENERATION
            response = f"{guidance}\n\n🎯 **Now generating your localized document for {target_country.title()}...**\n\nPlease hold on while I create a jurisdiction-compliant document based on my research."
            
        except Exception as e:
            print(f"Localization research error: {e}")
            # Fallback to standard document generation
            self.state = ConversationState.DOCUMENT_GENERATION
            response = f"⚠️ **Note:** I encountered an issue researching {target_country.title()} requirements. I'll generate a standard document, but please verify compliance with local laws.\n\n🎯 **Generating your document now...**"
        
        self.conversation_history.append({"role": "assistant", "content": response})
        return response, False
    
    def _handle_document_generation_state(self, user_message: str) -> tuple[str, bool]:
        """Handle document generation state."""
        # Generate the document
        from core.document_gen import DocumentGenerator
        
        doc_generator = DocumentGenerator()
        generated_document = doc_generator.generate_document(
            self.current_document_type,
            self.collected_data,
            self.language
        )
        
        response = f"✅ **Document Generation Complete!**\n\nHere's your generated {self._get_document_name(self.current_document_type)}:\n\n{generated_document}\n\n🎯 **Next Steps:**\nYou can now export this document as a PDF or DOCX file using the export options in the sidebar."
        
        self.conversation_history.append({"role": "assistant", "content": response})
        self.state = ConversationState.COMPLETED
        
        return response, True
    
    def _identify_document_type(self, user_message: str) -> Optional[str]:
        """Identify document type from user message."""
        user_message_lower = user_message.lower()
        doc_types = get_all_document_types(self.language)
        
        # Create mapping of keywords to document types
        keyword_mapping = {
            "residential_lease": ["lease", "rent", "rental", "mietvertrag", "miete", "wohnung"],
            "nda": ["nda", "non-disclosure", "confidentiality", "geheimhaltung", "vertraulich"],
            "b2b_contract": ["b2b", "business", "contract", "service", "vertrag", "dienstleistung"],
            "power_of_attorney": ["power of attorney", "vollmacht", "attorney", "authorization"],
            "employment_contract": ["employment", "work", "job", "arbeitsvertrag", "arbeit"],
            "meeting_minutes": ["minutes", "meeting", "resolution", "protokoll", "beschluss"]
        }
        
        # Check for keyword matches
        for doc_type, keywords in keyword_mapping.items():
            if any(keyword in user_message_lower for keyword in keywords):
                return doc_type
        
        # Check for exact document type names
        for doc_type, doc_info in doc_types.items():
            doc_name_lower = doc_info["name"].lower()
            if doc_name_lower in user_message_lower:
                return doc_type
        
        return None
    
    def _get_document_name(self, doc_type: str) -> str:
        """Get document name in current language."""
        doc_types = get_all_document_types(self.language)
        return doc_types.get(doc_type, {}).get("name", doc_type)
    
    def reset_conversation(self):
        """Reset conversation to initial state."""
        self.state = ConversationState.GREETING
        self.conversation_history = []
        self.current_document_type = None
        self.collected_data = {}
        self.current_question_index = 0
        self.document_questions = []
    
    def get_current_state(self) -> ConversationState:
        """Get current conversation state."""
        return self.state
    
    def get_collected_data(self) -> Dict[str, Any]:
        """Get collected data for document generation."""
        return self.collected_data.copy()
    
    def get_current_document_type(self) -> Optional[str]:
        """Get current document type."""
        return self.current_document_type
    
    def process_message(self, user_message: str) -> str:
        """
        Process user message and return AI response.
        This is a simplified wrapper for the existing process_user_message method.
        
        Args:
            user_message: User's input message
            
        Returns:
            AI response string
        """
        try:
            response, is_complete = self.process_user_message(user_message)
            return response
        except Exception as e:
            error_msg = f"I'm sorry, I encountered an error processing your message: {str(e)}"
            self.conversation_history.append({"role": "assistant", "content": error_msg})
            return error_msg
