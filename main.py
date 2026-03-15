import argparse 
from pipeline.rss_fetcher import fetch_all_feeds
from pipeline.storage import init_db, save_articles


def run(days_back):
    print("Initializing database...")
    init_db()

    print(f"Fetching RSS feeds from the last {days_back} days...")
    articles = fetch_all_feeds(days_back=days_back)
    print(f"Fetched {len(articles)} articles")

    print("Saving to database...")
    new_count = save_articles(articles)
    print(f"Inserted {new_count} new articles")

    print("Done.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--days-back', type=int, default=14, 
                        help= 'How many days back to fetch from RSS feeds')
    args = parser.parse_args()
    run(days_back=args.days_back)

