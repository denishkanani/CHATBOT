import requests
from config import config


def _fallback_search_results(query, num_results=5):
    """
    Provide a simple, deterministic fallback result set when the Google Custom
    Search API cannot be used.
    """
    query_lower = query.lower()

    fallback_items = []

    if "artificial intelligence" in query_lower or "ai" in query_lower:
        fallback_items = [
            {
                "title": "Artificial Intelligence",
                "link": "https://example.com/artificial-intelligence",
                "snippet": "Artificial Intelligence is the simulation of human intelligence by machines."
            },
            {
                "title": "Machine Learning",
                "link": "https://example.com/machine-learning",
                "snippet": "Machine Learning is a branch of AI that enables computers to learn from data."
            }
        ]
    elif "machine learning" in query_lower:
        fallback_items = [
            {
                "title": "Machine Learning",
                "link": "https://example.com/machine-learning",
                "snippet": "Machine Learning is a field of AI focused on building systems that learn from data."
            }
        ]
    else:
        fallback_items = [
            {
                "title": query,
                "link": "https://example.com/search",
                "snippet": "No live search results were available, so a local fallback result is being shown."
            }
        ]

    return fallback_items[:num_results]


def search_google(query, num_results=5):
    """
    Search Google Custom Search API or fall back to local demo results.

    Returns:
        List of dictionaries
    """

    if not config.GOOGLE_API_KEY or not config.GOOGLE_CSE_ID:
        return _fallback_search_results(query, num_results=num_results)

    url = "https://www.googleapis.com/customsearch/v1"

    params = {
        "key": config.GOOGLE_API_KEY,
        "cx": config.GOOGLE_CSE_ID,
        "q": query,
        "num": num_results
    }

    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()

        data = response.json()

        results = []

        if "items" in data:
            for item in data["items"]:
                results.append({
                    "title": item.get("title"),
                    "link": item.get("link"),
                    "snippet": item.get("snippet")
                })

        return results or _fallback_search_results(query, num_results=num_results)

    except requests.exceptions.RequestException as e:
        print(f"Search Error: {e}")
        return _fallback_search_results(query, num_results=num_results)
