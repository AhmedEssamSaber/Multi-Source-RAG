import os
import requests


class WikiLoader:

    def __init__(self):
        self.base_dir = os.path.abspath(".")
        self.data_dir = os.path.join(self.base_dir, "data", "wiki")

    def fetch(self, title):

        url = "https://en.wikipedia.org/w/api.php"

        params = {
            "action": "query",
            "prop": "extracts",
            "explaintext": True,
            "titles": title.replace("_", " "),
            "format": "json"
        }

        res = requests.get(url, params=params)

        if res.status_code != 200:
            return None

        data = res.json()
        pages = data["query"]["pages"]

        for page_id in pages:
            return pages[page_id].get("extract")

        return None

    def save(self, title):

        text = self.fetch(title)

        if not text:
            print(f"Failed: {title}")
            return

        os.makedirs(self.data_dir, exist_ok=True)

        path = os.path.join(self.data_dir, f"{title}.txt")

        with open(path, "w", encoding="utf-8") as f:
            f.write(text)

        print(f"Saved: {title}")