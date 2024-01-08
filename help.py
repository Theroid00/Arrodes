import nltk
from nltk import word_tokenize, pos_tag
from nltk.corpus import stopwords

def capitalize_except_unwanted_words(text):
    tagged_words = pos_tag(text.split())

    # List of POS tags for words to be excluded
    excluded_pos_tags = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'IN', 'CC']
    
    capitalized_words = []
    for word, tag in tagged_words:
        if tag not in excluded_pos_tags:
            capitalized_words.append(word.capitalize())
        else:
            capitalized_words.append(word.lower())
    return ' '.join(capitalized_words)