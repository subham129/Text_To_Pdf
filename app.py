import streamlit as st
import os
import tempfile
import base64
from pdf_generator import generate_pdf

def main():
    st.title("Text to PDF Converter")
    st.markdown("Enter your text and customize formatting to generate a PDF document.")
    
    # Text input area
    st.subheader("Text Content")
    text_content = st.text_area("Enter your text here:", height=200)
    
    # Formatting options
    st.subheader("Formatting Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Font options
        font_options = ["Helvetica", "Times-Roman", "Courier", "Arial"]
        selected_font = st.selectbox("Select Font:", font_options)
        
        # Font size options
        font_size_options = [8, 10, 12, 14, 16, 18, 20, 22, 24]
        selected_font_size = st.selectbox("Select Font Size:", font_size_options, index=2)  # Default to 12
        
    with col2:
        # Font color options
        font_color_options = {
            "Black": (0, 0, 0),
            "Red": (255, 0, 0),
            "Blue": (0, 0, 255),
            "Green": (0, 128, 0),
            "Gray": (128, 128, 128)
        }
        selected_font_color_name = st.selectbox("Select Font Color:", list(font_color_options.keys()))
        selected_font_color = font_color_options[selected_font_color_name]
        
        # Alignment options
        alignment_options = ["Left", "Center", "Right"]
        selected_alignment = st.selectbox("Select Text Alignment:", alignment_options)
    
    # Page options
    st.subheader("Page Options")
    col3, col4 = st.columns(2)
    
    with col3:
        page_size_options = ["A4", "Letter", "Legal"]
        selected_page_size = st.selectbox("Select Page Size:", page_size_options)
        
        margin_options = [10, 15, 20, 25, 30]
        selected_margin = st.selectbox("Select Margin (mm):", margin_options, index=2)  # Default to 20
    
    with col4:
        orientation_options = ["Portrait", "Landscape"]
        selected_orientation = st.selectbox("Select Orientation:", orientation_options)
        
        line_spacing_options = [1.0, 1.15, 1.5, 2.0]
        selected_line_spacing = st.selectbox("Select Line Spacing:", line_spacing_options, index=1)  # Default to 1.15
    
    # Generate PDF button
    if st.button("Generate PDF"):
        if not text_content.strip():
            st.error("Please enter some text before generating the PDF.")
        else:
            try:
                with st.spinner("Generating PDF..."):
                    # Create PDF
                    pdf_bytes = generate_pdf(
                        text_content,
                        font=selected_font,
                        font_size=selected_font_size,
                        font_color=selected_font_color,
                        alignment=selected_alignment.lower(),
                        page_size=selected_page_size,
                        margin=selected_margin,
                        orientation=selected_orientation.lower(),
                        line_spacing=selected_line_spacing
                    )
                    
                    # Create a download link
                    b64_pdf = base64.b64encode(pdf_bytes).decode()
                    href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="converted_document.pdf">Download PDF</a>'
                    
                    # PDF Preview
                    st.subheader("PDF Preview & Download")
                    
                    # Create a temporary file to display the PDF
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                        tmp_file.write(pdf_bytes)
                        tmp_file_path = tmp_file.name
                    
                    # Display download link
                    st.markdown(href, unsafe_allow_html=True)
                    
                    # Display PDF preview using an iframe
                    pdf_display = f'<iframe src="data:application/pdf;base64,{b64_pdf}" width="100%" height="500" type="application/pdf"></iframe>'
                    st.markdown(pdf_display, unsafe_allow_html=True)
                    
                    # Clean up the temporary file
                    os.unlink(tmp_file_path)
                    
                    st.success("PDF generated successfully!")
                    
            except Exception as e:
                st.error(f"An error occurred while generating the PDF: {str(e)}")

    # Instructions
    with st.expander("Instructions"):
        st.markdown("""
        ### How to use this tool:
        1. Enter your text in the input area
        2. Select your preferred formatting options from the dropdowns
        3. Click 'Generate PDF' button
        4. Preview the generated PDF
        5. Download the PDF using the download link
        """)

if __name__ == "__main__":
    main()
