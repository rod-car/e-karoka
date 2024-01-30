from spellchecker import SpellChecker
# import language_tool_python

def correct_word(word: str, lang:str = "fr") -> str:
    spell = SpellChecker(language=lang)
    return spell.correction(word=word)

def correct_phrase(phrase: str, lang:str = "fr") -> str:
    spelled_phrase = [correct_word(word, lang=lang) for word in phrase.split()]
    return ' '.join(spelled_phrase)

# def correct_grammar(phrase:str) -> str:
#    tool = language_tool_python.LanguageTool('fr')
#    return tool.correct(phrase)