import sqlite3
import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

def vectorize(tokens: list) -> tuple:
    print("''''''''''''''''''''''''''''''''")
    print("Vectorizing")
    print("''''''''''''''''''''''''''''''''")
    
    doc_content = " ".join(tokens)
    docs = [doc_content]

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(docs)
    # feature_names = vectorizer.get_feature_names_out()
    
    return tfidf_matrix