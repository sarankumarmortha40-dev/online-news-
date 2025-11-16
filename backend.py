from flask import Flask, render_template
import os
import json
import trafilatura

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Load JSON
def load_json(filename):
    base_path = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_path, filename)

    if os.path.exists(full_path):
        with open(full_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"data": []}

# ⭐ Correct Extract Full Article using Trafilatura
def extract_full_article(url):
    try:
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            article_text = trafilatura.extract(downloaded)
            return article_text
        return "Full article could not be extracted."
    except Exception as e:
        print("Error extracting:", e)
        return "Full article could not be extracted."

# Routes
@app.route("/")
def home():
    data = load_json("news.json")
    return render_template("main.html", articles=data["data"], category="news")

@app.route("/world")
def world():
    data = load_json("world.json")
    return render_template("world.html", articles=data["data"], category="world")

@app.route("/entertainment")
def entertainment():
    data = load_json("entertainment.json")
    return render_template("entertainment.html", articles=data["data"], category="entertainment")

@app.route("/sports")
def sports():
    data = load_json("sports.json")
    return render_template("sports.html", articles=data["data"], category="sports")

@app.route("/tech")
def tech():
    data = load_json("tech.json")
    return render_template("tech.html", articles=data["data"], category="tech")

@app.route("/politics")
def politics():
    data = load_json("politics.json")
    return render_template("politics.html", articles=data["data"], category="politics")

@app.route("/health")
def health():
    data = load_json("health.json")
    return render_template("health.html", articles=data["data"], category="health")

# FULL ARTICLE PAGE
@app.route("/article/<category>/<int:id>")
def article_page(category, id):
    filename = f"{category}.json"
    data = load_json(filename)

    if id < 0 or id >= len(data["data"]):
        return "Article not found", 404

    article = data["data"][id]

    # Extract full article text
    full_content = extract_full_article(article["url"])

    return render_template(
        "article.html",
        article=article,
        full_content=full_content,
        category=category
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
