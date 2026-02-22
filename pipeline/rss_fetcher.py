import feedparser
from config.rss_sources import rss_sources


def fetch_all_feeds():
    all_articles = []

    for source_name, url in rss_sources.items():
        feed = feedparser.parse(url)

        for entry in feed.entries:
            article = {
                "source": source_name,
                "title": entry.get("title"),
                "link": entry.get("link"),
                "published": entry.get("published", ""),
                "summary": entry.get("summary", "")
            }
            all_articles.append(article)

    return all_articles