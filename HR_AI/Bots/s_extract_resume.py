import re
import pdfplumber
import docx

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()

def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    return "\n".join([para.text for para in doc.paragraphs]).strip()

def extract_links(text):
    url_pattern = r"https?://[a-zA-Z0-9./_-]+"
    links = re.findall(url_pattern, text)
    return list(set(links))  # Remove duplicates

def extract_resume_info(file_path):
    if file_path.endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        text = extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file format")
    
    links = extract_links(text)
    return links

if __name__ == "__main__":
    resume_path = "Input/s_Resume.pdf"  # Update with your actual resume file
    extracted_links = extract_resume_info(resume_path)
    print("Extracted Links:", extracted_links)