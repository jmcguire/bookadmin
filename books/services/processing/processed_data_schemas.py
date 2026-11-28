from ninja import Schema


class ProcessedCatalogType(Schema):
    external_id: str = ""
    revision: int = 0


class ProcessedWorkData(ProcessedCatalogType):
    title: str = ""
    author_id: str = ""
    description: str = ""
    year_first_published: int | None = None
    language: str = ""


class ProcessedAuthorData(ProcessedCatalogType):
    name: str = ""
    given_name: str = ""
    family_name: str = ""
    bio: str = ""
    birthday: str = ""
    birthyear: str = ""
    century_active: str = ""
    deathday: str = ""
    names: list[str] = []
    nationality: list[str] = []
    language: list[str] = []
    identifiers: dict = {}


class ProcessedEditionData(ProcessedCatalogType):
    title: str = ""
    description: str = ""
    translator: str = ""
    introduction_by: str = ""
    year_published: int | None = None
    publisher: str = ""
    pages: int | None = None
    work: str = ""
    language: str = ""
    identifiers: dict = {}
    subtitle: str = ""
