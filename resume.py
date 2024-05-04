import streamlit as st
import spacy
import fitz  # PyMuPDF

# Load the pre-trained Spacy model
nlp = spacy.load(r'C:\Users\EMC\Desktop\resume\model\output\model-best')

def extract_text_from_pdf(file):
    file_stream = file.read()
    doc = fitz.open(stream=file_stream, filetype="pdf")
    text = " "
    for page in doc:
        text += page.get_text()
    return text

def extract_entities(text):
    doc = nlp(text)
    entities = {}
    for ent in doc.ents:
        if ent.label_ not in entities:
            entities[ent.label_] = ent.text
        else:
            # Add only unique entries for each entity type
            if ent.text not in entities[ent.label_]:
                entities[ent.label_] += "; " + ent.text
    return entities

def main():
    st.title("Resume Information Extractor")
    uploaded_file = st.sidebar.file_uploader("Upload your resume in PDF format", type=["pdf","docx"])
    
    if uploaded_file:
        text = extract_text_from_pdf(uploaded_file)
        entities = extract_entities(text)

        if entities:
            for label, value in entities.items():
                st.subheader(f"{label.replace('_', ' ').title()}:")
                st.write(value)

if __name__ == "__main__":
    main()
