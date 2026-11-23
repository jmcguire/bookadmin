from django.conf import settings
from django.shortcuts import get_list_or_404, get_object_or_404
from ninja import NinjaAPI
from ninja.errors import HttpError

from ...models import ProvenanceImport
from .FileImporter import FileImporter
from .FileImporterOpenLibrary import FileImporterOpenLibrary

imports_api = NinjaAPI()


@imports_api.get("")
def get_imports(request):
    imports = get_list_or_404(ProvenanceImport)
    return {"imports": imports}


@imports_api.get("import/{import_id}")
def get_import(request, import_id):
    imp = get_object_or_404(ProvenanceImport, import_id)
    return {"import": imp, "stats": imp.stats()}


@imports_api.get("files")
def get_files(request):
    downloads = settings.DOWNLOAD_DIR

    imp_hash = {}
    for imp in ProvenanceImport.objects.all():
        imp_hash[imp.filename] = imp

    files = []
    for file in downloads.iterdir():
        files.append({"file": file.name, "import": imp_hash.get(file, None)})

    if not files:
        raise HttpError(404, "no files found")

    return {"files": files}


@imports_api.post("files/{filename}/import")
def import_file(request, filename):
    fileimporter: FileImporter = FileImporterOpenLibrary(filename)

    if not fileimporter.check_file():
        raise HttpError(400, "invalid file")

    if not fileimporter.unzip_file():
        raise HttpError(400, "file cannot be unzipped")

    if not fileimporter.load_file():
        raise HttpError(400, "import failed")

    return {
        "import_id": fileimporter.imp.id,
        "file_stats": fileimporter.file_stats().__dict__,
        "import_stats": fileimporter.imp.stats(),
    }
