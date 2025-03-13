import streamlit as st
from crew import Compactor
import tempfile
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from io import BytesIO
import base64
import google.generativeai as genai

# Function to convert Markdown to PDF
def markdown_to_pdf(markdown_text):
    print(markdown_text)

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Create custom styles
    custom_styles = {
        'CustomH1': ParagraphStyle(
            'CustomH1',
            parent=styles['Heading1'],
            fontSize=20,
            spaceAfter=30,
            alignment=1,  # Center alignment
            backColor=colors.HexColor('#f0f0f0'),  # Light gray background
            borderPadding=10,  # Padding around text
            textColor=colors.HexColor('#2c3e50')  # Dark blue-gray text
        ),
        'CustomH2': ParagraphStyle(
            'CustomH2',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=20,
            leftIndent=20,  # Left indentation
            textColor=colors.HexColor('#34495e'),  # Slightly lighter blue-gray
            borderColor=colors.HexColor('#bdc3c7'),  # Light gray border
            borderWidth=1,
            borderPadding=8
        ),
        'CustomCode': ParagraphStyle(
            'CustomCode',
            parent=styles['Code'],
            fontName='Courier',
            fontSize=10,
            leftIndent=36,
            rightIndent=36,
            backColor=colors.lightgrey
        ),
        'CustomList': ParagraphStyle(
            'CustomList',
            parent=styles['Normal'],
            leftIndent=36,
            firstLineIndent=-18
        )
    }

    try:
        # Split text into paragraphs
        paragraphs = markdown_text.split('\n\n')
        
        for para in paragraphs:
            if not para.strip():
                continue

            # Handle code blocks
            if para.startswith('```'):
                code_lines = para.split('\n')[1:-1]  # Remove ``` lines
                code_text = '\n'.join(code_lines)
                story.append(Paragraph(code_text, custom_styles['CustomCode']))
                story.append(Spacer(1, 12))
                continue

            # Handle lists
            if para.startswith('- ') or para.startswith('* '):
                list_items = para.split('\n')
                for item in list_items:
                    if item.strip():
                        tmp = item[1:]
                        tmp = tmp.replace('**', '<b>', 1).replace('**', '</b>', 1)  # Bold
                        tmp = tmp.replace('*', '<i>', 1).replace('*', '</i>', 1)    # Italic
                        tmp = tmp.replace('`', '<code>', 1).replace('`', '</code>', 1)  # Inline code
                        bullet_text = '•' + tmp
                        story.append(Paragraph(bullet_text, custom_styles['CustomList']))
                story.append(Spacer(1, 6))
                continue

            # Handle headers and regular paragraphs
            if para.startswith('# '):
                text = para[2:]
                style = custom_styles['CustomH1']
            elif para.startswith('## '):
                text = para[3:]
                style = custom_styles['CustomH2']
            else:
                text = para
                style = styles['Normal']
            
            # Handle inline formatting
            text = text.replace('**', '<b>', 1).replace('**', '</b>', 1)  # Bold
            text = text.replace('*', '<i>', 1).replace('*', '</i>', 1)    # Italic
            text = text.replace('`', '<code>', 1).replace('`', '</code>', 1)  # Inline code
            
            story.append(Paragraph(text, style))
            story.append(Spacer(1, 12))

        # Build the PDF
        doc.build(story)
        buffer.seek(0)
        return buffer

    except Exception as e:
        st.error(f"Error generating PDF: {str(e)}")
        return None


# Set page config for a cleaner look
st.set_page_config(
    page_title="Compactor - Document Analysis",
    page_icon="📚",
    layout="wide"
)

# Add custom CSS for modern styling
# Remove or comment out the .api-key-section CSS class in the styling section
st.markdown("""
<style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .main-header {
        text-align: center;
        padding: 2rem 0;
    }
    .upload-section {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<div class="main-header"><h1>📚 Compactor</h1></div>', unsafe_allow_html=True)
#st.markdown('*AI-powered document analysis and synthesis system*')

# Initialize session state
if 'api_key_validated' not in st.session_state:
    st.session_state.api_key_validated = False
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = []
if 'urls' not in st.session_state:
    st.session_state.urls = []
if 'generated_report' not in st.session_state:
    st.session_state.generated_report = None

# API Key validation
def validate_api_key(api_key):
    if not api_key or not api_key.strip():
        return False, "API key cannot be empty"
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')
        # Test the API key with a simple generation request
        response = model.generate_content("Test")
        if response:
            return True, "API key is valid"
        return False, "Unable to generate content with the provided API key"
    except Exception as e:
        error_message = str(e).lower()
        if "invalid api key" in error_message:
            return False, "Invalid API key format"
        elif "unauthorized" in error_message:
            return False, "Invalid API key: unauthorized access"
        else:
            return False, f"API key validation failed: {str(e)}"

# Show API key input if not validated
if not st.session_state.api_key_validated:
    st.markdown("<h3 style='text-align: center; margin-bottom: 2rem;'>Your AI-powered document analysis and synthesis system</h3>", unsafe_allow_html=True)
    api_key = st.text_input("Enter your Gemini API Key", type="password", help="Get your API key from Google AI Studio")
    if st.button("Submit", key="submit_api_key"):
        is_valid, message = validate_api_key(api_key)
        if is_valid:
            st.session_state.api_key_validated = True
            os.environ["GEMINI_API_KEY"] = api_key
            st.rerun()
        else:
            st.error(message)
    st.stop()

# Only show the rest of the interface if API key is validated
if st.session_state.api_key_validated:
    # File upload section
    st.markdown('## 📎 Upload Documents')
    col1, col2 = st.columns(2)

    with col1:
        uploaded_files = st.file_uploader(
            "Drop PDF files here or click to browse",
            type=["pdf"],
            accept_multiple_files=True,
            help="Currently supporting PDF files"
        )

    with col2:
        urls = st.text_area(
            "Enter URLs (one per line)",
            height=150,
            help="Add URLs containing relevant information"
        )

    # User input section
    st.markdown('## 💭 Your Thoughts')
    col3, col4 = st.columns(2)

    with col3:
        intuition = st.text_area(
            "Share your intuitions",
            height=150,
            help="What are your initial thoughts or hypotheses?"
        )

    with col4:
        questions = st.text_area(
            "Ask questions",
            height=150,
            help="What specific questions would you like answered?"
        )

    # Process button
    if st.button("Generate Report", type="primary"):
        if not (uploaded_files or urls.strip()):
            st.error("Please provide at least one document or URL to analyze")
        else:
            with st.spinner("Analyzing documents and generating report..."):
                # Save uploaded files to temporary location
                temp_files = []
                if uploaded_files:
                    for file in uploaded_files:
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                            tmp_file.write(file.getvalue())
                            temp_files.append(tmp_file.name)

                # Process URLs
                url_list = [url.strip() for url in urls.split('\n') if url.strip()]

                # Prepare sources string
                sources = []
                sources.extend([f"PDF: {os.path.basename(f)}" for f in temp_files])
                sources.extend([f"URL: {url}" for url in url_list])
                sources_str = '\n'.join(sources)

                # Initialize and run the crew
                crew = Compactor(os.environ["GEMINI_API_KEY"])
                result = crew.crew().kickoff(
                    inputs={
                        "sources": sources_str,
                        "intuition": intuition,
                        "questions": questions
                    }
                )
                
                # Store the generated report in session state
                st.session_state.generated_report = str(result).replace("```md","").replace("```","")

                # Display the report
                st.markdown("## 📊 Analysis Report")
                st.markdown(str(result))

                # Cleanup temporary files
                for temp_file in temp_files:
                    try:
                        os.unlink(temp_file)
                    except:
                        pass

    # Add PDF export button if report is generated
    if st.session_state.generated_report:
        if st.button("Export to PDF", type="secondary"):
            with st.spinner("Converting to PDF..."):
                md = str(st.session_state.generated_report)
                try:
                    # Get the PDF buffer
                    pdf_buffer = markdown_to_pdf(md)

                    # Create download button
                    st.download_button(
                        label="Download PDF",
                        data=pdf_buffer,
                        file_name="compactor_report.pdf",
                        mime="application/pdf"
                    )
                    
                    # Close the buffer to free up resources
                    pdf_buffer.close()
                except Exception as e:
                    st.error(f"Error converting to PDF: {str(e)}")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <small>Powered by CrewAI and Streamlit</small>
    </div>
    """, unsafe_allow_html=True)