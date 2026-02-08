import streamlit as st
import PyPDF2
from pdf2docx import Converter
import os
import tempfile
from io import BytesIO

# Page configuration
st.set_page_config(
    page_title="Pure PDF | Simplified Performance",
    page_icon="📄",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #667eea;
        padding: 20px;
    }
    .stButton>button {
        width: 100%;
        height: 60px;
        font-size: 18px;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">Pure PDF | Simplified Performance</h1>', unsafe_allow_html=True)
st.markdown("---")

# Initialize session state for tracking operations
if 'operation' not in st.session_state:
    st.session_state.operation = None

# PDF Validation Function
def validate_pdf(file):
    """Validate that the uploaded file is a valid PDF"""
    try:
        PyPDF2.PdfReader(file)
        return True, "Valid PDF"
    except Exception as e:
        return False, f"Invalid PDF: {str(e)}"

# PDF Operations Functions

def merge_pdfs(pdf_files):
    """Merge multiple PDF files into a single PDF"""
    try:
        merger = PyPDF2.PdfMerger()
        for pdf_file in pdf_files:
            merger.append(pdf_file)
        
        output = BytesIO()
        merger.write(output)
        output.seek(0)
        return output, None
    except Exception as e:
        return None, f"Error merging PDFs: {str(e)}"

def delete_pages(pdf_file, pages_to_delete):
    """Delete specified pages from a PDF"""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        pdf_writer = PyPDF2.PdfWriter()
        
        total_pages = len(pdf_reader.pages)
        
        # Validate page numbers
        for page in pages_to_delete:
            if page < 1 or page > total_pages:
                return None, f"Page {page} is out of range (1-{total_pages})"
        
        for page_num in range(total_pages):
            if (page_num + 1) not in pages_to_delete:
                pdf_writer.add_page(pdf_reader.pages[page_num])
        
        output = BytesIO()
        pdf_writer.write(output)
        output.seek(0)
        return output, None
    except Exception as e:
        return None, f"Error deleting pages: {str(e)}"

def reorder_pages(pdf_file, page_order):
    """Reorder pages of a PDF"""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        pdf_writer = PyPDF2.PdfWriter()
        
        total_pages = len(pdf_reader.pages)
        
        # Validate page numbers
        for page in page_order:
            if page < 1 or page > total_pages:
                return None, f"Page {page} is out of range (1-{total_pages})"
        
        for page_num in page_order:
            pdf_writer.add_page(pdf_reader.pages[page_num - 1])
        
        output = BytesIO()
        pdf_writer.write(output)
        output.seek(0)
        return output, None
    except Exception as e:
        return None, f"Error reordering pages: {str(e)}"

def pdf_to_word(pdf_file):
    """Convert a PDF to Word format"""
    try:
        # Create temporary files
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_pdf:
            tmp_pdf.write(pdf_file.read())
            tmp_pdf_path = tmp_pdf.name
        
        tmp_docx_path = tempfile.mktemp(suffix='.docx')
        
        # Convert
        converter = Converter(tmp_pdf_path)
        converter.convert(tmp_docx_path, start=0, end=None)
        converter.close()
        
        # Read the output
        with open(tmp_docx_path, 'rb') as f:
            output = BytesIO(f.read())
        
        # Cleanup
        os.unlink(tmp_pdf_path)
        os.unlink(tmp_docx_path)
        
        output.seek(0)
        return output, None
    except Exception as e:
        return None, f"Error converting to Word: {str(e)}"

def protect_pdf(pdf_file, password):
    """Add password protection to a PDF"""
    try:
        if not password or len(password) < 4:
            return None, "Password must be at least 4 characters"
        
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        pdf_writer = PyPDF2.PdfWriter()
        
        for page in pdf_reader.pages:
            pdf_writer.add_page(page)
        
        pdf_writer.encrypt(password)
        
        output = BytesIO()
        pdf_writer.write(output)
        output.seek(0)
        return output, None
    except Exception as e:
        return None, f"Error protecting PDF: {str(e)}"

def rotate_pages(pdf_file, pages_to_rotate, rotation_angle):
    """Rotate specified pages in a PDF"""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        pdf_writer = PyPDF2.PdfWriter()
        
        total_pages = len(pdf_reader.pages)
        
        # Validate page numbers
        for page in pages_to_rotate:
            if page < 1 or page > total_pages:
                return None, f"Page {page} is out of range (1-{total_pages})"
        
        for page_num in range(total_pages):
            page = pdf_reader.pages[page_num]
            if (page_num + 1) in pages_to_rotate:
                page.rotate(rotation_angle)
            pdf_writer.add_page(page)
        
        output = BytesIO()
        pdf_writer.write(output)
        output.seek(0)
        return output, None
    except Exception as e:
        return None, f"Error rotating pages: {str(e)}"

def extract_pages(pdf_file, pages_to_extract):
    """Extract specified pages from a PDF"""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        pdf_writer = PyPDF2.PdfWriter()
        
        total_pages = len(pdf_reader.pages)
        
        # Validate page numbers
        for page in pages_to_extract:
            if page < 1 or page > total_pages:
                return None, f"Page {page} is out of range (1-{total_pages})"
        
        for page_num in pages_to_extract:
            pdf_writer.add_page(pdf_reader.pages[page_num - 1])
        
        output = BytesIO()
        pdf_writer.write(output)
        output.seek(0)
        return output, None
    except Exception as e:
        return None, f"Error extracting pages: {str(e)}"

def add_watermark(pdf_file, watermark_file):
    """Add a watermark to each page of a PDF"""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        watermark_reader = PyPDF2.PdfReader(watermark_file)
        watermark_page = watermark_reader.pages[0]
        
        pdf_writer = PyPDF2.PdfWriter()
        
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            page.merge_page(watermark_page)
            pdf_writer.add_page(page)
        
        output = BytesIO()
        pdf_writer.write(output)
        output.seek(0)
        return output, None
    except Exception as e:
        return None, f"Error adding watermark: {str(e)}"

# Main UI - Tool Selection
st.subheader("Select a Tool")

# Create columns for tool buttons
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📄 Merge PDFs", use_container_width=True):
        st.session_state.operation = "merge"
    if st.button("🔄 Reorder Pages", use_container_width=True):
        st.session_state.operation = "reorder"
    if st.button("🔒 Protect PDF", use_container_width=True):
        st.session_state.operation = "protect"

with col2:
    if st.button("✂️ Delete Pages", use_container_width=True):
        st.session_state.operation = "delete"
    if st.button("📝 Convert to Word", use_container_width=True):
        st.session_state.operation = "convert"
    if st.button("🔃 Rotate Pages", use_container_width=True):
        st.session_state.operation = "rotate"

with col3:
    if st.button("📋 Extract Pages", use_container_width=True):
        st.session_state.operation = "extract"
    if st.button("💧 Add Watermark", use_container_width=True):
        st.session_state.operation = "watermark"

st.markdown("---")

# Operation-specific UI
if st.session_state.operation == "merge":
    st.header("Merge PDFs")
    uploaded_files = st.file_uploader("Select PDF files to merge", type="pdf", accept_multiple_files=True)
    
    if uploaded_files and len(uploaded_files) > 1:
        if st.button("Merge Files", type="primary"):
            with st.spinner("Merging PDFs..."):
                output, error = merge_pdfs(uploaded_files)
                if error:
                    st.error(error)
                else:
                    st.success("PDFs merged successfully!")
                    st.download_button(
                        label="📥 Download Merged PDF",
                        data=output,
                        file_name="merged.pdf",
                        mime="application/pdf"
                    )
    elif uploaded_files and len(uploaded_files) == 1:
        st.warning("Please upload at least 2 PDF files to merge")

elif st.session_state.operation == "delete":
    st.header("Delete Pages")
    uploaded_file = st.file_uploader("Select PDF file", type="pdf")
    
    if uploaded_file:
        pages_input = st.text_input("Enter page numbers to delete (comma-separated)", placeholder="e.g., 1,3,5")
        
        if pages_input and st.button("Delete Pages", type="primary"):
            try:
                pages = [int(p.strip()) for p in pages_input.split(',')]
                with st.spinner("Deleting pages..."):
                    output, error = delete_pages(uploaded_file, pages)
                    if error:
                        st.error(error)
                    else:
                        st.success("Pages deleted successfully!")
                        st.download_button(
                            label="📥 Download Modified PDF",
                            data=output,
                            file_name="deleted_pages.pdf",
                            mime="application/pdf"
                        )
            except ValueError:
                st.error("Invalid page numbers. Please use comma-separated numbers (e.g., 1,3,5)")

elif st.session_state.operation == "reorder":
    st.header("Reorder Pages")
    uploaded_file = st.file_uploader("Select PDF file", type="pdf")
    
    if uploaded_file:
        order_input = st.text_input("Enter new page order (comma-separated)", placeholder="e.g., 3,1,2,4")
        
        if order_input and st.button("Reorder Pages", type="primary"):
            try:
                order = [int(p.strip()) for p in order_input.split(',')]
                with st.spinner("Reordering pages..."):
                    output, error = reorder_pages(uploaded_file, order)
                    if error:
                        st.error(error)
                    else:
                        st.success("Pages reordered successfully!")
                        st.download_button(
                            label="📥 Download Reordered PDF",
                            data=output,
                            file_name="reordered.pdf",
                            mime="application/pdf"
                        )
            except ValueError:
                st.error("Invalid page order. Please use comma-separated numbers (e.g., 3,1,2,4)")

elif st.session_state.operation == "convert":
    st.header("Convert PDF to Word")
    uploaded_file = st.file_uploader("Select PDF file", type="pdf")
    
    if uploaded_file and st.button("Convert to Word", type="primary"):
        with st.spinner("Converting to Word (this may take a while)..."):
            output, error = pdf_to_word(uploaded_file)
            if error:
                st.error(error)
            else:
                st.success("PDF converted to Word successfully!")
                st.download_button(
                    label="📥 Download Word Document",
                    data=output,
                    file_name="converted.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )

elif st.session_state.operation == "protect":
    st.header("Protect PDF with Password")
    uploaded_file = st.file_uploader("Select PDF file", type="pdf")
    
    if uploaded_file:
        password = st.text_input("Enter password (minimum 4 characters)", type="password")
        
        if password and st.button("Protect PDF", type="primary"):
            with st.spinner("Adding password protection..."):
                output, error = protect_pdf(uploaded_file, password)
                if error:
                    st.error(error)
                else:
                    st.success("PDF password protected successfully!")
                    st.download_button(
                        label="📥 Download Protected PDF",
                        data=output,
                        file_name="protected.pdf",
                        mime="application/pdf"
                    )

elif st.session_state.operation == "rotate":
    st.header("Rotate Pages")
    uploaded_file = st.file_uploader("Select PDF file", type="pdf")
    
    if uploaded_file:
        pages_input = st.text_input("Enter page numbers to rotate (comma-separated)", placeholder="e.g., 1,3,5")
        rotation = st.selectbox("Select rotation angle", [90, 180, 270])
        
        if pages_input and st.button("Rotate Pages", type="primary"):
            try:
                pages = [int(p.strip()) for p in pages_input.split(',')]
                with st.spinner("Rotating pages..."):
                    output, error = rotate_pages(uploaded_file, pages, rotation)
                    if error:
                        st.error(error)
                    else:
                        st.success("Pages rotated successfully!")
                        st.download_button(
                            label="📥 Download Rotated PDF",
                            data=output,
                            file_name="rotated.pdf",
                            mime="application/pdf"
                        )
            except ValueError:
                st.error("Invalid page numbers. Please use comma-separated numbers (e.g., 1,3,5)")

elif st.session_state.operation == "extract":
    st.header("Extract Pages")
    uploaded_file = st.file_uploader("Select PDF file", type="pdf")
    
    if uploaded_file:
        pages_input = st.text_input("Enter page numbers to extract (comma-separated)", placeholder="e.g., 1,3,5")
        
        if pages_input and st.button("Extract Pages", type="primary"):
            try:
                pages = [int(p.strip()) for p in pages_input.split(',')]
                with st.spinner("Extracting pages..."):
                    output, error = extract_pages(uploaded_file, pages)
                    if error:
                        st.error(error)
                    else:
                        st.success("Pages extracted successfully!")
                        st.download_button(
                            label="📥 Download Extracted PDF",
                            data=output,
                            file_name="extracted.pdf",
                            mime="application/pdf"
                        )
            except ValueError:
                st.error("Invalid page numbers. Please use comma-separated numbers (e.g., 1,3,5)")

elif st.session_state.operation == "watermark":
    st.header("Add Watermark")
    uploaded_file = st.file_uploader("Select PDF file", type="pdf", key="main_pdf")
    watermark_file = st.file_uploader("Select Watermark PDF", type="pdf", key="watermark_pdf")
    
    if uploaded_file and watermark_file and st.button("Add Watermark", type="primary"):
        with st.spinner("Adding watermark..."):
            output, error = add_watermark(uploaded_file, watermark_file)
            if error:
                st.error(error)
            else:
                st.success("Watermark added successfully!")
                st.download_button(
                    label="📥 Download Watermarked PDF",
                    data=output,
                    file_name="watermarked.pdf",
                    mime="application/pdf"
                )

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: gray; font-size: 14px;'>
        <p>Pure PDF | Version 5.0 (Web Version)</p>
        <p>Developed by JS</p>
        <p style="font-size: 12px;">
            🔒 Files are processed only during your session and are not permanently stored. All uploaded files are deleted when the session ends.
        </p>
    </div>
""", unsafe_allow_html=True)




