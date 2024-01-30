import spacy

def get_nlp(model:str = "fr_core_news_sm"):
    return spacy.load(model)