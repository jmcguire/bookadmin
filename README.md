

# uv notes

brew install uv

uv to manage python versions, and dependencies, and run code

don't touch pip or venv

```
uv add DEPENDENCY
uv add --dev DEPENDENCY
uv remove DEPENDENCY
uv run pytest

uv run python manage.py runserver

uv run python -m django --version
uv run python manage.py shell
uv run python manage.py check

uv run python manage.py makemigrations APPNAME
uv run python manage.py migrate
uv run python manage.py test polls

uv run pytest
uv run python manage.py test
```

when cloning this repo, initially run uv sync

# vs code notes

use ruff to auto-format on save, and auto-sort imports

# other site notes

bookwyrm too slow
hardcover doesn't have leo the late bloomer, takes too many steps to mark a book as read, their top lists isn't personalized, missing young zeus
fable is built to be an app, really app based, does have a nice way to start noting books youve read, where selecing one opens a fields of similar books
goodreads is amazon

# features

easy way to add books and rate books, like old school netflix, hover over and quickly say "read, 0-3 stars, want to read"
get a book info from a picture
use AI to tag authors by race, sex, nationality
distinguish between "author" and "wrote the forward"
on the authors page, can sort by "originally written", "originally published"
when looking up books, multiple versions of a book, with different forwards should be under one book entry, but it should note the versions there
a way to put different translations of one book into the same conversation
sometimes a conversation is on a work, sometimes it's on a translation, but mostly all conversa
on the conversation, there's a little notes on which work a person has read
each editino has a tag of if it's a translation, annotated, abridged

# ideas

a work is an intellectual piece
an edition is a published thing, has an ISBN
this website focuses on works (though a person can decide they've read a specific edition)
an edition is composed of or more provenances

what about an abridged version?
what about a translation?
what about an annotated edition?
are these all the same "thing"
you read a specific one, but you talk on the general one


tables around a work

 - provenance - each source has a line here
 - edition_editorial - manual overrides
 - provenance_to_identity - maps many provenance can be mapped to one identity, with an order of which they will be applied
 - edition_identity - the final entry for one ISBN book, a published version
 - edition - a "rendered" book, is expected to be recreated anytime, has ISBN
 - edition_to_work - edition to work
 - work_editorial - manual overrides
 - work_identity - the final entry for a book on the website, could be comprised of multiple specificbooks, has an original written date, a first published date
 - work - a "rendered" book with the general information, title, author, description. the intellectual work.

some normalized data:

 - author - given, family, sorted ("family, given"), full name ("given family", given nationality), nationality, sex, gay
 - publisher

tables around my organization:

 - work_groups - name of group, type (enum, e.g. series, translation)

work can be in mulitple groups
these are not user created
a group could be like "translations of an original intellectual work"
a group coule be "harry potter"


tables around interacting with a work

 - user - 
 - user_rating - 
 - conversation - an abstract place where a single conversation happens
 - conversation_to_work - each conversation can be part of multiple works
 - conversation_to_series - each conversation can be part of multiple series
 - message - on a conversation, some text and a user, can mark it as a review, otherwise a message is limited to a smaller size (reviews can be larger)
 - user_read
 - user_want_to_read - includes who recommended it, maybe a link to a message or a user
 - update - an update a user makes on their wall



any review is specific for a work
a work can be part of a series
a work can be part of a translation group

conversation is a specific thing, separate from anything
but it can be shown on a page, and often is connected to a work, to a series, to the original untranslated work
this way we can just "attach" the same conversationto multiple "translations" of a book
or a whole series

# API

## backend

