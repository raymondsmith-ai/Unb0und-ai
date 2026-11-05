from src.web_reader import read_webpage
from src.source_verifier import verify_source


source = {
    "title": "Python Official Website",
    "url": "https://www.python.org/about/"
}

print("Checking source...")

webpage = read_webpage(source["url"])

result = verify_source(source, webpage)

print("\nVerification Results:")
print("Title:", result["title"])
print("URL:", result["url"])
print("Retrieved:", result["retrieved"])
print("Status:", result["status"])
print("Checked at:", result["checked_at"])

if result["error"]:
    print("Error:", result["error"])