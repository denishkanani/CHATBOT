from search import search_google

results = search_google("Artificial Intelligence")

for result in results:
    print("Title:", result["title"])
    print("Link:", result["link"])
    print("Snippet:", result["snippet"])
    print("-" * 50)