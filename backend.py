from flask import Flask, render_template, request, jsonify
import os
import json
import trafilatura
from groq import Groq

app = Flask(__name__)
app.secret_key = "your_secret_key"

# ----------------------------
# SAFE GROQ CONFIG
# ----------------------------
api_key = os.getenv("GROQ_API_KEY")

if api_key:
    client = Groq(api_key=api_key)
else:
    client = None
    print("⚠️ GROQ_API_KEY not set — AI disabled")

# ----------------------------
# LOAD JSON
# ----------------------------
def load_json(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return {"data": []}

# ----------------------------
# ARTICLE EXTRACTION
# ----------------------------
def extract_full_article(url):
    try:
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            return trafilatura.extract(downloaded)
    except Exception as e:
        print("Error extracting article:", e)
    return "Full article could not be extracted."

# ----------------------------
# SAFE AI CALL
# ----------------------------
def call_llama(prompt):
    if not client:
        return "⚠️ AI service not available"

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        print("Groq Error:", e)
        return "⚠️ AI service failed"

# ----------------------------
# AI ROUTES
# ----------------------------
@app.route("/translate", methods=["POST"])
def translate():
    data = request.get_json()
    text = data.get("text", "")
    lang = data.get("language", "English")

    prompt = f"Translate this article into {lang}:\n\n{text}"
    result = call_llama(prompt)

    return jsonify({"translation": result})

@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.get_json()
    text = data.get("text", "")

    prompt = f"Summarize this news in 3 simple lines:\n\n{text}"
    result = call_llama(prompt)

    return jsonify({"summary": result})

@app.route("/explain", methods=["POST"])
def explain():
    data = request.get_json()
    text = data.get("text", "")

    prompt = f"Explain this news in simple words:\n\n{text}"
    result = call_llama(prompt)

    return jsonify({"explanation": result})

# ----------------------------
# ROUTES
# ----------------------------
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

# ----------------------------
# ARTICLE PAGE
# ----------------------------
@app.route("/article/<category>/<int:id>")
def article_page(category, id):
    data = load_json(f"{category}.json")

    if id < 0 or id >= len(data["data"]):
        return "Article not found", 404

    article = data["data"][id]
    full_content = extract_full_article(article.get("url", ""))

    return render_template("article.html",
                           article=article,
                           full_content=full_content,
                           category=category)

# ----------------------------
# HEALTH CHECK
# ----------------------------
@app.route("/health-check")
def health_check():
    return "OK", 200

# ----------------------------
# RUN
# ----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)