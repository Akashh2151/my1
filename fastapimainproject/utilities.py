import re
import docx
import fitz

def is_title(token):
    titles = {'Mr.', 'Mrs.', 'Ms.', 'Dr.', 'Prof.', 'Sir'}
    return token in titles

def likely_name(tokens):
    name_tokens = []
    for token in tokens:
        if not is_title(token):
            name_tokens.append(token)
    return ' '.join(name_tokens[:2]) if name_tokens else "Unknown"

def get_tokens(doc):
    tokens = re.split(r"\b[^A-Za-z.']+\b", doc)
    return [token.strip() for token in tokens if token.strip()]

def convert_docx_to_txt(doc_file):
    doc = docx.Document(doc_file)
    return '\n'.join([para.text for para in doc.paragraphs if para.text != ""])

def convert_pdf_to_txt(pdf_file):
    doc = fitz.open(pdf_file)
    return ''.join([page.get_text() for page in doc])

def extract_phone_number(text):
    phone_pattern = re.compile(r'(\(?\+\d+\)?[\s-]?\d+[\s-]?\d+[\s-]?\d+)|(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})|(\b\d{10}\b)')
    match = phone_pattern.search(text)
    return match.group(0) if match else "No phone number found"

def extract_email(text):
    email_pattern = re.compile(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+')
    match = email_pattern.search(text)
    return match.group(0) if match else "No email found"

def extract_skills(text, skills_list):
    return set(skill for skill in skills_list if re.search(r"\b" + re.escape(skill) + r"\b", text, re.IGNORECASE))

def load_skills():
    with open("all_linked_skills.txt", "r") as f:
        return f.read().splitlines()
