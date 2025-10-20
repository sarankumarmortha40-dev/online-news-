import requests

# Your API key
API_KEY = "a0a7b8c9114a89994e10b2a916dfd857"

# Base URL
BASE_URL = "http://api.mediastack.com/v1/news"

# Parameters
params = {
    "access_key": API_KEY,
    "categories": "health,-sports",  # health news, exclude sports
    "languages": "en",              # only English articles
    "limit": 10                     # number of results
}

# Make the GET request
response = requests.get(BASE_URL, params=params)

# Check if request is successful
if response.status_code == 200:
    data = response.json()
    
    # Loop through news data
    for article in data.get("data", []):
        print(f"Title: {article.get('title')}")
        print(f"Source: {article.get('source')}")
        print(f"Published At: {article.get('published_at')}")
        print(f"URL: {article.get('url')}")
        print("-" * 60)
else:
    print("Error:", response.status_code, response.text)
