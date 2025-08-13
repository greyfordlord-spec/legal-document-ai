# Legal Document AI Assistant

A local AI-powered chatbot for generating legal documents through conversational interface. Built with Streamlit, LangChain, and OpenAI.

## Features

- **Interactive Chat Interface**: Natural conversation flow for document generation
- **Multiple Document Types**: Support for residential leases, NDAs, B2B contracts, power of attorney, employment contracts, and meeting minutes
- **Template-Based Generation**: Professional legal document templates with dynamic content filling
- **Export Capabilities**: Export generated documents as PDF or DOCX
- **Multi-language Support**: German and English interface
- **Extensible Architecture**: Easy to add new document types and templates

## Supported Document Types

1. **Residential Lease Agreement** - Complete lease contracts with all standard clauses
2. **Non-Disclosure Agreement (NDA)** - Confidentiality agreements for business relationships
3. **Business-to-Business Contract** - Professional service and partnership agreements
4. **Power of Attorney** - Legal authorization documents
5. **Employment Contract** - Standard employment agreements
6. **Meeting Minutes/Resolutions** - Corporate meeting documentation

## Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key (or other compatible LLM)

### Installation

1. **Clone or download this repository**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file in the project root:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. **Run the application**:
   ```bash
   streamlit run app.py
   ```

5. **Access the application**:
   Open your browser and go to `http://localhost:8501`

## Project Structure

```
legal-document-ai/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Development dependencies
├── requirements-deploy.txt   # Production dependencies for Streamlit Cloud
├── README.md                # This file
├── .streamlit/              # Streamlit configuration
│   └── config.toml         # Streamlit settings
├── assets/                  # Static assets (logos, icons)
├── core/                    # Core AI and conversation logic
│   ├── ai_engine.py        # AI engine implementation
│   ├── conversation.py     # Conversation management
│   ├── document_gen.py     # Document generation
│   └── localization_research.py # Localization features
├── config/                  # Configuration settings
│   ├── settings.py         # App configuration
│   └── ui_translations.py  # Multi-language support
├── data/                    # Document type definitions
│   └── document_types.py   # Document type configurations
├── templates/               # Document templates and prompts
│   ├── document_templates/ # Legal document templates
│   └── prompts/            # AI prompt templates
├── utils/                   # Utility functions
│   ├── export.py           # Document export functionality
│   └── advanced_components.py # Advanced UI components
├── assets/                  # All images and branding assets
├── docs/                    # Documentation
│   ├── STREAMLIT_CLOUD_DEPLOYMENT.md # Deployment guide
│   └── DEPLOYMENT_CHECKLIST.md       # Deployment checklist
└── exports/                 # Generated documents (auto-created)
```

## Usage

1. **Start a conversation**: The AI will greet you and ask which document type you want to generate
2. **Select document type**: Choose from the available legal document types
3. **Answer questions**: The AI will ask specific questions to gather all required information
4. **Review and export**: Once complete, review the generated document and export as needed

## Deployment

### Local Development
```bash
streamlit run app.py
```

### Streamlit Community Cloud
See `docs/STREAMLIT_CLOUD_DEPLOYMENT.md` for detailed deployment instructions.

**Important**: Use `requirements-deploy.txt` for Streamlit Cloud deployment.

## Configuration

### Adding New Document Types

1. Add document definition in `data/document_types.py`
2. Create template in `templates/document_templates/`
3. Update prompts in `templates/prompts/`

### Customizing AI Behavior

Modify prompts and conversation flow in:
- `core/conversation.py` - Conversation state management
- `templates/prompts/` - AI prompt templates

## Architecture

- **Frontend**: Streamlit web interface
- **AI Engine**: LangChain with OpenAI integration
- **Templates**: Jinja2 for document generation
- **Export**: python-docx and reportlab for document export

## Development

### Adding Features

1. **New Document Type**: Add to `data/document_types.py` and create corresponding template
2. **New Export Format**: Extend `utils/export.py`
3. **Custom AI Behavior**: Modify prompts in `templates/prompts/`

## License

This project is for educational and professional use. Please ensure compliance with local legal requirements when using generated documents.

## Support

For issues or questions, please check the code comments and documentation within the project files.
