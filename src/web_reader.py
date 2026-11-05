import requests
from bs4 import BeautifulSoup


def read_webpage(url, max_characters=5000):
    """
    Download a webpage and extract its readable text.
    """

    try:
        response = requests.get(
            url,
            timeout=15,
            headers={
                "User-Agent": "Unb0und-AI/0.1"
            }
        )

        response.raise_for_status()

        content_type = response.headers.get(
            "Content-Type", ""
        ).lower()

        if "text/html" not in content_type:
            return {
                "success": False,
                "url": url,
                "content": "",
                "error": "Unsupported content type"
            }

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # Remove elements that usually contain
        # navigation, scripts, and unrelated content.
        for element in soup([
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "noscript"
        ]):
            element.decompose()

        text = soup.get_text(
            separator=" ",
            strip=True
        )

        # Normalize whitespace.
        text = " ".join(text.split())

        return {
            "success": True,
            "url": url,
            "content": text[:max_characters],
            "error": None
        }

    except requests.RequestException as error:
        return {
            "success": False,
            "url": url,
            "content": "",
            "error": str(error)
        }