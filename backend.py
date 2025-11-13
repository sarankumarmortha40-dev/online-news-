from flask import Flask, render_template
import os
import json

app = Flask(__name__)
app.secret_key = "your_secret_key"

def load_json(filename):
    base_path = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_path, filename)

    if os.path.exists(full_path):
        with open(full_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"data": []}

@app.route("/")
def home():
    data = load_json("news.json")
    return render_template("main.html", articles=data["data"], category_title="Home News")

@app.route("/world")
def world():
    data = load_json("world.json")
    return render_template("world.html", articles=data["data"], category_title="World News")

@app.route("/entertainment")
def entertainment():
    data = load_json("entertainment.json")
    return render_template("entertainment.html", articles=data["data"], category_title="Entertainment News")

@app.route("/sports")
def sports():
    data = load_json("sports.json")
    return render_template("sports.html", articles=data["data"], category_title="Sports News")

@app.route("/tech")
def tech():
    data = load_json("tech.json")
    return render_template("tech.html", articles=data["data"], category_title="Tech News")

@app.route("/politics")
def politics():
    data = load_json("politics.json")
    return render_template("politics.html", articles=data["data"], category_title="Politics News")

@app.route("/health")
def health():
    data = load_json("health.json")
    return render_template("health.html", articles=data["data"], category_title="Health News")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
