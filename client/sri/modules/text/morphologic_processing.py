import nltk
import spacy
from nltk.corpus import wordnet
from PyMultiDictionary import MultiDictionary
from nltk.corpus.reader.wordnet import WordNetError

nlp = spacy.load("fr_core_news_lg")

# nltk.download('wordnet')
# nltk.download('omw-1.4')

def synonyms_en_wordnet(word):
    synonyms = []

    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())

    return list(set(synonyms))

def synonyms_fr(word):
    dictionary = MultiDictionary()
    return dictionary.synonym('fr', word)

def synonyms_sentence_fr(sentence):
    synonyms = []
    words = nltk.word_tokenize(sentence, language="french")
    
    for word in words:
        synsets = wordnet.synsets(word, lang='fra')

        if synsets:
            word_synonyms = [lemma.name() for synset in synsets for lemma in synset.lemmas(lang='fra')]
            synonyms.extend(word_synonyms)

    return list(set(synonyms))

def synonyms_sentence_fr_(sentence):
    synonyms = []
    words = word_tokenize(sentence, language="french")
    
    for word in words:
        synsets = wordnet.synsets(word, lang='fra')

        if synsets:
            word_synonyms = []
            for synset in synsets:
                for lemma in synset.lemmas(lang='fra'):
                    similarity = synset.wup_similarity(wordnet.synset(synset.name()), wordnet.synset(lemma.name()))
                    word_synonyms.append((lemma.name(), similarity))
            
            # Sort synonyms by similarity and get the top two
            word_synonyms.sort(key=lambda x: -x[1])  # Sort in descending order of similarity
            top_synonyms = word_synonyms[:2]
            synonyms.extend([synonym[0] for synonym in top_synonyms])

    return list(set(synonyms))

def get_synonyms(word, lang='fra'):
    most_similar = []
    synsets = wordnet.synsets(word, lang=lang)

    if not synsets:
        return most_similar  # Return an empty list if no synsets found

    # Create a reference synset from the first synset found
    reference_synset = synsets[0]

    # Calculate and store similarity scores for each synonym
    similarity_scores = {}
    for synset in synsets:
        for lemma in synset.lemmas(lang=lang):
            try:
                similarity = reference_synset.wup_similarity(wordnet.synset(lemma.name()), simulate_root=False)
                if similarity is not None:  # Check for None (no similarity score) before adding
                    similarity_scores[lemma.name()] = similarity
            except WordNetError:
                pass  # Handle cases where the lemma does not exist in WordNet

    # Sort synonyms by similarity and get the top two
    sorted_synonyms = sorted(similarity_scores.items(), key=lambda x: -x[1])
    top_similar_words = [synonym for synonym, _ in sorted_synonyms[:2]]
    most_similar = top_similar_words

    return most_similar

# import gensim.downloader
# 
# model = gensim.downloader.load("fasttext-wiki-news-subwords-300")
# 
# def get_most_similar_synonyms(word, topn=2):
#     try:
#         similar_words = model.most_similar(word, topn=topn)
#         return [word for word, similarity in similar_words]
#     except KeyError:
#         return []
#     
# get_most_similar_synonyms("")

def get_most_similar_synonyms(word, topn=2):
    synonyms = []
    print([word.text for word in nlp.vocab if word.is_alpha and word.is_lower])
    exit(0)
    if word in nlp.vocab:
        token = nlp(word)
        for other in nlp.vocab:
            # Calculate the similarity between the word and other words
            if other.is_lower and other.is_alpha:
                similarity = token.similarity(other)
                synonyms.append((other.text, similarity))
    
    # Sort by similarity and get the top two
    synonyms.sort(key=lambda x: -x[1])
    top_synonyms = [synonym for synonym, _ in synonyms[:topn]]
    return top_synonyms