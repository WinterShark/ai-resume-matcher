import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def preprocess_text(text: str) -> str:
    """
    Preprocess the input text by removing stopwords, punctuation, and lemmatizing it.

    Args:
        text (str): The text to be processed.

    Returns:
        str: The cleaned and lemmatized text.
    """
    # Process the text with spaCy
    doc = nlp(text)
    processed_text = " ".join([token.lemma_ for token in doc if not token.is_stop and not token.is_punct])
    return processed_text

def extract_keywords(text: str) -> list:
    """
    Extract keywords (nouns and adjectives) from the provided text using spaCy.

    Args:
        text (str): The text to extract keywords from.

    Returns:
        list: A list of extracted keywords.
    """
    # Process the text with spaCy
    doc = nlp(text)
    keywords = [token.text for token in doc if token.pos_ in ['NOUN', 'ADJ']]
    return keywords

def compute_match_score(resume_text: str, jd_text: str) -> float:
    """
    Compute a cosine similarity score between the resume and job description.

    Args:
        resume_text (str): The resume text.
        jd_text (str): The job description text.

    Returns:
        float: The cosine similarity score between 0 and 1.
    """
    # Vectorize the resume and job description text using TF-IDF
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume_text, jd_text])

    # Compute cosine similarity
    similarity_matrix = cosine_similarity(vectors)
    return similarity_matrix[0, 1] * 100  # Scale to 100 for better readability
