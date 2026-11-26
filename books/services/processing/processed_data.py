from ninja import Schema


class ProcessedWorkData(Schema):
    external_id: str = ""
    revision: int = ""

    title: str = ""
    author_id: str = ""
    description: str = ""
    year_first_published: int = ""
    language: str = ""


class ProcessedAuthorData(Schema):
    external_id: str = ""
    revision: int = ""

    name: str = ""
    given_name: str = ""
    family_name: str = ""
    bio: str = ""
    birthday: str = ""
    deathday: str = ""
    names: list[str] = []
    nationality: list[str] = []
    language: list[str] = []
    identifiers: dict = {}


class ProcessedEditionData(Schema):
    external_id: str = ""
    revision: int = ""

    title: str = ""
    description: str = ""
    translator: str = ""
    introduction_by: str = ""
    year_published: int = ""
    publisher: str = ""
    pages: int = 0
    work: str = ""
    language: str = ""
    identifiers: dict = {}
    subtitle: str = ""
