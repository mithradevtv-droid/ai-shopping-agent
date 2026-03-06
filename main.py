from agents.preference_agent import preference_agent
from agents.normalization_agent import normalize_preferences
from agents.aggregator_search_agent import aggregator_search_agent
from agents.ranking_agent import ranking_agent

user_input = input("What do you want to buy? ")

prefs = preference_agent(user_input)
prefs = normalize_preferences(prefs)

print("\nNormalized preferences:")
print(prefs)

products = aggregator_search_agent(prefs)

print(f"\nDEBUG: Found {len(products)} products before ranking")

ranked_products = ranking_agent(products, prefs)

print("\nBest options:")
for p in ranked_products[:5]:
    print(f"- {p.title} | ₹{p.price} | ⭐ {p.rating} | {p.source}")