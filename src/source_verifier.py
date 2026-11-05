from datetime import datetime


def verify_source(source, webpage):
    """
    Check whether a source was successfully retrieved.
    """

    verified = webpage.get("success", False)

    result = {
        "title": source.get("title", ""),
        "url": source.get("url", ""),
        "retrieved": verified,
        "publication_date": None,
        "checked_at": datetime.now().isoformat(timespec="seconds"),
        "status": "RETRIEVED" if verified else "NOT RETRIEVED",
        "error": webpage.get("error")
    }

    return result