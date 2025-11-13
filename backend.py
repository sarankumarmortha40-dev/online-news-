from flask import Flask, render_template
import os
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load news data from JSON file
with open("news.json", "r", encoding="utf-8") as f:
    news_data = json.load(f)

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
    return render_template('geopolitics.html')

@app.route('/tech')
def tech():
    return render_template('tech.html')

@app.route('/politics')
def politics():
    return render_template('politics.html')

@app.route('/favicon')
def favicon():
    return render_template('favicon.ico')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=True)
