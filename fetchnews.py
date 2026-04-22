import requests
import os
from db import supabase   # <-- IMPORTANT: import connection to Supabase

# ----------------------------------------
# MEDiASTACK API KEY
# ----------------------------------------
MEDIASTACK_API_KEY = os.getenv("MEDIASTACK_KEY") or "YOUR_MEDIASTACK_API_KEY"

# ----------------------------------------
# CATEGORY MAP
# ----------------------------------------
CATEGORY_MAP = {
    "news": "general",
    "world": "general",
    "sports": "sports",
    "tech": "technology",
    "entertainment": "entertainment",
    "politics": "politics",
    "health": "health"
}

# ----------------------------------------
# FETCH NEWS FROM MEDiASTACK API
# ----------------------------------------
def fetch_mediastack_news(category):
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
            "category": category,
            "title": item.get("title", "No Title"),
            "description": item.get("description", ""),
            "url": item.get("url", "#"),
            "image": item.get("image") or "https://via.placeholder.com/300x200?text=No+Image"
        })

    return final_list


# ----------------------------------------
# SAVE NEWS TO SUPABASE
# ----------------------------------------
def save_news_to_db(category, news_list):
    if not news_list:
        print("No news to save for", category)
        return

    print(f"Saving {len(news_list)} articles to Supabase...")

    # Insert into supabase table
    response = supabase.table("news").insert(news_list).execute()

    print("Supabase response:", response)


