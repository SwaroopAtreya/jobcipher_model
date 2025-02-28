import fitz  # PyMuPDF for better PDF parsing
from docx import Document

def extract_text_with_layout(file_path):
    """Extract text with better layout preservation"""
    if file_path.endswith(".pdf"):
        # Use PyMuPDF for better PDF parsing
        doc = fitz.open(file_path)
        text = ""

        for page in doc:
            text += page.get_text("text")

    elif file_path.endswith(".docx"):
        # Extract with paragraph and section awareness
        doc = Document(file_path)

        sections = []
        current_section = ""

        for para in doc.paragraphs:
            # Check if this is a section header (often formatted differently)
            if para.style.name.startswith('Heading'):
                if current_section:
                    sections.append(current_section.strip())
                current_section = para.text + "\n"
            else:
                current_section += para.text + "\n"

        if current_section:
            sections.append(current_section.strip())

        text = "\n\n".join(sections)

    else:
        raise ValueError("Unsupported file format. Use PDF or DOCX.")

    return text