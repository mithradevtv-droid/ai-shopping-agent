from typing import List
from serpapi import GoogleSearch
from models.product import Product
from models.preference import UserPreference
import os
import urllib.parse

SKIP_AS_SEARCH_TERMS = [
    "battery", "battery life", "camera", "performance", "display",
    "storage", "ram", "processor", "screen", "design", "build",
    "sound", "audio", "speaker", "charging", "fast charging"
]

def get_best_url(item: dict) -> str:
    title = item.get("title", "")
    source = (item.get("source") or "").lower()
    encoded = urllib.parse.quote_plus(title)

    if "amazon" in source:
        return f"https://www.amazon.in/s?k={encoded}"
    elif "flipkart" in source:
        return f"https://www.flipkart.com/search?q={encoded}"
    elif "croma" in source:
        return f"https://www.croma.com/searchB?q={encoded}"
    elif "reliance" in source or "jiomart" in source:
        return f"https://www.reliancedigital.in/search?q={encoded}"
    elif "tata" in source or "cliq" in source:
        return f"https://www.tatacliq.com/search/?searchCategory=all&text={encoded}"
    elif "vijay" in source:
        return f"https://www.vijaysales.com/search/{encoded}"
    else:
        return f"https://www.google.com/search?tbm=shop&q={encoded}"

def build_query(prefs: UserPreference) -> str:
    parts = [f"best {prefs.category}"]
    for p in prefs.priorities:
        if p.lower() not in SKIP_AS_SEARCH_TERMS:
            parts.append(p)
    parts.append(f"under {prefs.budget}")
    return " ".join(parts)

def aggregator_search_agent(prefs: UserPreference) -> List[Product]:
    query = build_query(prefs)
    print(f"SEARCH QUERY: {query}")
    params = {
        "engine": "google_shopping",
        "q": query,
        "hl": "en",
        "gl": "in",
        "api_key": os.getenv("SERPAPI_KEY"),
        "num": 20
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    shopping_results = results.get("shopping_results", [])
    print(f"TOTAL SHOPPING RESULTS: {len(shopping_results)}")

    products = []
    for item in shopping_results:
        price = item.get("extracted_price")
        if not price:
            continue

        title_lower = item.get("title", "").lower()
        category_words = prefs.category.lower().split()
        if not any(word in title_lower for word in category_words):
            print(f"  SKIPPED (wrong category): {item.get('title')}")
            continue

        products.append(
            Product(
                title=item.get("title", "Unknown"),
                brand=item.get("source", "Unknown"),
                price=int(price),
                rating=item.get("rating"),
                reviews=int(item.get("reviews") or 0),
                source=item.get("source", "google_shopping"),
                url=get_best_url(item),
                image=item.get("thumbnail")
            )
        )

    print(f"PRODUCTS PARSED: {len(products)}")
    return products
