# when deciding to delete certain files from the DB 
from pipeline.storage import delete_source

sources_to_delete = ["Product Hunt", "Hacker News", "MarkTechPost"]

for source in sources_to_delete:
    delete_source(source)
    print(f"Deleted articles from: {source}")