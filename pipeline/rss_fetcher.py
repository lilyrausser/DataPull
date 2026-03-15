import feedparser
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from config.rss_sources import rss_sources
from config.lexicon import INVESTMENT_TERMS


def parse_entry_date(entry):
    date_str = entry.get('published', "") or entry.get('updated', "")
    if not date_str: 
        return None, ""

    try: 
        dt = parsedate_to_datetime(date_str)
        if dt.tzinfo is None: 
            dt = dt.replace(tzinfo=timezone.utc)
        return dt, date_str 
    except Exception: 
        return None, date_str 

def matches_lexicon(text, terms): 
    text = text.lower()
    return any(term in text for term in terms)

def fetch_all_feeds(days_back=7):
    all_articles = []
    cutoff = datetime.now(timezone.utc) - timedelta(days=days_back)

    for source_name, url in rss_sources.items():
        feed = feedparser.parse(url)
        total_seen = 0
        date_matched = 0 
        lexicon_matched = 0


        for entry in feed.entries:
            total_seen +=1 
            published_dt, published_str = parse_entry_date(entry)

            #skip articles older than cutoff when date is available 
            if published_dt is not None and published_dt < cutoff: 
                continue 

            date_matched += 1
            title = entry.get('title', "")
            summary = entry.get("summary", "")
            link = entry.get("link", "")
            combined_text = f"{title} {summary}"

            if not matches_lexicon(combined_text, INVESTMENT_TERMS):
                continue 
            lexicon_matched += 1

            if link: 
                article = {
                    "source": source_name, 
                    "title": title, 
                    "link": link, 
                    "published": published_str, 
                    "summary": summary 
                }
                all_articles.append(article)

        print(
            f"{source_name}: ", 
            f"saw {total_seen}, "
            f"{date_matched} within last {days_back} days, "
            f"{lexicon_matched} matched lexicon"
        )
    return all_articles 