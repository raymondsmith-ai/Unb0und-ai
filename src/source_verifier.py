"""
Unb0und-AI Source Verifier

Checks whether a webpage was retrieved successfully
and extracts publication dates when available.
"""

from datetime import datetime
from email.utils import parsedate_to_datetime

import requests
from bs4 import BeautifulSoup


def normalize_date(date_string):
    """
    Convert a publication date into a consistent format.

    Returns YYYY-MM-DD when possible.
    """

    if not date_string:
        return None

    date_string = str(date_string).strip()

    try:
        # Handle ISO 8601 dates.
        normalized = date_string.replace("Z", "+00:00")

        return datetime.fromisoformat(
            normalized
        ).date().isoformat()

    except ValueError:
        pass

    try:
        # Handle HTTP-style dates.
        return parsedate_to_datetime(
            date_string
        ).date().isoformat()

    except (TypeError, ValueError, IndexError):
        return None


def extract_publication_date(url):
    """
    Attempt to find a webpage's publication date.

    Returns None when no recognizable date is found.
    """

    if not url:
        return None

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
            return None

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # Common publication-date metadata.
        metadata = [
            ("property", "article:published_time"),
            ("name", "datePublished"),
            ("name", "pubdate"),
            ("name", "publish_date"),
            ("name", "date"),
            ("itemprop", "datePublished")
        ]

        for attribute, value in metadata:

            tag = soup.find(
                "meta",
                attrs={attribute: value}
            )

            if tag:
                publication_date = normalize_date(
                    tag.get("content")
                )

                if publication_date:
                    return publication_date

        # Check HTML time elements.
        time_tag = soup.find(
            "time",
            attrs={"datetime": True}
        )

        if time_tag:
            return normalize_date(
                time_tag.get("datetime")
            )

        return None

    except requests.RequestException:
        return None


def verify_source(source, webpage):
    """
    Verify webpage retrieval and collect source metadata.

    Important:
    Successful retrieval does not establish that
    the webpage's claims are factually correct.
    """

    retrieved = webpage.get(
        "success",
        False
    )

    url = source.get("url", "")

    publication_date = None

    if retrieved:
        publication_date = extract_publication_date(
            url
        )

    result = {
        "title": source.get("title", ""),
        "url": url,
        "retrieved": retrieved,
        "publication_date": publication_date,
        "checked_at": datetime.now().isoformat(
            timespec="seconds"
        ),
        "status": (
            "RETRIEVED"
            if retrieved
            else "NOT RETRIEVED"
        ),
        "error": webpage.get("error")
    }

    return result