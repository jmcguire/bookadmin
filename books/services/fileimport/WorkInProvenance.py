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
