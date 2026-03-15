"""
RSS feeds contain truncated summaries 
here: 
- takes the URL 
- scrapes the full article
- extracts full text
- returns cleaned content
** later extract full article body, clean text and remove unwanted information via BeautifulSoup = HTML parser
** deduplication at DB level 
"""
import re 
import trafilatura 

from storage import (
    init_db, 
    get_unprocessed_articles, 
    update_article_parsed, 
    mark_article_failed
)

def clean_text(text: str) -> str: 
    """
    Clean extracted article text.
    Keeps it simple for now:
    - removes extra whitespace
    - removes repeated blank lines
    """
    if not text:
        return ""

    text = re.sub(r"\s+", " ", text).strip()
    return text

def extract_article_text(url: str) -> str: 
    """
    Download the webpage and extract the main article text. 
    """
    downloaded = trafilatura.fetch_url(url)
    if not downloaded: 
        return ""
    extracted = trafilatura.extract(downloaded)
    return extracted or ""

def main(): 
    init_db()
    articles = get_unprocessed_articles(limit=20)
    print(f"Found {len(articles)} unprocessed articles")

    for article_id, source, title, link in articles: 
        print(f"\nProcessing article {article_id}")
        print(f"Source: {source}")
        print(f"Title: {title}")
        print(f"URL: {link}")

        try: 
            article_text = extract_article_text(link)

            if not article_text: 
                print("No article text extracted")
                mark_article_failed(article_id, fetch_status='no_text_extracted')
                continue 

            cleaned = clean_text(article_text)

            update_article_parsed(
                article_id=article_id,
                article_text=article_text,
                clean_text=cleaned,
                fetch_status="success"
            )

            print("Saved article text successfully")

        except Exception as e:
            print(f"Error: {e}")
            mark_article_failed(article_id, fetch_status=f"error: {str(e)}")


if __name__ == "__main__":
    main()
