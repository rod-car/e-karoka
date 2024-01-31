from spellchecker import SpellChecker

def correct_word(word: str, lang:str = "fr") -> str:
    spell = SpellChecker(language=lang)
    return spell.correction(word=word)

def correct_phrase(phrase: str, lang:str = "fr") -> str:
    spelled_phrase = [correct_word(word, lang=lang) for word in phrase.split()]
    return ' '.join(spelled_phrase)