# take one

I'd use Django + PostgreSQL, with server-rendered HTML and a little JavaScript where needed.

Django is particularly well suited to your plan because it comes with an administrative interface, authentication, database models, migrations, and templating. You can concentrate on the book data instead of building website infrastructure.

And I agree with building the admin panel first.

## 1. Recommended technology stack

| Component            | Technology                   |
| -------------------- | ---------------------------- |
| Language             | Python                       |
| Web framework        | Django                       |
| Database             | PostgreSQL                   |
| Database access      | Django ORM                   |
| Frontend rendering   | Django templates             |
| Dynamic interactions | HTMX + occasional JavaScript |
| Styling              | CSS                          |
| Import processing    | Python management commands   |
| Resolution engine    | Ordinary Python package      |
| Testing              | pytest + pytest-django       |

[HTMX](https://htmx.org/docs/?utm_source=chatgpt.com) is especially interesting here. It lets you update parts of a page by making requests that return HTML fragments, rather than building a separate JavaScript frontend and JSON API.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://htmx.org\&sz=32)

htmx



You could use it for instant book searches, editable metadata fields, and previews of resolved records.

I would not start with React, Next.js, or a separate FastAPI service.

## 2. Your admin panel is nearly built already

Django has a built-in admin site that automatically creates CRUD interfaces for your database models, including searching, filtering, and editing records. It supports custom pages and actions.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://docs.djangoproject.com\&sz=32)

Django



Your initial book-management interface could look roughly like this:

Book administration

Internal

Search by title, author, ISBN, or source ID

[Dune | Frank Herbert | First Edition](https://images.openai.com/static-rsc-4/bqdZjj4SunCu_vt9FwRXKy1e_QNSu5eep2F3D1hnW0-EGJOLg2uR6BRL-WKewPUI-iqZIT5QVAEzPca-cx5Qqf6wPOIRbpSBB1CS6_oY_TcqplTwJpfWWbfPYpA2QRrxsO72yJFSGadataXtdXWudLKrNgYrIwMAHlpGNwPXCc4?purpose=inline)

Dune

Frank Herbert · Internal work #123

Open Library: 2 linked works

Editions: 87 · Overrides: 2

Field resolution

| Title       | Dune              | Open Library |
| ----------- | ----------------- | ------------ |
| Genres      | Sci-fi, Adventure | Editorial    |
| Description | Custom text       | Editorial    |

Edit overrides

View sources

Resolve work

Conceptual admin screen, not a functional interface.

Django won't generate that entire interface automatically. But it gives you the framework to extend, rather than starting from nothing.

## 3. How I'd run the resolution engine

I'd write the resolution engine as ordinary Python code, independent of the web interface.

One central function:

```
resolve_work(work_id)
```

It reads provenance, identity mappings, and editorial overrides, then writes the resolved result into the catalog.

You can invoke it in three ways:

| Trigger                | Behavior                       |
| ---------------------- | ------------------------------ |
| Admin clicks "Resolve" | Rebuild one book immediately   |
| Monthly source import  | Rebuild only affected books    |
| Full rebuild command   | Recalculate the entire catalog |

For example, you could add Django management commands:

```
python manage.py resolve_catalog --work-id 123
python manage.py resolve_catalog --changed-only
python manage.py resolve_catalog --all
```

Django supports custom management commands specifically for this sort of administrative processing.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://docs.djangoproject.com\&sz=32)

Django



I'd run full imports and rebuilds as separate processes, not inside web requests. The admin panel can submit a job and display its progress.

For the full Open Library dataset, I'd also use PostgreSQL bulk loading rather than calling Django's ORM `.save()` tens of millions of times.

## 4. Pre-rendering versus server-side rendering

There's an important distinction:

- Static pre-rendering: Generate HTML files in advance and serve them.
- Server-side rendering: Generate HTML in response to requests using database data.
- Client-side rendering: JavaScript fetches data and builds the page in the browser.

I'd choose server-side rendering initially.

Your catalog database is already materialized by the resolution engine. Displaying a book page only requires fetching a resolved record and rendering a template.

For ten users, this should be plenty fast. Django also supports caching entire pages or individual template fragments if you eventually need it.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://docs.djangoproject.com\&sz=32)

Django



The public site can use HTMX for conversations, TBR filtering, and other interactive features without becoming a full JavaScript application.

## 5. How I'd organize the Python project

```
booksite/
├── config/             # Django settings
├── books/
│   ├── models.py       # Database models
│   ├── admin.py        # Django admin customization
│   ├── resolver.py     # Book resolution logic
│   ├── matching.py     # Work/edition matching
│   ├── importers/
│   │   ├── openlibrary.py
│   │   └── isbndb.py
│   └── management/
│       └── commands/
├── readers/            # User libraries, TBR, profiles
├── conversations/      # Social functionality
└── templates/          # Server-rendered HTML
```

Those are organizational boundaries, not separate services. Everything can remain in one Django project.

## 6. What I'd build first

1. Set up Django, PostgreSQL, and pytest.
2. Create the provenance, identity, editorial, and catalog models.
3. Import 1,000 Open Library works and their editions.
4. Browse and search them through Django admin.
5. Implement `resolve_work()`, including field provenance.
6. Add a custom admin page showing each source's values alongside the resolved values.
7. Add editorial overrides and a "Re-resolve" action.
8. Scale ingestion to the full Open Library dump.

Then build the public-facing site.

The trickiest interface will probably be manually merging and splitting works, not editing individual fields.

My recommendation is to use Django for both the admin and public websites, at least initially. You can give them completely different interfaces while sharing the same models and business logic. There is very little reason to maintain separate applications yet.

Start here: [Django's official tutorial](https://docs.djangoproject.com/en/6.0/intro/tutorial01/?utm_source=chatgpt.com), particularly [Part 2: Models and the Admin Site](https://docs.djangoproject.com/en/6.0/intro/tutorial02/?utm_source=chatgpt.com).

# take two

We've settled on quite a bit of the architecture. The central idea is a standalone bibliographic ingestion and normalization system that collects book data from multiple providers, reconciles identities, supports manual corrections, and publishes a clean catalog.

Your social-reading website would be one consumer of that catalog. Other applications could potentially use it too.

## 1. Overall architecture

We settled on four logical layers:

1\. Provenance

Original Open Library, ISBNdb, and other source records, preserved independently

2\. Identity

Determines which source records refer to the same work, edition, or author

3\. Resolution engine + Editorial

Applies source priorities and human corrections to produce canonical records

4\. Catalog

Final structured records, ready for websites, search, and APIs

These are logical boundaries. We decided they could all be ordinary tables in one PostgreSQL schema, rather than separate databases or PostgreSQL schemas.

## 2. Bibliographic model

We examined Open Library, Goodreads, StoryGraph, LibraryThing, Google Books, and traditional library standards.

We settled on these core concepts:

| Entity           | Meaning                                                          |
| ---------------- | ---------------------------------------------------------------- |
| Work             | Abstract book, e.g. Moby-Dick                                    |
| Edition          | Specific publication, translation, format, or printing           |
| Author           | Canonical author identity, independent of individual books       |
| Source record    | What one external provider says about a work, edition, or author |
| Identity mapping | Links external records to your internal IDs                      |

One work has many editions. Each edition can have ISBN identifiers; some have none. Multiple provenance sources can describe the same work or edition.

Translations ordinarily belong to the same work. Adaptations and collections require more careful handling.

We also decided to preserve author `display_name` and `sort_name` independently, since proper author sorting is important and providers rarely supply reliably structured first and last names.

One thing we haven't settled: whether to eventually implement the more elaborate library-science concept of an expression between work and edition. The initial model doesn't need it.

## 3. Provenance and editorial corrections

This was one of your strongest requirements.

We never overwrite original provider data with our own corrections.

For example, a canonical work could be assembled from:

- Open Library work record
- ISBNdb records for related editions
- Open Book Genome genre classifications
- Custom editorial overrides

Each provider's original information remains available.

The resolution engine uses field-specific priority rules, such as:

```
TITLE_PRIORITY = ["editorial", "isbndb", "openlibrary"]DESCRIPTION_PRIORITY = ["editorial", "openlibrary", "isbndb"]
```

We agreed that maintaining these rules manually in Python is fine. You don't need an elaborate configurable rules engine.

Editorial overrides are field-level, permanent until removed, and auditable. Identity corrections are separate: they control whether two source records represent the same entity.

We also discussed recording which source contributed each resolved field.

## 4. Open Library ingestion

Open Library is the initial primary data source.

At the time we researched it, its catalog contained approximately:

- 42 million works
- 57 million editions
- 15 million authors

It publishes monthly full dumps containing both new and updated records.

We established that:

- Source records include identifiers, revisions, and modification timestamps.
- Revisions can identify records that changed between imports.
- Redirect records indicate merged identities.
- Deletion information must also be processed.
- An Open Library merge should not automatically destroy or merge your own canonical work identities.
- Original compressed dumps could be archived separately for reproducibility.

The import pipeline needs to handle monthly updates without losing editorial changes.

## 5. Other metadata providers

These were our candidate sources:

| Provider             | Intended use                                                                  |
| -------------------- | ----------------------------------------------------------------------------- |
| Open Library         | Primary work, edition, author and cover metadata                              |
| ISBNdb               | Supplemental ISBN-level publication metadata                                  |
| Google Books         | Supplemental categories and other metadata, subject to licensing restrictions |
| Open Book Genome     | Normalized genre classifications                                              |
| ONIX/publisher feeds | Potential future metadata source                                              |

We decided each provider should have its own Python adapter, converting its records into a common internal representation.

But the original source JSON should also be retained, ideally using PostgreSQL `JSONB`.

We discussed maintaining only one to three primary genres per work, from a controlled vocabulary, while preserving the more extensive original subjects.

For covers, we considered using Open Library's cover service initially and storing additional permitted images externally. Spine images would probably be generated rather than downloaded.

## 6. Technology choices

These were fairly firm decisions.

| Component             | Decision                            |
| --------------------- | ----------------------------------- |
| Language              | Python                              |
| Web framework         | Django                              |
| Database              | PostgreSQL                          |
| Dependency management | `uv`                                |
| Testing               | pytest + pytest-django              |
| Linting/formatting    | Ruff                                |
| Raw provider records  | PostgreSQL JSONB                    |
| Canonical catalog     | Relational PostgreSQL tables        |
| Batch processing      | Python / Django management commands |
| Initial frontend      | Django admin                        |
| Containers            | Deferred                            |

We specifically discussed using Django's built-in admin rather than building an administrative interface from scratch.

We also decided on one PostgreSQL schema with descriptively named tables, rather than four PostgreSQL schemas.

## 7. Admin-first development

The administrative application is the first thing we want to build.

It should support:

- Searching works, editions, and authors.
- Inspecting all source records contributing to an entity.
- Comparing provider values against the resolved values.
- Adding, changing, or removing editorial overrides.
- Correcting identity matches and work/edition relationships.
- Triggering resolution for one entity.
- Running bulk imports and rebuilding the catalog.
- Reviewing questionable automatic matches.

Resolution should be ordinary Python logic, callable independently of an HTTP request.

We discussed commands conceptually like:

```
uv run python manage.py import_openlibrary
uv run python manage.py resolve_catalog --work-id 123
uv run python manage.py resolve_catalog --changed-only
uv run python manage.py resolve_catalog --all
```

These commands haven't been implemented yet.

## 8. What's changed with your new direction

Previously, we envisioned one Django project containing the catalog, admin, and eventual social website.

Now you're considering a standalone catalog system that could serve multiple applications.

I think that's a useful boundary to establish now, without necessarily creating a separate deployed microservice.

I'd organize the repository something like:

```
bookcatalog/
├── config/             # Django configuration
├── provenance/         # Provider records and importers
├── identity/           # Matching, merging, relationships
├── editorial/          # Overrides and audit history
├── catalog/            # Final resolved data
├── resolution/         # Resolution engine
├── api/                # External catalog access (later)
├── templates/          # Custom admin views
├── tests/
├── manage.py
├── pyproject.toml
└── uv.lock
```

This is a proposed refinement, not a structure we've already committed to.

The social-reading site would eventually use the catalog through a stable interface. It wouldn't need to know how Open Library works, what ISBNdb provides, or how editorial precedence rules operate.

## 9. What we haven't decided

The remaining architectural questions are:

1. Identity matching: Exact rules and confidence thresholds for deciding when records describe the same work or edition.
2. Import scale: Whether to bulk-import the entire Open Library catalog immediately or begin with a limited sample.
3. Data publication: Whether the resolved catalog is exposed through a REST API, direct database access, or bulk exports.
4. Resolution strategy: Incremental updates versus complete rebuilding, and how to ensure resolution is reproducible.
5. Provider licenses: What supplemental metadata we may legally retain and redistribute to other applications.
6. Catalog versioning: Whether consumers can access historical resolved records or only the latest version.

### Where I'd resume

I'd start by building a very small but complete vertical slice:

Import 100 Open Library works, their editions, and authors → establish canonical identities → inspect them in Django admin → apply a correction → resolve them into the catalog → import an updated source record and verify the correction survives.

That tests the essential architecture before we process tens of millions of records.

The most important new decision is whether this system is simply an independently maintained component of your book-social website, or a reusable bibliographic data product with its own public API. We can design for the latter without prematurely deploying separate services.
