# test_serp.py — run with: python test_serp.py
import os
from dotenv import load_dotenv
from serpapi import GoogleSearch

load_dotenv()

params = {
    "engine": "google_shopping",
    "q": "samsung phone under 25000",
    "hl": "en",
    "gl": "in",
    "api_key": os.getenv("SERPAPI_KEY"),
    "num": 5
}

search = GoogleSearch(params)
results = search.get_dict()

shopping = results.get("shopping_results", [])
print(f"Results found: {len(shopping)}")

if shopping:
    print("First item:", shopping[0])
else:
    print("Full response:", results)  # this will show the error
