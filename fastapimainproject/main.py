import streamlit as st
from pathlib import Path
import shutil
from utilities import (
    convert_docx_to_txt, convert_pdf_to_txt, extract_phone_number, 
    extract_email, extract_skills, load_skills, get_tokens, likely_name
)
import logging

# Configure logging
logging.basicConfig(level=logging.ERROR, filename='error.log', 
                    format='%(asctime)s %(levelname)s:%(message)s')

UPLOAD_FOLDER = Path('uploads')
UPLOAD_FOLDER.mkdir(exist_ok=True)
skills_list = load_skills()

def save_upload_file(upload_file):
    try:
        if not upload_file.name.endswith(('.docx', '.pdf')):
            st.sidebar.error("Unsupported file type")
            return None
        file_path = UPLOAD_FOLDER / upload_file.name
        with open(file_path, "wb") as buffer:
            buffer.write(upload_file.getbuffer())
        return file_path
    except Exception as e:
        logging.error(f"Error saving file: {e}")
        st.sidebar.error("Error saving file.")
        return None

def process_file(file_path):
    try:
        if file_path.name.endswith('.docx'):
            text = convert_docx_to_txt(str(file_path))
        elif file_path.name.endswith('.pdf'):
            text = convert_pdf_to_txt(str(file_path))

        tokens = get_tokens(text)
        username = likely_name(tokens)
        matched_skills = extract_skills(text, skills_list)
        phone_number = extract_phone_number(text)
        email = extract_email(text)

        return {
            "name": username, 
            "skillset": [skill for skill in matched_skills if len(skill) > 1 and not skill.isdigit()],
            "phone number": phone_number,
            "email": email
        }
    except Exception as e:
        logging.error(f"Error processing file: {e}")
        st.error("Error processing file.")
        return {}

def display_results(results):
    st.subheader('Processed Resume Details')
    st.text(f"Name: {results['name']}")
    st.text(f"Phone Number: {results['phone number']}")
    st.text(f"Email: {results['email']}")
    st.subheader('Skillset')
    st.write(", ".join(results['skillset']))

def main():
    st.sidebar.title('Resume Upload')
    uploaded_file = st.sidebar.file_uploader("Choose a file", type=['docx', 'pdf'])
    
    st.title('Resume Parser')
    if uploaded_file is not None:
        file_path = save_upload_file(uploaded_file)
        if file_path:
            results = process_file(file_path)
            if results:
                st.success("File processed successfully")
                display_results(results)

if __name__ == "__main__":
    main()
