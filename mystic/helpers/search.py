"""Helper functions for search and autocomplete queries using the Fandom MediaWiki API"""

import aiohttp

API_URL = "https://lordofthemysteries.fandom.com/api.php"
REQUEST_TIMEOUT = 5

POPULAR_FALLBACKS = [
    "Klein Moretti",
    "Audrey Hall",
    "Leonard Mitchell",
    "Alger Wilson",
    "Derrick Berg",
    "Fors Wall",
    "Emlyn White",
    "Cattleya",
    "Xio Derecha",
    "Lumian Lee",
    "Tarot Club",
    "Sefirah Castle",
    "Fool Pathway",
    "Visionary Pathway",
    "Error Pathway",
    "Door Pathway",
    "Red Priest Pathway",
    "Creeping Hunger",
    "Magic Wishing Lamp"
]


def sort_suggestions(suggestions: list[str], query: str) -> list[str]:
    """Sorts search suggestions based on match relevance (exact, prefix, word prefix, substring)."""
    cleaned_query = query.strip().lower()
    if not cleaned_query:
        return suggestions

    def score(title: str) -> tuple[int, int, str]:
        title_lower = title.lower()
        # 1. Exact match
        if title_lower == cleaned_query:
            return (0, len(title), title_lower)
        # 2. Starts with query
        if title_lower.startswith(cleaned_query):
            return (1, len(title), title_lower)
        # 3. Word starts with query
        words = title_lower.split()
        if any(w.startswith(cleaned_query) for w in words):
            return (2, len(title), title_lower)
        # 4. Substring match
        if cleaned_query in title_lower:
            return (3, len(title), title_lower)
        # 5. Fallback
        return (4, len(title), title_lower)

    return sorted(suggestions, key=score)


async def fetch_suggestions(query: str) -> list[str]:
    """
    Queries the Fandom MediaWiki opensearch endpoint to get autocomplete suggestions.

    Parameters:
    - query (str): The search input string.

    Returns:
    - list[str]: A list of matching page titles (up to 20 suggestions).
    """
    cleaned_query = query.strip()
    if not cleaned_query:
        return POPULAR_FALLBACKS[:25]

    params = {
        "action": "opensearch",
        "search": cleaned_query,
        "limit": 25,
        "format": "json"
    }
    headers = {
        "User-Agent": "ArrodesBot/1.0 (Discord Bot; contact: owner)"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(API_URL, params=params, headers=headers, timeout=REQUEST_TIMEOUT) as response:
                if response.status == 200:
                    data = await response.json()
                    # OpenSearch format: [query, [titles], [descriptions], [urls]]
                    if len(data) >= 2:
                        titles = [str(title) for title in data[1]]
                        return sort_suggestions(titles, cleaned_query)
    except Exception as e:
        print(f"Warning: Autocomplete API error for query '{query}': {e}")
        
    return []
