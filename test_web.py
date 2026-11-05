from src.web_search import search_web


print("Searching the internet...")

results = search_web("latest developments in artificial intelligence")

for result in results:
    print("\nTitle:", result["title"])
    print("URL:", result["url"])
    print("Description:", result["description"])