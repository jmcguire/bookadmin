# todo __init__ is to big
# rename to results
# eventually have detailed results: a success file and a failure file, that says precisely what succeeded and what failed and why


class FileImportStats:
    def __init__(self, size, lines, success, failed):
        self.size = size
        self.lines = lines
        self.success = success
        self.failed = failed
