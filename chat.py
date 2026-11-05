from src.research import research_question


print("=" * 50)
print("UNB0UND-AI")
print("Local AI with Automatic Internet Research")
print("=" * 50)

while True:
    question = input("\nYou: ").strip()

    if question.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break

    if not question:
        continue

    try:
        result = research_question(question)

        print("\nUnb0und-AI:")
        print(result["answer"])

        if result["sources"]:
            print("\nSources:")

            for source in result["sources"]:
                print(f"- {source['title']}: {source['url']}")

    except Exception as error:
        print(f"\nError: {error}")