from urllib.parse import urlparse

from ddgs import DDGS


def search_web(query, max_results=5):
    """
    Search the internet using DuckDuckGo.

    Returns a list of search results containing:
    - Title
    - URL
    - Description

    Invalid URLs and duplicate results are removed.
    """

    results = []
    seen_urls = set()

    try:
        with DDGS() as search:

            search_results = search.text(
                query,
                max_results=max_results
            )

            for result in search_results:

                # Get the webpage URL.
                url = result.get("href", "")

                # Skip missing or invalid URLs.
                if not isinstance(url, str):
                    continue

                url = url.strip()

                if not url:
                    continue

                # Validate the URL structure.
                parsed = urlparse(url)

                if parsed.scheme not in ("http", "https"):
                    continue

                if not parsed.hostname:
                    continue

                # Skip duplicate websites.
                if url in seen_urls:
                    continue

                seen_urls.add(url)

                # Extract search-result information.
                title = result.get("title", "")
                description = result.get("body", "")

                # Store the result.
                results.append({
                    "title": title,
                    "url": url,
                    "description": description
                })

                # Stop when we have enough results.
                if len(results) >= max_results:
                    break

    except Exception as error:
        print(f"Web search error: {error}")

    return results