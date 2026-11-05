from src.web_reader import read_webpage


url = "https://www.python.org/about/"

print("Reading webpage...")
print("URL:", url)

result = read_webpage(url)

if result["success"]:
    print("\nSUCCESS!")
    print("\nExtracted content:\n")
    print(result["content"][:1500])
else:
    print("\nFAILED!")
    print(result["error"])