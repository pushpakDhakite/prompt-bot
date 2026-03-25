"""
Input Processor - Handles different types of input (text, PDF, images, URLs)
"""

import os
import json
from pathlib import Path

class InputProcessor:
    def __init__(self):
        self.supported_extensions = {
            '.txt': 'text',
            '.pdf': 'pdf',
            '.jpg': 'image',
            '.jpeg': 'image',
            '.png': 'image',
            '.gif': 'image',
            '.doc': 'document',
            '.docx': 'document',
            '.md': 'markdown',
            '.json': 'json',
            '.csv': 'csv'
        }
    
    def process_file(self, filepath, filename):
        """Process a file and extract its content"""
        ext = os.path.splitext(filename)[1].lower()
        
        if ext == '.txt':
            return self._process_text_file(filepath)
        elif ext == '.pdf':
            return self._process_pdf_file(filepath)
        elif ext in ['.jpg', '.jpeg', '.png', '.gif']:
            return self._process_image_file(filepath)
        elif ext in ['.doc', '.docx']:
            return self._process_document_file(filepath)
        elif ext == '.md':
            return self._process_markdown_file(filepath)
        elif ext == '.json':
            return self._process_json_file(filepath)
        elif ext == '.csv':
            return self._process_csv_file(filepath)
        else:
            return self._process_text_file(filepath)
    
    def process_url(self, url):
        """Process a URL and extract content"""
        try:
            # For now, return a placeholder
            # In production, you'd use requests and beautifulsoup
            return f"Content from URL: {url}\n\n[Note: URL content extraction would require additional libraries. This is a placeholder for demonstration.]"
        except Exception as e:
            return f"Error processing URL: {str(e)}"
    
    def _process_text_file(self, filepath):
        """Process a plain text file"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            return content[:10000]  # Limit to 10k chars
        except Exception as e:
            return f"Error reading text file: {str(e)}"
    
    def _process_pdf_file(self, filepath):
        """Process a PDF file"""
        try:
            # Try to import PyPDF2
            try:
                import PyPDF2
                with open(filepath, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text() + "\n"
                    return text[:10000]  # Limit to 10k chars
            except ImportError:
                return "[PDF processing requires PyPDF2 library. Content extraction simulated.]"
        except Exception as e:
            return f"Error processing PDF: {str(e)}"
    
    def _process_image_file(self, filepath):
        """Process an image file (simulated OCR)"""
        try:
            # For demo purposes, return description
            filename = os.path.basename(filepath)
            return f"Image file: {filename}\n\n[Note: Image content extraction would require OCR libraries like pytesseract. This is a placeholder for demonstration.]"
        except Exception as e:
            return f"Error processing image: {str(e)}"
    
    def _process_document_file(self, filepath):
        """Process a Word document"""
        try:
            # For demo purposes
            return f"Document file: {os.path.basename(filepath)}\n\n[Note: Document content extraction would require python-docx library. This is a placeholder for demonstration.]"
        except Exception as e:
            return f"Error processing document: {str(e)}"
    
    def _process_markdown_file(self, filepath):
        """Process a markdown file"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            return content[:10000]
        except Exception as e:
            return f"Error reading markdown file: {str(e)}"
    
    def _process_json_file(self, filepath):
        """Process a JSON file"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                data = json.load(f)
            # Convert to readable format
            return json.dumps(data, indent=2)[:10000]
        except Exception as e:
            return f"Error reading JSON file: {str(e)}"
    
    def _process_csv_file(self, filepath):
        """Process a CSV file"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            # Return first 100 lines
            return "".join(lines[:100])
        except Exception as e:
            return f"Error reading CSV file: {str(e)}"
    
    def detect_input_type(self, filename):
        """Detect input type from filename"""
        ext = os.path.splitext(filename)[1].lower()
        return self.supported_extensions.get(ext, 'text')
    
    def validate_file(self, filename):
        """Validate if file type is supported"""
        ext = os.path.splitext(filename)[1].lower()
        return ext in self.supported_extensions