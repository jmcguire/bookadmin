from django.conf import settings
from django.shortcuts import get_list_or_404, get_object_or_404
from ninja import NinjaAPI
from ninja.errors import HttpError

from ...models import ProvenanceImport
from .file_importer import FileImporter
from .file_importer_open_library import FileImporterOpenLibrary
from .results import FileImportResults, FileList, ImportsList, ProvenanceImportOut

import_api = NinjaAPI()


@import_api.get("", response=ImportsList)
def get_imports(request):
    imports = get_list_or_404(ProvenanceImport)
    return ImportsList(imports=imports)


@import_api.get("import/{import_id}", response=ProvenanceImportOut)
def get_import(request, import_id):
    imp = get_object_or_404(ProvenanceImport, import_id)
    return imp


@import_api.get("files", response=FileList)
def get_files(request):
    downloads = settings.DOWNLOAD_DIR

    imp_hash = {}
    for imp in ProvenanceImport.objects.all():
        imp_hash[imp.filename] = imp

    files = []
    for file in downloads.glob("*.gz"):
        files.append({"file": file.name, "import": imp_hash.get(file, None)})

    if not files:
        raise HttpError(404, "no files found")

    return FileList(files=files)


@import_api.post("files/{filename}/import", response=FileImportResults)
def import_file(request, filename):
    fileimporter: FileImporter = FileImporterOpenLibrary(filename)

    if not fileimporter.check_file():
        raise HttpError(400, "invalid file")

    if not fileimporter.unzip_file():
        raise HttpError(400, "file cannot be unzipped")

    if not fileimporter.load_file():
        raise HttpError(400, "import failed")

    return FileImportResults(
        import_id=fileimporter.imp.id,
        file_stats=fileimporter.file_stats(),
        import_stats=fileimporter.imp.stats(),
    )
