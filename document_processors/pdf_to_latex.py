import pdfplumber
import re
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clean_text(text):
    """
    Clean extracted text by handling common PDF extraction artifacts.
    
    Args:
        text (str): Raw text extracted from PDF
        
    Returns:
        str: Cleaned text
    """
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)
    
    # Handle hyphenated words at line breaks
    text = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', text)
    
    # Remove isolated numbers that might be page numbers
    text = re.sub(r'\n\s*\d+\s*\n', '\n', text)
    
    return text.strip()

def pdf_to_latex(pdf_path, output_path=None):
    """
    Convert PDF to LaTeX format, attempting to preserve structure and formatting.
    
    Args:
        pdf_path (str): Path to input PDF file
        output_path (str, optional): Path for output LaTeX file. If None, uses PDF name with .tex extension
        
    Returns:
        tuple: (success: bool, message: str, output_path: str)
    """
    try:
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            return False, f"PDF file not found: {pdf_path}", None

        if output_path is None:
            output_path = pdf_path.with_suffix('.tex')
        
        latex_content = []
        latex_content.append("\\documentclass{article}")
        latex_content.append("\\usepackage[utf8]{inputenc}")
        latex_content.append("\\usepackage{amsmath}")
        latex_content.append("\\usepackage{graphicx}")
        latex_content.append("\\begin{document}")
        
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                # Extract text and tables
                text = page.extract_text()
                tables = page.extract_tables()
                
                if text:
                    text = clean_text(text)
                    
                    # Attempt to identify and convert sections
                    sections = text.split('\n')
                    for section in sections:
                        # Check for potential headers
                        if re.match(r'^[0-9.]*\s*[A-Z][^.!?]*$', section.strip()):
                            latex_content.append(f"\n\\section{{{section.strip()}}}")
                        else:
                            # Regular paragraph
                            latex_content.append(f"\n{section}")
                
                # Convert tables to LaTeX format
                if tables:
                    for table in tables:
                        if table:
                            latex_content.append("\\begin{table}[h!]")
                            latex_content.append("\\begin{tabular}{" + "l" * len(table[0]) + "}")
                            
                            for row in table:
                                # Clean and escape special characters
                                cleaned_row = [str(cell).replace('_', '\\_').replace('%', '\\%') if cell else '' for cell in row]
                                latex_content.append(" & ".join(cleaned_row) + " \\\\")
                            
                            latex_content.append("\\end{tabular}")
                            latex_content.append("\\end{table}")
        
        latex_content.append("\\end{document}")
        
        # Write to output file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(latex_content))
        
        return True, f"Successfully converted PDF to LaTeX: {output_path}", str(output_path)
    
    except Exception as e:
        error_msg = f"Error converting PDF to LaTeX: {str(e)}"
        logger.error(error_msg)
        return False, error_msg, None

def main():
    """
    Command line interface for PDF to LaTeX conversion.
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='Convert PDF to LaTeX format')
    parser.add_argument('pdf_path', help='Path to input PDF file')
    parser.add_argument('--output', '-o', help='Path for output LaTeX file (optional)')
    
    args = parser.parse_args()
    
    success, message, output_path = pdf_to_latex(args.pdf_path, args.output)
    if success:
        logger.info(message)
    else:
        logger.error(message)

if __name__ == '__main__':
    main() 