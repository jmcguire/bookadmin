import gzip
import json
import time
from pathlib import Path
from urllib.request import Request, urlopen

output = Path("downloads")
output.mkdir(parents=True, exist_ok=True)

USER_AGENT = "BooksiteSampleImporter/0.1 (contact: jm@landedstar.com)"


def fetch(path):
    time.sleep(30)
    url = f"https://openlibrary.org{path}"
    print(url)

    request = Request(url, headers={"User-Agent": USER_AGENT})

    with urlopen(request, timeout=30) as response:
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


books = [
    "OL61981W",  # the iliad
    "OL157104W",  # life and fate
    "OL8386917W",  # erasure
    "OL16653954W",  # a short stay in hell
    "OL19956036W",  # old and cold
    "OL14858392W",  # to say nothing of the dog
    "OL9591154W",  # angel whispers
    "OL19764030W",  # on gravity
    "OL14866001W",  # citizens
    "OL491846W",  # black hack down
    "OL51158W",  # battle cry of freedom
]

all_authors = []
all_editions = []
all_works = []
for book in books:
    work = fetch(f"/works/{book}.json")
    editions = fetch(f"/works/{book}/editions.json?limit=10")["entries"]
    author_keys = {entry["author"]["key"] for entry in work.get("authors", [])}
    authors = [fetch(f"{key}.json") for key in author_keys]

    all_works.append(work)
    all_editions.extend(editions)
    all_authors.extend(authors)

save("works.txt.gz", all_works)
save("editions.txt.gz", all_editions)
save("authors.txt.gz", all_authors)
