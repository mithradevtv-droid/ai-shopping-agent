from typing import List
from models.product import Product
from models.preference import UserPreference


CHINESE_BRANDS = [
    "Xiaomi", "Redmi", "Realme", "Oppo", "Vivo",
    "OnePlus", "iQOO", "Poco", "Huawei", "Honor"
]


def is_chinese_brand(brand: str) -> bool:
    return brand.lower() in [b.lower() for b in CHINESE_BRANDS]


def score_product(product: Product, prefs: UserPreference) -> float:
    """Higher score = better product"""
    score = 0.0

    if product.rating:
        score += product.rating * 10

    # Price advantage (cheaper within budget is better)
    score += max(0, (prefs.budget - product.price) / 1000)

    return score


def ranking_agent(products: List[Product], prefs: UserPreference) -> List[Product]:
    filtered = []

    # Normalize constraints for reliable matching
    constraints = " ".join(prefs.brand_constraints).lower()
    block_chinese = "no_chinese" in constraints or "no chinese" in constraints

    for p in products:
        # Budget filter
        if p.price > prefs.budget:
            continue

        # Brand constraint
        if block_chinese and is_chinese_brand(p.brand):
            continue

        filtered.append(p)

    # Rank by score (highest first)
    ranked = sorted(
        filtered,
        key=lambda p: score_product(p, prefs),
        reverse=True
    )

    return ranked