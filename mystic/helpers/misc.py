"""Helper functions for miscellaneous tasks"""

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

    Parameters:
    text (str): The input string to be formatted.

    Returns:
    str: The formatted string with capitalized words (excluding prepositions/conjunctions/articles) joined by underscores.
    """
    words = text.split()
    capitalized_words = []
    for word in words:
        if word.lower() in EXCLUDED_WORDS:
            capitalized_words.append(word.lower())
        else:
            capitalized_words.append(word.capitalize())

    return "_".join(capitalized_words)

