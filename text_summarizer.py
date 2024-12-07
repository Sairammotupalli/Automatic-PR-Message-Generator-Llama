def summarize_text(text, num_sentences=3):
    if not text.strip():
        return "Input text is empty."
    sentences = sent_tokenize(text)
    words = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))

    # Count word frequencies excluding stop words
    word_frequencies = Counter(word for word in words if word not in stop_words and word.isalnum())

    # Rank sentences based on word frequencies
    sentence_scores = {}
    for sentence in sentences:
        for word in word_tokenize(sentence.lower()):
            if word in word_frequencies:
                sentence_scores[sentence] = sentence_scores.get(sentence, 0) + word_frequencies[word]

    # Sort and select top sentences
    summarized_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:num_sentences]
    
    # Ensure the result is not empty
    if summarized_sentences:
        return ' '.join(summarized_sentences)
    return "No meaningful summary could be generated."
