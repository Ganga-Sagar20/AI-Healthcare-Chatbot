import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import os

# Download required NLTK data if not present
def download_nltk_data():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', quiet=True)
        nltk.download('punkt_tab', quiet=True) # Sometimes required in newer NLTK versions
    
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords', quiet=True)

# Run once upon import
download_nltk_data()

def preprocess_text(text):
    """
    Cleans and preprocesses the user's text input.
    """
    if not isinstance(text, str):
        return []
        
    # 1. Lowercase conversion
    text = text.lower()
    
    # 2. Punctuation removal
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # 3. Tokenization
    tokens = word_tokenize(text)
    
    # 4. Stopword removal
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    
    return filtered_tokens
