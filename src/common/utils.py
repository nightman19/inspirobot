import random
from django.core.cache import cache
import requests

CACHE_TIMEOUT = 60 * 10 # Cache quotes for 10 minutes to reduce API calls and improve performance


def fetch_quote(keyword=None, author=None, limit=10, use_cache=True):
    """Fetches a random inspirational quote from the Zen Quotes API,
        optionally filtered by keyword and author.

    Args:
        keyword (str, optional): Keyword to filter quotes by. Defaults to None.
        author (str, optional): Author to filter quotes by. Defaults to None.
        limit (int, optional): Number of quotes to fetch (maximum 100). Defaults to 1.

    Returns:
        dict: A dictionary containing quote information (q: quote text, a: author),
            or None if no quotes are found matching the criteria.
    """


    if limit < 1 or limit > 100:
        raise ValueError("Limit must be between 1 and 100")

    cache_key = f"quote:{keyword or ''}:{author or ''}:{limit}"
    
    if use_cache:
        cached_data = cache.get(cache_key)
        if cached_data:
            return random.choice(cached_data)

    try:
        # Choose endpoint based on filters
        if keyword or author:
            url = "https://zenquotes.io/api/quotes"
            params = {
                "q": keyword or "",
                "a": author or "",
            }
        else:
            url = "https://zenquotes.io/api/random"
            params = {}

        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

    except requests.exceptions.RequestException:
        return None

    if not data:
        return None

    # Normalize → always store list
    if isinstance(data, dict):
        data = [data]

    if use_cache:
        cache.set(cache_key, data, CACHE_TIMEOUT)

    return random.choice(data)