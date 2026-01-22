import streamlit as st
import PyPDF2
import docx
import ollama

def extract_text(uploaded_file):
    if uploaded_file.type == "application/pdf":
        reader = PyPDF2.PdfReader(uploaded_file)
        return "".join([page.extract_text() for page in reader.pages])
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(uploaded_file)
        return "\n".join([para.text for para in doc.paragraphs])
    return ""

st.title("Local AI Resume Analyzer (Private)")
role = st.sidebar.selectbox("Login As:", ["Student", "HR Professional"])
uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])

if uploaded_file and st.button("Analyze locally"):
    resume_text = extract_text(uploaded_file)
    
    # Custom 2026 Prompts
    if role == "Student":
        prompt = f"Analyze this resume. Identify technical/soft skill gaps for 2026 roles. Suggest projects to bridge them.\n\nResume: {resume_text}"
    else:
        prompt = f"Act as an HR expert. List specific advantages and disadvantages (red flags) for this candidate.\n\nResume: {resume_text}"

    # Local Processing with Ollama
    with st.spinner("Processing locally on your hardware..."):
        response = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': prompt}])
    
    st.subheader(f"Local AI Insights for {role}")
    st.write(response['message']['content'])
