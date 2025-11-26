import requests
import json
import os

# ----------------------------------------
# MEDiASTACK API KEY
# ----------------------------------------
MEDIASTACK_API_KEY = os.getenv("a0a7b8c9114a89994e10b2a916dfd857") 

# ----------------------------------------
# CATEGORY MAP:
# Your frontend categories -> Mediastack categories
# ----------------------------------------
CATEGORY_MAP = {
    "news": "general",
    "world": "general",        # Mediastack has no "world" category
    "sports": "sports",
    "tech": "technology",
    "entertainment": "entertainment",
    "politics": "politics",
    "health": "health"
}

# ----------------------------------------
# FETCH NEWS FROM MEDiASTACK
# ----------------------------------------
def fetch_mediastack_news(category):
    """
    category = your website category (news/sports/etc.)
    """

    if category not in CATEGORY_MAP:
        print("Invalid category:", category)
        return []

    api_category = CATEGORY_MAP[category]

    url = (
        f"http://api.mediastack.com/v1/news?"
        f"access_key={MEDIASTACK_API_KEY}&"
        f"countries=in&"
        f"languages=en&"
        f"categories={api_category}&"
        f"limit=50"
    )

    print(f"Fetching: {category} -> {api_category}")
    response = requests.get(url).json()

    if "data" not in response:
        print("API ERROR:", response)
        return []

    final_list = []

    for item in response["data"]:
        final_list.append({
            "title": item.get("title", "No Title"),
            "description": item.get("description", ""),
            "url": item.get("url", "#"),
            "img": item.get("image") or "/static/no-image.png"
        })

    return final_list


# ----------------------------------------
# SAVE JSON
# ----------------------------------------
def save_news_to_json(category, news_list):
    file_path = f"{category}.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump({"data": news_list}, f, indent=4, ensure_ascii=False)

    print(f"Saved {len(news_list)} articles to {file_path}")
