from flask import Flask, render_template
import os
app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/world')
def world():
    return render_template('world.html')

@app.route('/entertainment')
def entertainment():
    return render_template('entertainment.html')

@app.route('/sports')
def sports():
    return render_template('sports.html')

@app.route('/international')
def international():
    return render_template('international.html')

@app.route('/geopolitics')
def geopolitics():
    return render_template('geopolitics.html')

@app.route('/tech')
def tech():
    return render_template('tech.html')

@app.route('/favicon')
def favicon():
    return render_template('favicon.ico')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)