import streamlit as st
import spacy
import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from fpdf import FPDF
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from python_docx import Document

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

# Helper Functions

# Function to process text (remove stopwords, lemmatize, etc.)
def preprocess_text(text):
    doc = nlp(text)
    cleaned_text = " ".join([token.lemma_ for token in doc if not token.is_stop and not token.is_punct])
    return cleaned_text

# Function to extract entities and skills from text (can be extended)
def extract_skills(text):
    doc = nlp(text)
    skills = [ent.text for ent in doc.ents if ent.label_ == "SKILL"]
    return skills

# Function to compute cosine similarity between Resume and JD
def compute_similarity(resume_text, jd_text):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume_text, jd_text])
    cosine_sim = (vectors * vectors.T).A[0, 1]
    return cosine_sim * 100  # Convert to percentage

# PDF Report Generation
def generate_pdf_report(resume_text, jd_text, missing_keywords, suggestions, match_score):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Resume vs Job Description Match Report", ln=True, align="C")
    pdf.cell(200, 10, txt=f"Match Score: {match_score:.2f}%", ln=True, align="L")
    pdf.ln(10)

    pdf.cell(200, 10, txt="Resume Preview:", ln=True, align="L")
    pdf.multi_cell(0, 10, resume_text)
    pdf.ln(10)

    pdf.cell(200, 10, txt="Job Description Preview:", ln=True, align="L")
    pdf.multi_cell(0, 10, jd_text)
    pdf.ln(10)

    if missing_keywords:
        pdf.cell(200, 10, txt="Missing Keywords:", ln=True, align="L")
        pdf.multi_cell(0, 10, ", ".join(missing_keywords))
        pdf.ln(10)

    pdf.cell(200, 10, txt="Suggestions for Improvement:", ln=True, align="L")
    for suggestion in suggestions:
        pdf.multi_cell(0, 10, suggestion)
        pdf.ln(5)

    file_path = "feedback_report.pdf"
    pdf.output(file_path)
    return file_path

# Markdown Report Generation
def generate_markdown_report(resume_text, jd_text, missing_keywords, suggestions, match_score):
    report = f"# Resume vs Job Description Match Report\n\n"
    report += f"## Match Score: {match_score:.2f}%\n\n"

    report += f"## Resume Preview:\n\n{resume_text}\n\n"
    report += f"## Job Description Preview:\n\n{jd_text}\n\n"

    if missing_keywords:
        report += f"## Missing Keywords:\n\n" + ", ".join(missing_keywords) + "\n\n"

    report += f"## Suggestions for Improvement:\n\n"
    for suggestion in suggestions:
        report += f"- {suggestion}\n"

    file_path = "feedback_report.md"
    with open(file_path, "w") as file:
        file.write(report)
    
    return file_path

# Function to send email
def send_email(subject, body, to_email):
    from_email = "your_email@example.com"
    from_password = "your_email_password"

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        return "Email sent successfully!"
    except Exception as e:
        return f"Error: {str(e)}"

# Function to store session logs locally
def store_session_log(resume_text, jd_text, missing_keywords, suggestions, match_score):
    log = {
        "resume_text": resume_text,
        "jd_text": jd_text,
        "missing_keywords": list(missing_keywords),
        "suggestions": suggestions,
        "match_score": match_score,
    }

    log_file = "session_logs.json"
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            logs = json.load(f)
    else:
        logs = []

    logs.append(log)

    with open(log_file, "w") as f:
        json.dump(logs, f, indent=4)

# Streamlit UI
def main():
    st.title("Resume vs Job Description Matching")

    # Upload Resume and Job Description
    resume_file = st.file_uploader("Upload your Resume (.pdf, .docx, .txt)", type=["pdf", "docx", "txt"])
    jd_file = st.file_uploader("Upload Job Description (.pdf, .docx, .txt)", type=["pdf", "docx", "txt"])

    if resume_file and jd_file:
        # Extract text from files
        resume_text = ""
        jd_text = ""

        # Handle different file types
        if resume_file.type == "application/pdf":
            resume_text = extract_pdf_text(resume_file)
        elif resume_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            resume_text = extract_docx_text(resume_file)
        else:
            resume_text = resume_file.read().decode("utf-8")

        if jd_file.type == "application/pdf":
            jd_text = extract_pdf_text(jd_file)
        elif jd_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            jd_text = extract_docx_text(jd_file)
        else:
            jd_text = jd_file.read().decode("utf-8")

        # Preprocess Text
        cleaned_resume = preprocess_text(resume_text)
        cleaned_jd = preprocess_text(jd_text)

        # Extract Skills
        resume_skills = extract_skills(resume_text)
        jd_skills = extract_skills(jd_text)

        # Compute Match Score
        match_score = compute_similarity(cleaned_resume, cleaned_jd)

        # Identify Missing Keywords
        missing_keywords = set(jd_skills) - set(resume_skills)

        # Provide Suggestions (Basic Suggestions)
        suggestions = []
        if missing_keywords:
            suggestions.append(f"Consider adding skills like: {', '.join(missing_keywords)}")

        suggestions.append("Make sure to use action verbs and tailor your experience.")

        # Display Match Score
        st.subheader(f"Match Score: {match_score:.2f}%")

        # Display Suggestions
        st.subheader("Suggestions for Improvement:")
        for suggestion in suggestions:
            st.write(f"- {suggestion}")

        # Save Session Logs
        store_session_log(resume_text, jd_text, missing_keywords, suggestions, match_score)

        # Download Feedback Report
        st.subheader("Download Feedback Report")
        if st.button("Download as PDF"):
            pdf_file = generate_pdf_report(resume_text, jd_text, missing_keywords, suggestions, match_score)
            st.download_button("Download PDF", pdf_file)

        if st.button("Download as Markdown"):
            md_file = generate_markdown_report(resume_text, jd_text, missing_keywords, suggestions, match_score)
            st.download_button("Download Markdown", md_file)

        # Send Email Option
        email = st.text_input("Enter Email to Send Results")
        if st.button("Email Results"):
            if email:
                subject = "Your Resume vs Job Description Match Results"
                body = f"Match Score: {match_score:.2f}%\n\nSuggestions:\n" + "\n".join(suggestions)
                result = send_email(subject, body, email)
                st.write(result)
            else:
                st.error("Please enter a valid email address.")

# Function to extract text from PDF files
def extract_pdf_text(file):
    from pdfminer.high_level import extract_text
    text = extract_text(file)
    return text

# Function to extract text from .docx files
def extract_docx_text(file):
    doc = Document(file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

if __name__ == "__main__":
    main()
