import streamlit as st
import pypdf
import docx
import easyocr
import numpy as np
from PIL import Image
from openai import OpenAI
api_key = st.secrets["233b6aa7a7mshe7cab71ea3d65cep120b5bjsn51f791853f4a"]
# Initialize EasyOCR Reader (2026 standard for simple local OCR)
reader = easyocr.Reader(['en'])

def extract_text(uploaded_file):
    file_type = uploaded_file.type
    
    if file_type == "application/pdf":
        pdf_reader = pypdf.PdfReader(uploaded_file)
        return "".join([page.extract_text() for page in pdf_reader.pages])
    
    elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(uploaded_file)
        return "\n".join([para.text for para in doc.paragraphs])
    
    # NEW: Image Analysis (OCR)
    elif file_type in ["image/jpeg", "image/png", "image/jpg"]:
        image = Image.open(uploaded_file)
        image_np = np.array(image) # Convert PIL image to format EasyOCR understands
        results = reader.readtext(image_np, detail=0)
        return " ".join(results)
    
    return ""

st.title("AI Multi-Format Resume Analyzer")
role = st.sidebar.selectbox("Login As:", ["Student", "HR Professional"])
uploaded_file = st.file_uploader("Upload Resume (PDF, DOCX, or Image)", type=["pdf", "docx", "jpg", "jpeg", "png"])

if uploaded_file and st.button("Analyze"):
    with st.spinner("Extracting and analyzing text..."):
        resume_text = extract_text(uploaded_file)
        
        if not resume_text.strip():
            st.error("Could not extract text. Please ensure the file is clear.")
        else:
            # AI Logic (Example using OpenAI API for 2026 cloud compatibility)
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            
            if role == "Student":
                prompt = f"Identify skill gaps and suggest improvements for this resume:\n\n{resume_text}"
            else:
                prompt = f"List professional advantages and disadvantages for this candidate:\n\n{resume_text}"
            
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}]
            )
            st.subheader(f"Results for {role}")
            st.write(response.choices.message.content)

