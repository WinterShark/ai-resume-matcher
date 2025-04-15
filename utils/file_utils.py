from io import StringIO
import PyPDF2
import docx

def save_uploaded_file(uploaded_file):
    """
    Extracts text from uploaded file (.pdf, .docx, .txt).

    Args:
        uploaded_file: The uploaded file.

    Returns:
        str: The extracted text content.
    """
    file_extension = uploaded_file.name.split('.')[-1].lower()

    if file_extension == 'pdf':
        return extract_pdf_text(uploaded_file)
    elif file_extension == 'docx':
        return extract_docx_text(uploaded_file)
    elif file_extension == 'txt':
        return uploaded_file.getvalue().decode("utf-8")
    else:
        raise ValueError("Unsupported file type")

def extract_pdf_text(file):
    """
    Extract text from PDF file.

    Args:
        file: The uploaded PDF file.

    Returns:
        str: The extracted text from the PDF.
    """
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_docx_text(file):
    """
    Extract text from DOCX file.

    Args:
        file: The uploaded DOCX file.

    Returns:
        str: The extracted text from the DOCX file.
    """
    doc = docx.Document(file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text
