from crewai.tools import BaseTool
from typing import Type, List
from pydantic import BaseModel, Field, PrivateAttr

import PyPDF2

class PdfReaderToolInput(BaseModel):
    """Input schema for PDF to Text conversion tool."""
    pdf_path: str = Field(..., description="Path to the PDF file to read")

class PdfReaderTool(BaseTool):
    name: str = "PDF reader"
    description: str = (
        "Read a PDF file and return its content"
    )
    args_schema: Type[BaseModel] = PdfReaderToolInput

    def _run(self, pdf_path: str) -> str:
        """Convert PDF to text with comprehensive error handling."""
        try:
            # Read PDF file
            with open(pdf_path, 'rb') as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                
                # Extract text from all pages
                text = []
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:  # Handle empty pages
                        text.append(page_text)
                
                if not text:  # Handle PDFs with no extractable text
                    return("PDF contains no extractable text (might be scanned/image-based)")
                
                return '\n'.join(text)
                
        except FileNotFoundError:
            return(f"File not found: {pdf_path}")
        except PermissionError:
            return(f"Permission denied for file: {pdf_path}")
        except PyPDF2.errors.PdfReadError:
            return("Invalid or corrupted PDF file")
        except Exception as e:
            return(f"Conversion failed: {str(e)}")


