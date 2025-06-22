# pdf_utils.py
import pdfplumber

def extract_text_from_pdf(file, max_pages=30):
    text = ""
    with pdfplumber.open(file) as pdf:
        total_pages = min(len(pdf.pages), max_pages)
        for i in range(total_pages):
            page = pdf.pages[i]
            text += page.extract_text() + "\n"
    return text
