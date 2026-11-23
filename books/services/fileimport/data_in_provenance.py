class WorkInProvenance:
    def __init__(self):
        self.external_id = ""
        self.revision = ""
        self.data = self.WorkDataInProvenance()

    def __str__(self):
        return f"work {self.external_id}\t{self.revision}\t{self.data}"

    class WorkDataInProvenance:
        def __init__(self):
            self.title = ""
            self.author_id = ""
            self.description = ""
            self.year_first_published = ""
            self.language = ""


class AuthorInProvenance:
    def __init__(self):
        self.external_id = ""
        self.revision = ""
        self.data = self.AuthorDataInProvenance()

    def __str__(self):
        return f"work {self.external_id}\t{self.revision}\t{self.data}"

    class AuthorDataInProvenance:
        def __init__(self):
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


class EditionInProvenance:
    def __init__(self):
        self.external_id = ""
        self.revision = ""
        self.data = self.EditionDataInProvenance()

    def __str__(self):
        return f"work {self.external_id}\t{self.revision}\t{self.data}"

    class EditionDataInProvenance:
        def __init__(self):
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
