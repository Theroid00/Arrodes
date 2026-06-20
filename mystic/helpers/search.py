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
                        return [str(title) for title in data[1]]
    except Exception as e:
        print(f"Warning: Autocomplete API error for query '{query}': {e}")
        
    return []
