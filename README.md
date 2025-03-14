# Compactor

An AI-powered document analysis and synthesis system built with CrewAI and Streamlit. Upload PDFs and URLs, share your intuitions and questions, and get comprehensive reports with key insights.

## Features

- 📄 PDF document upload with drag-and-drop support
- 🔗 URL analysis capabilities
- 💡 Intuition validation
- ❓ Question answering
- 📊 Comprehensive report generation with PDF export
- 🎨 Modern, clean interface
- 🔒 Secure API key management

## Prerequisites

- Python 3.10 or higher
- Google Gemini API key
- Conda (recommended)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/compactor.git
cd compactor
```

2. Create conda environment:
```bash
conda create -n compactor python=3.12.8
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Activate your conda environment:
```bash
conda activate compactor
```

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