from typing import List
from serpapi import GoogleSearch
from models.product import Product
from models.preference import UserPreference
import os


def aggregator_search_agent(prefs: UserPreference) -> List[Product]:
    query_parts = [
        prefs.category,
        " ".join(prefs.priorities),
        f"under {prefs.budget}"
    ]

    query = " ".join(query_parts)

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
        # Use extracted_price (already a number) instead of parsing price string
        price = item.get("extracted_price")
        if not price:
            continue

        # SerpAPI uses product_link, not link
        link = item.get("product_link")
        if not link:
            continue

        products.append(
            Product(
                title=item.get("title", "Unknown"),
                brand=item.get("source", "Unknown"),
                price=int(price),
                rating=item.get("rating"),
                reviews=item.get("reviews"),
                source=item.get("source", "google_shopping"),
                url=link,
                image=item.get("thumbnail")
            )
        )

    print(f"PRODUCTS PARSED: {len(products)}")
    return products