import json
import os
from dotenv import load_dotenv
from groq import Groq
from models.preference import UserPreference

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def preference_agent(user_input: str) -> UserPreference:
    prompt = f"""
You are a shopping assistant. Extract the user's shopping intent and return ONLY valid JSON.

Rules:
- "category" must be the PRODUCT TYPE the user wants to buy (e.g. "smartwatch", "phone", "laptop", "earbuds"). Never use a feature as the category.
- "budget" must be a number in INR. If not mentioned, use 50000 as default.
- "priorities" are the features they care about most (e.g. ["battery life", "camera", "performance"]).
- "brand_constraints" are brand restrictions (e.g. ["no Chinese brands"]). Empty list if none.

Examples:
Input: "smartwatch with large battery life under 5000"
Output: {{"category": "smartwatch", "budget": 5000, "priorities": ["battery life"], "brand_constraints": []}}

Input: "best camera phone under 25000 no Chinese brands"
Output: {{"category": "smartphone", "budget": 25000, "priorities": ["camera"], "brand_constraints": ["no Chinese brands"]}}

Input: "gaming laptop under 60000"
Output: {{"category": "gaming laptop", "budget": 60000, "priorities": ["performance"], "brand_constraints": []}}

Now extract from this input:
{user_input}

Return ONLY the JSON object, nothing else.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    text = response.choices[0].message.content.strip()

    # Strip markdown code blocks if present
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    text = text.strip()

    data = json.loads(text)
    return UserPreference(**data)