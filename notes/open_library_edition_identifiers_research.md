# Open Library edition identifiers: APIs, bulk data, and reuse rights

**Research snapshot:** November 27, 2026  
**Context:** Booksite bibliographic ingestion / provenance and identity resolution  
**Scope:** 22 non-ISBN identifier keys observed in Open Library *edition* records. The counts below were supplied from the user's analysis of the October 31, 2026 Open Library edition dump.

> **Important:** These counts are the number of edition records containing a given identifier **key**, not the number of distinct external identifiers, books, or authoritative matches. The original investigation was a research survey, **not a legal opinion**. Licenses, API terms, export availability, and commercial usage policies should be reconfirmed against each provider before implementing bulk harvesting or redistribution. In particular, a public API does **not** imply a right to maintain a permanent local copy of its data.

## At-a-glance comparison

| Open Library key | Records | Source / meaning | Individual lookup / API | Bulk download / harvest | Licensing and retention considerations |
|---|---:|---|---|---|---|
| `goodreads` | 6,460,102 | Goodreads book / edition-oriented identifiers | Legacy API retired to new developers; public web pages exist | No licensed public full dump established | Proprietary; no general permission to harvest or republish catalog/reviews. **Cross-reference/link only** by default. |
| `librarything` | 4,301,061 | LibraryThing **work** IDs (even when attached to OL editions) | Limited specialized APIs (e.g., ISBN/work equivalences); no unrestricted general catalog API established | No open general catalog dump established | Proprietary; systematic extraction and competing-database uses restricted. **Work-scoped ID**. |
| `amazon` | 1,800,687 | Amazon ASIN, often ISBN-10 for books | Amazon Creators API; authenticated and eligibility/affiliate requirements | No openly reusable catalog dump | Proprietary affiliate content rules, including short permitted caching for most product content; retain identifiers separately from licensed metadata. |
| `better_world_books` | 1,025,280 | Better World Books seller / ISBN-related catalog reference | Public product pages; no general public bibliographic API verified | No public complete licensed dump verified | No open general metadata-reuse license identified. Some supplied descriptions may originate with third parties. |
| `doi` | 178,808 | Digital Object Identifier (DOI); identifies a registered scholarly/digital object, not necessarily a retail edition | Crossref REST; DataCite REST; DOI registry resolution | Crossref public metadata files and DataCite public dumps | Basic citation metadata generally available for reuse (many CC0 datasets); **individual fields** such as abstracts may be copyrighted. Determine registration agency. |
| `dnb` | 96,584 | Deutsche Nationalbibliothek (German National Library) bibliographic identifiers | SRU, OAI-PMH, linked-data interfaces | Open MARC/XML/RDF data distributions | DNB open bibliographic metadata described as **CC0**; verify dataset-specific notices. |
| `overdrive` | 76,208 | OverDrive ebook/audiobook catalog entries | Approved developer/library partner APIs | Collection-specific APIs; no unrestricted global catalog dump | Proprietary; license and application-purpose restrictions. Useful for live library availability. |
| `bnp` | 70,120 | Biblioteca Nacional de Portugal bibliographic identifiers | Catalog/search and linked-data interfaces | Open catalog data published in JSON, RDF, XML, CSV | Portuguese national catalog datasets described as **CC0**; check selected distribution metadata. |
| `wikidata` | 45,236 | Wikidata entities (can describe work, edition, author, etc.) | REST/JSON entity access and SPARQL | Full JSON/RDF dumps | **CC0**. Validate entity type before mapping to an edition. |
| `google` | 17,556 | Google Books volume identifiers | Google Books Volumes API | No official complete public volume dump | Google API terms restrict creating permanent databases from returned API content without authorization. Treat as live enrichment / outbound reference. |
| `issn` | 14,396 | International Standard Serial Number; identifies serials/continuing resources | ISSN Portal and restricted/subscription APIs; partial free discovery | Full ISSN Register under subscription; ROAD open subset | Full ISSN register is licensed; not a generally open bulk source. **Serial-level** identifier. |
| `open_alex` | 12,661 | OpenAlex scholarly work records | REST API | Full public S3 snapshot | **CC0** core dataset; useful for scholarly works, not necessarily publisher editions. |
| `bookbrainz` | 11,112 | BookBrainz author/work/edition/edition-group identifiers | REST API | Weekly database dumps | **CC0 core data**; other public data may be CC BY-SA. Track dataset/field provenance. |
| `depósito_legal` | 8,429 | Spanish *depósito legal* (legal deposit) numbers associated with Spanish catalog records | Biblioteca Nacional de España (BNE) catalogs / search interfaces | BNE datasets, MARC/XML, OAI-PMH and related harvesting | BNE open catalog metadata described as **CC0**; note that legal deposit number itself is not a universal edition identifier. |
| `storygraph` | 5,887 | StoryGraph book catalog identifiers | No public developer API verified | No public full catalog dump | Proprietary; no general open metadata-reuse license found. Cross-reference/link only. |
| `bnf` | 5,516 | Bibliothèque nationale de France bibliographic/authority record IDs | BnF SRU and linked-data access | data.bnf.fr RDF dumps | French **Licence Ouverte / Open Licence**; preserve attribution/source and access/update date. |
| `project_gutenberg` | 2,616 | Project Gutenberg ebook/catalog records | Per-item RDF/catalog pages; third-party Gutendex API | Complete RDF/XML catalog export | Catalog metadata is openly distributed; ebook contents have their own copyright and Gutenberg trademark/redistribution rules. **Digital manifestation**, not always a print edition. |
| `amazon.co.uk_asin` | 1,683 | Amazon UK marketplace ASIN | Amazon Creators API, UK marketplace | No open dump | Amazon affiliate/Creators API restrictions; not an independent source for freely persisted product metadata. |
| `isfdb` | 1,523 | Internet Speculative Fiction Database publication/title references | Website and some limited ISBN/XML lookups | Published database backups | Research identified **CC BY 4.0** for the database; verify exact backup license and attribution requirements. Especially rich sci-fi/fantasy bibliography. |
| `amazon.de_asin` | 1,473 | Amazon German marketplace ASIN | Amazon Creators API, German marketplace | No open dump | Same Amazon restrictions; preserve marketplace context. |
| `hathi_trust` | 1,460 | HathiTrust digitized item / bibliographic identifiers | Bibliographic API; catalog and item endpoints | HathiFiles and OAI-PMH / reduced metadata harvesting | Availability and reuse depend on the particular metadata and contributing institutions. **Do not assume unrestricted redistribution**. Digital copy access is separate. |
| `librivox` | 1,192 | LibriVox public-domain audio recordings / catalog records | Official JSON/XML API | Harvestable with paginated API; no single official catalog dump verified | Recordings are public domain; confirm metadata-specific terms if redistributing catalog descriptions. **Audiobook manifestation**. |

## Practical priority for Booksite

1. **Open bibliographic identity:** Wikidata and BookBrainz. Import their bulk data where feasible and treat external IDs as independently sourced identity assertions.
2. **National library bibliography:** DNB, BnF, BNP, BNE. These offer rich publication metadata, useful authority relationships, and relatively clear open-data terms; support attribution where required.
3. **Specialist bibliography:** ISFDB for science-fiction/fantasy titles, publication histories, series, and related works. Preserve the attribution required by its published license.
4. **Academic/research corpus:** Crossref, DataCite, and OpenAlex for DOIs and scholarly works. Their entities do not always map one-to-one to consumer book editions.
5. **Digital availability:** Project Gutenberg, LibriVox, HathiTrust, and (subject to contracts) OverDrive. Treat an online text, scan, recording, and print edition as distinct manifestations/resources.
6. **Link/match only by default:** Goodreads, LibraryThing, Amazon marketplaces, Better World Books, Google Books, StoryGraph. Preserve IDs and source links; avoid importing proprietary fields permanently without explicit terms that allow it.
7. **ISSN:** Special-case serials/continuing resources rather than treating them as book editions.

## Important modeling implications

### Identifier scope matters

An identifier present in an Open Library **edition** JSON object is **not necessarily edition-scoped** in the originating database:

- `librarything` generally identifies a **work**.
- `wikidata` can point to a **work, edition, author, or another entity type**.
- `doi` and `open_alex` may identify **scholarly works/articles/chapters**, not commercial print editions.
- `issn` identifies a **serial/continuing resource**.
- `project_gutenberg`, `hathi_trust`, and `librivox` can refer to **digital texts, scans, or audio items**.
- Amazon ASINs are **marketplace product identifiers**; some coincide with ISBN-10 but should not be assumed to do so.

Consider recording identifiers with a structure such as:

```text
external_identifier
  provider          # e.g. "librarything", "wikidata", "dnb"
  namespace         # optional marketplace / specific subservice
  value             # identifier as string, preserving zeros and punctuation
  entity_scope      # author | work | edition | publication | serial | digital_item | unknown
  source_record_id  # optional provenance assertion that supplied this identifier
  fetched_at        # optional
  rights_profile    # optional provider/dataset terms version
```

Do not impose global uniqueness on `value`; uniqueness is at least provider-scoped, and may require namespace/entity type. A single external identifier can also appear on multiple Open Library editions.

### Licenses apply to **retrieved data**, not just identifiers

Retaining a public-facing cross-reference is not the same as copying a provider's titles, descriptions, cover images, reviews, or full record payload into the permanent catalog. Keep provider attribution and rights metadata separate from the merged fields, and preserve editorial overrides independently of source refreshes.

### Bulk does not mean a one-click file

Some providers publish full periodic snapshots; others offer paginated APIs, OAI-PMH harvesting, linked-data dumps, or subscription-only feeds. Record which access mechanism you actually use, the snapshot date, and the exact source license.

## Documentation and starting points

These links provide source entry points and were identified in the preceding investigation. They are not substitutes for checking terms immediately before production use.

| Provider | Reference links |
|---|---|
| Open Library identifier definitions | [Edition identifier config](https://openlibrary.org/config/edition) |
| Goodreads | [Goodreads](https://www.goodreads.com/) |
| LibraryThing | [LibraryThing](https://www.librarything.com/) |
| Amazon | [Creators API documentation](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/introduction) |
| Better World Books | [Better World Books](https://www.betterworldbooks.com/) |
| Crossref | [REST API](https://api.crossref.org/) · [Documentation](https://www.crossref.org/documentation/retrieve-metadata/rest-api/) |
| DataCite | [REST API](https://api.datacite.org/) · [Docs](https://support.datacite.org/docs/api) |
| DNB | [Open data downloads](https://data.dnb.de/opendata/) |
| OverDrive | [Developer portal](https://developer.overdrive.com/) |
| BNP | [Open catalog dataset](https://dados.gov.pt/pt/datasets/catalogo-bnp/) |
| Wikidata | [Entity API example](https://www.wikidata.org/wiki/Special:EntityData/Q892.json) · [Dumps](https://www.wikidata.org/wiki/Wikidata:Database_download) |
| Google Books | [API overview](https://developers.google.com/books) · [Books API terms](https://developers.google.com/books/terms) · [General API terms](https://developers.google.com/terms) |
| ISSN | [ISSN Portal](https://portal.issn.org/) · [ROAD](https://road.issn.org/) |
| OpenAlex | [API docs](https://docs.openalex.org/) · [Snapshot docs](https://docs.openalex.org/download-all-data/openalex-snapshot) |
| BookBrainz | [API docs](https://api.bookbrainz.org/1/docs/) · [BookBrainz](https://bookbrainz.org/) |
| Spanish National Library / legal deposit | [BNE bibliographic metadata](https://www.bne.es/en/node/7606) |
| StoryGraph | [StoryGraph](https://app.thestorygraph.com/) |
| BnF | [data.bnf.fr dumps](https://api.bnf.fr/fr/dumps-de-databnffr) |
| Project Gutenberg | [Machine-readable catalog](https://www.gutenberg.org/ebooks/offline_catalogs.html) · [Gutendex (third party)](https://gutendex.com/) |
| ISFDB | [ISFDB](https://www.isfdb.org/) |
| HathiTrust | [Data and APIs](https://www.hathitrust.org/) |
| LibriVox | [Official catalog API](https://librivox.org/api/feed/audiobooks/?format=json) |

## Questions to resolve before ingestion

- Verify the **specific dataset license** and required attribution text/version for each selected download, especially ISFDB, BnF, HathiTrust, and national-library subdatasets.
- Confirm whether the provider's API terms permit **permanent caching, derivative works, redistribution, and commercial operation**, not merely API calls.
- Test a sample of each identifier key against its provider to establish **entity type**, canonical URL, redirects, and collision patterns.
- For sources with publisher-contributed fields (descriptions, abstracts, covers), determine **field-level rights** instead of assigning one blanket license to the entire record.
- Establish download/refresh cadence, deletion and redirect handling, and reconciliation against previously applied human overrides.

---

*Prepared from the investigation in this conversation for the Booksite project. Source counts were supplied by the user; API/bulk/license characterizations are research findings that may change.*
