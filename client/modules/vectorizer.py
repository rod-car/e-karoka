from sklearn.feature_extraction.text import TfidfVectorizer

def vectorize(tokens: list) -> tuple:
    # doc_content = " ".join(tokens)
    
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(tokens)
    
    # tfidf_matrix = vectorizer.fit_transform([doc_content])
    
    return tfidf_matrix