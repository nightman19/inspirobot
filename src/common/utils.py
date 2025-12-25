import requests
def fetch_quote(keyword=None, author=None, limit=1):
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

    # Base URL for the Zen Quotes API with random parameter
    base_url = "https://zenquotes.io/api/random?q={q}&a={a}&n={n}"
    
    # Validate limit (muast be between 1 and 100)
    if limit < 1 or limit > 100:
        raise ValueError("Limit musat be between 1 and 100") 

    # Build the query string with optional parameters
    params = {
        "q": keyword if keyword else "",
        "a" : author if author else "",
        "n" : limit
    }

    # send a GET request to the API endpoint
    try:
        response = requests.get(base_url.format(**params))
        response.raise_for_status() # Raise an exception for non-2xx status

        # Parse JSON reponse
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fectching quote: (e)")
        return None
    
    # Check if the quotes were found
    if not data:
        return None
    
    # if multiple  quotes are fetched (due to limit > 1), return the first one
    return data[0]

    # Example usage with keyword filter
    quote = fetch_quote(keyword="gratitude")

    #Example usage with author filter
    quote = fetch_quote(author="Maya Angelou")

    # Example usage with both filters(will return a random quote from matching results)
    quote = fetch_quote(keyword="success", author="Napoleon Hill")

    if quote:
        print(f"{quote['q']} - {quote['a']}")
    else:
        print("No quote found matching your criteria.")