from ddgs import DDGS


def search_web(query, max_results=5):
    """
    Search the internet and return relevant results.
    """

    results = []

    try:
        with DDGS() as search:
            search_results = search.text(
                query,
                max_results=max_results
            )

            for result in search_results:
                results.append({
                    "title": result.get("title", ""),
                    "url": result.get("href", ""),
                    "description": result.get("body", "")
                })

    except Exception as error:
        print(f"Web search error: {error}")

    return results