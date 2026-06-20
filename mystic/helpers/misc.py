"""Helper functions for miscellaneous tasks"""

import re

EXCLUDED_WORDS = {
    "of", "in", "with", "from", "through", "during", "including", "until", 
    "against", "among", "throughout", "despite", "towards", "upon", 
    "concerning", "and", "but", "or", "yet", "so", "the", "a", "an", "to", "for", "at", "by", "on"
}


def format_name(text):
    """
    This function takes a string as input, splits it into words, and capitalizes each word 
    that is not a preposition, conjunction, or article.
    It then joins the words together with underscores and returns the result.
    It splits by '/' first to correctly handle sub-page names.

    Parameters:
    text (str): The input string to be formatted.

    Returns:
    str: The formatted string with capitalized words (excluding prepositions/conjunctions/articles) joined by underscores.
    """
    parts = text.split('/')
    formatted_parts = []
    for part in parts:
        words = part.split()
        capitalized_words = []
        for word in words:
            if word.lower() in EXCLUDED_WORDS:
                capitalized_words.append(word.lower())
            else:
                capitalized_words.append(word.capitalize())
        formatted_parts.append("_".join(capitalized_words))

    return "/".join(formatted_parts)



def clean_text(text: str) -> str:
    """
    Strips citation brackets (e.g. [1], [Note 1]) and handles whitespace cleanly.

    Parameters:
    text (str): The input string to be cleaned.

    Returns:
    str: The cleaned string.
    """
    if not text:
        return ""
    # Remove citation brackets like [1], [Note 1]
    cleaned = re.sub(r'\[[^\]]*\]', '', text)
    # Normalize whitespaces
    return " ".join(cleaned.split()).strip()


