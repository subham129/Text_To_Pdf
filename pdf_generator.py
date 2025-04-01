from fpdf import FPDF
import textwrap
import io
import tempfile
import os
import unicodedata
import re

def generate_pdf(
    text_content,
    font="Helvetica",
    font_size=12,
    font_color=(0, 0, 0),
    alignment="left",
    page_size="A4",
    margin=20,
    orientation="portrait",
    line_spacing=1.15
):
    """
    Generate a PDF document with the given text and formatting options.
    
    Args:
        text_content (str): The text to include in the PDF
        font (str): Font family to use
        font_size (int): Font size in points
        font_color (tuple): RGB color tuple (0-255, 0-255, 0-255)
        alignment (str): Text alignment (left, center, right)
        page_size (str): Page size (A4, Letter, Legal)
        margin (int): Page margin in mm
        orientation (str): Page orientation (portrait, landscape)
        line_spacing (float): Line spacing multiplier
        
    Returns:
        bytes: The generated PDF as bytes
    """
    
    # Handle special characters by replacing them with ASCII alternatives
    def clean_text(text):
        # Replace common special characters with ASCII alternatives
        replacements = {
            '✓': 'v',    # Check mark
            '✗': 'x',    # X mark
            '→': '->',   # Right arrow
            '←': '<-',   # Left arrow
            '•': '*',    # Bullet point
            '…': '...',  # Ellipsis
            '—': '-',    # Em dash
            '–': '-',    # En dash
            '"': '"',    # Smart quotes
            '"': '"',    # Smart quotes
            ''': "'",    # Smart quotes
            ''': "'",    # Smart quotes
        }
        
        for special, replacement in replacements.items():
            text = text.replace(special, replacement)
        
        # For any remaining special characters, normalize to ASCII
        text = unicodedata.normalize('NFKD', text)
        # Replace any remaining non-ASCII characters
        text = re.sub(r'[^\x00-\x7F]+', '', text)
        
        return text
    
    # Clean the text content to ensure compatibility
    text_content = clean_text(text_content)
    
    # Create a new PDF object with proper orientation and format
    if orientation.lower().startswith('p'):
        pdf_orientation = 'P'  # Portrait
    else:
        pdf_orientation = 'L'  # Landscape
        
    pdf = FPDF(orientation=pdf_orientation, unit='mm', format=page_size.upper())
    
    # Add a page
    pdf.add_page()
    
    # Set margins
    pdf.set_margins(margin, margin, margin)
    
    # Set font
    pdf.set_font(font, size=font_size)
    
    # Set text color
    r, g, b = font_color
    pdf.set_text_color(r, g, b)
    
    # Calculate effective width (page width minus margins)
    effective_width = pdf.w - 2 * margin
    
    # Set the line height based on font size and line spacing
    line_height = font_size * 0.352778 * line_spacing  # Convert pt to mm and apply spacing
    
    # Set alignment
    if alignment.lower() == "left":
        align = "L"
    elif alignment.lower() == "center":
        align = "C"
    elif alignment.lower() == "right":
        align = "R"
    else:
        align = "L"  # Default to left
    
    # Calculate how many characters can fit in a line
    avg_char_width = pdf.get_string_width('A')  # Use 'A' as average character width estimation
    chars_per_line = int(effective_width / avg_char_width * 1.8)  # Adjusted for better estimation
    
    # Wrap the text to fit within the effective width
    lines = []
    for paragraph in text_content.split('\n'):
        if paragraph.strip() == '':
            lines.append('')  # Preserve empty paragraphs
        else:
            wrapped_lines = textwrap.wrap(paragraph, width=chars_per_line)
            lines.extend(wrapped_lines)
    
    # Write the text to the PDF
    for line in lines:
        if line == '':
            pdf.ln(line_height)  # Add empty line
        else:
            pdf.cell(w=effective_width, h=line_height, txt=line, ln=1, align=align)
    
    # Create a temporary file to save the PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
        temp_file_path = temp_file.name
    
    # Output the PDF to the temporary file
    pdf.output(temp_file_path)
    
    # Read the file into memory
    with open(temp_file_path, 'rb') as file:
        pdf_bytes = file.read()
    
    # Clean up the temporary file
    os.unlink(temp_file_path)
    
    return pdf_bytes
