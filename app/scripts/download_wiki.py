from app.models.wiki_model import WikiLoader

wiki = WikiLoader()

articles = [
    "Machine_learning",
    "Neural_network",
    "Natural_language_processing"
]

for article in articles:
    print(f"Downloading: {article}")
    wiki.save(article)