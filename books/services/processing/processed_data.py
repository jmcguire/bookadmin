class ProcessedWorkData:
    def __init__(self):
        self.external_id = ""
        self.revision = ""

        self.title = ""
        self.author_id = ""
        self.description = ""
        self.year_first_published = ""
        self.language = ""


class ProcessedAuthorData:
    def __init__(self):
        self.external_id = ""
        self.revision = ""

        self.bio = ""
        self.name = ""
        self.given_name = ""
        self.family_name = ""
        self.bio = ""
        self.birthday = ""
        self.deathday = ""
        self.names = []
        self.nationality = []
        self.language = []
        self.identifiers = {}


class ProcessedEditionData:
    def __init__(self):
        self.external_id = ""
        self.revision = ""

        self.title = ""
        self.description = ""
        self.translator = ""
        self.introduction_by = ""
        self.year_published = ""
        self.publisher = ""
        self.pages: int = 0
        self.work = ""
        self.language = ""
        self.identifiers = []
        self.subtitle = ""
        self.publisher = ""
