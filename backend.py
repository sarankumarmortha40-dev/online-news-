from flask import Flask, render_template
import os
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# ---------------------------
# SAFE NEWS LOADER (FIX HERE)
# ---------------------------
def load_news():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, "news.json")

    if os.path.exists(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print("Error reading news.json:", e)
            return {"data": []}
    else:
        print("⚠️ news.json NOT FOUND — using empty data")
        return {"data": []}

news_data = load_news()
# -------------------------------------

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/world')
def world():
    return render_template('world.html')

@app.route('/entertainment')
def entertainment():
    # Filter entertainment news
    articles = [item for item in news_data["data"] if item["category"] == "entertainment"]
    return render_template('news.html', articles=articles, category_title="Entertainment News")

@app.route('/sports')
def sports():
    # Filter sports news
    articles = [item for item in news_data["data"] if item["category"] == "sports"]
    return render_template('news.html', articles=articles, category_title="Sports News")

@app.route('/geopolitics')
def geopolitics():
   articles = [item for item in news_data["data"] if item["category"] == "geopolitics"]
   return render_template('news.html', articles=articles, category_title="Geopolitics News")

@app.route('/tech')
def tech():
    articles = [item for item in news_data["data"] if item["category"] == "tech"]
    return render_template('news.html', articles=articles, category_title="Tech News")

@app.route('/politics')
def politics():
    articles = [item for item in news_data["data"] if item["category"] == "politics"]
    return render_template('news.html', articles=articles, category_title="Politics News")

@app.route('/health')
def health():
    articles = [item for item in news_data["data"] if item["category"] == "health"]
    return render_template('news.html', articles=articles, category_title="Health News")

@app.route('/favicon')
def favicon():
    return render_template('favicon.ico')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=True)
