import praw
import pandas as pd
import nltk
import spacy
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.tokenize.treebank import TreebankWordDetokenizer
from google.colab import userdata
import asyncio

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt_tab')
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import Counter

nltk.download('punkt')
nltk.download('stopwords')

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import Counter

nltk.download('punkt')
nltk.download('stopwords')

def summarize_text(text, num_sentences=3, custom_stopwords=None):
    if not text.strip():
        return "Input text is empty."
    sentences = sent_tokenize(text)
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    if custom_stopwords:
        stop_words.update(custom_stopwords)

    # Count word frequencies excluding stop words
    words = [lemmatizer.lemmatize(word.lower()) for word in word_tokenize(text) if word.isalnum() and word.lower() not in stop_words]
    word_frequencies = Counter(words)

    # Rank sentences based on word frequencies
    sentence_scores = {}
    for sentence in sentences:
        for word in word_tokenize(sentence.lower()):
            if lemmatizer.lemmatize(word) in word_frequencies:
                sentence_scores[sentence] = sentence_scores.get(sentence, 0) + word_frequencies[lemmatizer.lemmatize(word)]

    # Sort and select top sentences
    summarized_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:num_sentences]
    
    # Ensure the result is not empty
    if summarized_sentences:
        return ' '.join(summarized_sentences)
    return "No meaningful summary could be generated."

# Example usage
text = """
Natural language processing (NLP) is a sub-field of artificial intelligence that focuses on the interaction between computers and humans through natural language. 
The ultimate objective of NLP is to read, decipher, understand, and make sense of human languages in a valuable way. 
Applications of NLP are vast and include chatbots, sentiment analysis, machine translation, and more.
"""
print(summarize_text(text))

