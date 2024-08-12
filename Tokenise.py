import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def extract_keywords(transcribed_text):

    # nltk.download("punkt")
    # nltk.download("stopwords")

    stop_words = set(stopwords.words('english'))
    words = word_tokenize(transcribed_text)
    filtered_words = [word for word in words if word.isalnum() and word.lower() not in stop_words]
    return filtered_words