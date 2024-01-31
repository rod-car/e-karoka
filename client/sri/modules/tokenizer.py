import re
import unicodedata
from collections import Counter
from spacy.tokenizer import Tokenizer

from ..config.app import get_nlp

nlp = get_nlp()

def custom_tokenizer(nlp):
    special_cases = {":)": [{"ORTH": ":)"}]}
    prefix_re = re.compile(r'''^[\[\("']''')
    suffix_re = re.compile(r'''[\]\)"']$''')
    infix_re = re.compile(r'''[-~]''')
    simple_url_re = re.compile(r'''^https?://''')
    
    return Tokenizer(
        nlp.vocab,
        rules=special_cases,
        prefix_search=prefix_re.search,
        suffix_search=suffix_re.search,
        infix_finditer=infix_re.finditer,
        url_match=simple_url_re.match
    )

def remove_accents_french(text):
    normalized_text = unicodedata.normalize('NFD', text)
    text_without_accents = ''.join([char for char in normalized_text if not unicodedata.combining(char)])
    return text_without_accents

def remove_most_occureng_text(tokens, percentage = 0.8):
    token_counts = Counter(tokens)
    total_tokens = len(tokens)
    threshold = total_tokens * percentage
    tokens_to_keep = []

    for token, count in token_counts.items():
        if count <= threshold:
            tokens_to_keep.append(token)
            
    filtered_tokens = [token for token in tokens if token in tokens_to_keep]
    return filtered_tokens

def tokenize1(text: str):
    text = re.sub(r'\n', ' ', text)
    text = remove_accents_french(text)
    document = nlp(text)
    
    tokens = [
        token.lemma_.lower() for token in document
        if not token.is_stop
        and not token.is_punct
        and not token.is_bracket
        and not token.is_quote
        and not token.is_digit
        and not token.is_space
    ]
    
    return tokens

def tokenize(text: str):
    text = text.replace('\n', ' ')
    text = remove_accents_french(text)

    # Tokenize the text using spaCy
    doc = nlp(text)

    # Precompile the stop words, punctuation, etc. conditions for faster filtering
    conditions = [
        lambda token: not token.is_stop,
        lambda token: not token.is_punct,
        lambda token: not token.is_bracket,
        lambda token: not token.is_quote,
        lambda token: not token.is_digit,
        lambda token: not token.is_space,
    ]
    
    print("''''''''''''''''''''''''''''''''")
    print("Tokenizing")
    print("''''''''''''''''''''''''''''''''")
    
    tokens = [token.lemma_.lower() for token in doc if all(cond(token) for cond in conditions)]

    return tokens