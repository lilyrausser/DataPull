# VC DataPull

A simple Python project that pulls startup and venture news from RSS feeds, filters for relevant articles using a keyword list, and saves results to a local SQLite database.

## What it does

- pulls articles from selected RSS feeds
- checks for keyword matches in the title and summary
- keeps recent articles
- saves matching articles to a database for later review

## Main files

```text
main.py           # runs the pipeline
vc_data.db        # SQLite database of saved articles
requirements.txt  # Python packages needed
README.md         # project overview and instructions
```
## Data saved

Each saved article includes:
- source
- title
- link
- published date
- summary
- fetched time


## Set up 
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run the project 
```
python main.py
```

## Example Output 

Initializing database...
Fetching RSS feeds from the last 7 days...
TechCrunch: saw 20, 20 within last 7 days, 5 matched lexicon
Crunchbase News: saw 10, 10 within last 7 days, 6 matched lexicon
Fetched 22 articles
Saving to database...
Inserted 22 new articles
Done.

## View the database 
In the terminal: 
```
sqlite3 vc_data.db
```
