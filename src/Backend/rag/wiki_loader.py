import os
import requests

def fetch_wikipedia_article(title):

    url = "https://en.wikipedia.org/w/api.php"

    headers = {
        "User-Agent": "MultiSourceRAG/1.0 (https://github.com/your-repo)"
    }

    params = {
        "action": "query",
        "prop": "extracts",
        "explaintext": True,
        "titles": title.replace("_", " "),
        "format": "json"
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        print(f"HTTP Error {response.status_code} for {title}")
        return None

    data = response.json()

    pages = data["query"]["pages"]

    for page_id in pages:
        return pages[page_id].get("extract")

    return None


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
DATA_DIR = os.path.join(BASE_DIR, "data", "wiki")

def save_article(title):

    text = fetch_wikipedia_article(title)

    if not text:
        print(f"Failed to fetch {title}")
        return

    os.makedirs(DATA_DIR, exist_ok=True)

    file_path = os.path.join(DATA_DIR, f"{title}.txt")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"Saved {title} in {DATA_DIR}")