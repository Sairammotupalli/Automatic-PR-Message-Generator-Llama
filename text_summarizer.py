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

def summarize_text(text, num_sentences=3, language='english', custom_stopwords=None):
    try:
        if not text.strip():
            return "Input text is empty."
        nltk.download('stopwords')
        nltk.download('punkt')
        stop_words = set(stopwords.words(language))
        if custom_stopwords:
            stop_words.update(custom_stopwords)

        sentences = sent_tokenize(text)
        words = word_tokenize(text.lower())
        words = [word for word in words if word.isalnum() and word not in stop_words]

        # POS tagging to weigh important words
        tagged_words = pos_tag(words)
        important_words = [word for word, tag in tagged_words if tag.startswith(('NN', 'VB'))]

        word_frequencies = Counter(important_words)

        # Rank sentences based on word frequencies
        sentence_scores = {}
        for sentence in sentences:
            for word in word_tokenize(sentence.lower()):
                if word in word_frequencies:
                    sentence_scores[sentence] = sentence_scores.get(sentence, 0) + word_frequencies[word]

        summarized_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:num_sentences]
        
        # Ensure the result is not empty
        if summarized_sentences:
            return ' '.join(summarized_sentences)
        return "No meaningful summary could be generated."
    except Exception as e:
        return f"Error: {e}"

# Example usage
text = """
Natural language processing (NLP) is a sub-field of artificial intelligence that focuses on the interaction between computers and humans through natural language. 
The ultimate objective of NLP is to read, decipher, understand, and make sense of human languages in a valuable way. 
Applications of NLP are vast and include chatbots, sentiment analysis, machine translation, and more.
"""
print(summarize_text(text))

