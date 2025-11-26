import requests

# Your Render app base URL
BASE_URL = "https://online-news-d80e.onrender.com/"

# All categories you want to refresh
CATEGORIES = [
    "news",
    "world",
    "sports",
    "tech",
    "health",
    "politics",
    "entertainment"
]

for cat in CATEGORIES:
    try:
        url = f"{BASE_URL}/update-news/{cat}"
        print("Updating:", url)
        r = requests.get(url)
        print("Response:", r.text)
    except Exception as e:
        print("Error updating", cat, ":", e)
