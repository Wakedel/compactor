# Compactor

An AI-powered document analysis and synthesis system built with CrewAI and Streamlit. Upload PDFs and URLs, share your intuitions and questions, and get comprehensive reports with key insights.

## Features

- 📄 PDF document upload with drag-and-drop support
- 🔗 URL analysis capabilities
- 💡 Intuition validation
- ❓ Question answering
- 📊 Comprehensive report generation
- 🎨 Modern, clean interface

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your Google API key:
- Get a Google API key from the Google Cloud Console
- Set the environment variable:
```bash
export GEMINI_API_KEY='your-api-key'
export GOOGLE_API_KEY='your-api-key'
```

## Running the Application

Start the application with:
```bash
streamlit run src/app.py
```

## Usage

1. Upload PDF documents using the file uploader or drag-and-drop
2. Add URLs containing relevant information
3. Share your intuitions about the content
4. Ask specific questions you'd like answered
5. Click "Generate Report" to get your analysis

## Technologies

- CrewAI for multi-agent orchestration
- Streamlit for the user interface
- Google's Gemini Pro for AI processing

## License

MIT