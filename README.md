# Resume Job Matcher

A Streamlit app that helps users match their resumes with job descriptions by comparing key skills, experience, and role-related keywords. The app extracts content from resumes and job descriptions, processes the text, and provides a **match score** based on cosine similarity.

## Features

- **Upload Resume & Job Description**: Upload `.pdf`, `.docx`, or `.txt` files.
- **Text Preprocessing & Tokenization**: Clean text, tokenize, lemmatize, and extract entities.
- **Resume vs Job Description Comparison**: Compute a match score based on skills, experience, and keywords.
- **Feedback & Suggestions**: Receive tips on improving your resume and filling gaps based on the job description.
- **Save & Share Results**: Download feedback as PDF or share results via email.

## Installation

### Prerequisites

Make sure you have Python 3.9 or later installed.

### Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/resume-job-matcher.git
    cd resume-job-matcher
    ```

2. Set up a Python virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Download the spaCy model:

    ```bash
    python -m spacy download en_core_web_sm
    ```

### Run the App

Run the Streamlit app:

```bash
streamlit run app.py
