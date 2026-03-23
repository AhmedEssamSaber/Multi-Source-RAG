from src.Backend.rag.wiki_loader import save_article

articles = [
    "Machine_learning",
    "Neural_network",
    "Natural_language_processing"
]

for article in articles:
    print(f"Downloading: {article}")
    save_article(article)
    print(f"Saved: {article}")