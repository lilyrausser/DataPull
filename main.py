from pipeline.rss_fetcher import fetch_all_feeds
from pipeline.storage import init_db, save_articles


def run():
    print("Initializing database...")
    init_db()

    print("Fetching RSS feeds...")
    articles = fetch_all_feeds()

    print(f"Fetched {len(articles)} articles")

    print("Saving to database...")
    save_articles(articles)

    print("Done.")


if __name__ == "__main__":
    run()