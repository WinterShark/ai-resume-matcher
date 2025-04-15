import streamlit as st
import os
import pandas as pd
from services.nlp import preprocess_text, extract_keywords, compute_match_score
from utils.file_utils import save_uploaded_file

# Title of the app
st.title("Resume Job Matcher")

# Sidebar for navigation
st.sidebar.title("Options")
app_mode = st.sidebar.selectbox("Select a feature", ["Upload Resume & Job Description", "Results"])

if app_mode == "Upload Resume & Job Description":
    st.subheader("Upload Resume & Job Description")

    # File upload widgets for resume and job description
    resume_file = st.file_uploader("Upload Resume (PDF/DOCX/TXT)", type=["pdf", "docx", "txt"])
    jd_file = st.file_uploader("Upload Job Description (PDF/DOCX/TXT)", type=["pdf", "docx", "txt"])

    if resume_file and jd_file:
        resume_text = save_uploaded_file(resume_file)
        jd_text = save_uploaded_file(jd_file)

        st.write("**Resume Preview:**")
        st.text(resume_text[:500])  # Show first 500 chars for preview

        st.write("**Job Description Preview:**")
        st.text(jd_text[:500])

        # Process and analyze resume vs job description
        if st.button("Analyze Match"):
            processed_resume = preprocess_text(resume_text)
            processed_jd = preprocess_text(jd_text)

            # Calculate match score
            match_score = compute_match_score(processed_resume, processed_jd)

            st.subheader("Match Score")
            st.write(f"Match Score: {match_score:.2f}/100")

            # Show keywords from both resume and job description
            resume_keywords = extract_keywords(processed_resume)
            jd_keywords = extract_keywords(processed_jd)

            st.write("**Resume Keywords:**", resume_keywords)
            st.write("**Job Description Keywords:**", jd_keywords)

            st.subheader("Feedback & Suggestions")
            missing_keywords = set(jd_keywords) - set(resume_keywords)
            if missing_keywords:
                st.write("**Missing Keywords:**", missing_keywords)
            else:
                st.write("No major missing keywords detected!")

            st.write("**Suggestions for Improvement:**")
            st.write("1. Consider adding action verbs to your resume.")
            st.write("2. Ensure all required skills are listed.")
            st.write("3. Tailor your resume based on the job description.")

if app_mode == "Results":
    st.subheader("Download & Share Results")
    st.write("You can save your analysis results as a PDF or share via email.")

    # Implement download functionality or email sharing (additional functionality)
    if st.button("Download Feedback Report"):
        # Implement the PDF download logic here
        st.write("Feedback report downloaded!")
