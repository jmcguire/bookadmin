import gzip
import json
from pathlib import Path
from urllib.request import urlopen

output = Path("downloads")
output.mkdir(parents=True, exist_ok=True)


def fetch(path):
    with urlopen(f"https://openlibrary.org{path}", timeout=30) as response:
        return json.load(response)


def save(filename, records):
    with gzip.open(output / filename, "wt", encoding="utf-8") as f:
        for record in records:
            modified = record.get("last_modified", {})
            modified = (
                modified.get("value", "") if isinstance(modified, dict) else modified
            )
            record_type = record.get("type", {}).get("key", "")

            row = [
                record_type,
                record["key"],
                str(record.get("revision", 0)),
                modified or "",
                json.dumps(record, ensure_ascii=False),
            ]
            f.write("\t".join(row) + "\n")


work = fetch("/works/OL27482W.json")  # The Hobbit
editions = fetch("/works/OL27482W/editions.json?limit=10")["entries"]

author_keys = {entry["author"]["key"] for entry in work.get("authors", [])}
authors = [fetch(f"{key}.json") for key in author_keys]

save("works.txt.gz", [work])
save("editions.txt.gz", editions)
save("authors.txt.gz", authors)
