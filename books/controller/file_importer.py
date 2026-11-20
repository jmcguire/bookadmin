class FileImporter:
    def __init__(self, file_id):
        self.file_id = file_id

    def check_file(self):
        self.file_name = ""
        return True

    def unzip_file(self):
        self.contents = []
        return True

    def load_file(self):
        self.imp = "import object"
        return True

    def file_stats(self):
        return {
            "size": 0,
            "lines": 0,
        }
