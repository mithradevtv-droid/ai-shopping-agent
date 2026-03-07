from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

from agents.preference_agent import preference_agent
from agents.normalization_agent import normalize_preferences
from agents.aggregator_search_agent import aggregator_search_agent
from agents.ranking_agent import ranking_agent

app = Flask(__name__, static_folder="static")
CORS(app)


@app.route("/")
def index():
    response = send_from_directory("static", "index.html")
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


@app.route("/search", methods=["POST"])
def search():
    data = request.get_json()
    user_input = data.get("query", "").strip()

    if not user_input:
        return jsonify({"error": "No query provided"}), 400

    try:
        prefs = preference_agent(user_input)
        prefs = normalize_preferences(prefs)
        products = aggregator_search_agent(prefs)
        ranked = ranking_agent(products, prefs)

        results = []
        for p in ranked[:10]:
            results.append({
                "title":   p.title,
                "brand":   p.brand,
                "price":   p.price,
                "rating":  p.rating,
                "reviews": p.reviews,
                "source":  p.source,
                "url":     p.url,
                "image":   p.image,
            })

        return jsonify({
            "query":             user_input,
            "category":          prefs.category,
            "budget":            prefs.budget,
            "priorities":        prefs.priorities,
            "brand_constraints": prefs.brand_constraints,
            "results":           results,
            "total":             len(results)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
