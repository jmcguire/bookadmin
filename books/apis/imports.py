from django.conf import settings
from ninja import NinjaAPI

from ..controller import FileImporter
from ..models import ProvenanceImport

imports_api = NinjaAPI()


@imports_api.get("")
def get_imports(request):
    imports = ProvenanceImport.objects.all()
    return {"imports": imports}


@imports_api.get("import/{import_id}")
def get_import(request, import_id):
    imp = ProvenanceImport.objects.get(pk=import_id)
    return {"import": imp, "stats": imp.stats()}


@imports_api.get("files")
def get_files(request):
    downloads = settings.DOWNLOAD_DIR

    imp_hash = {}
    for imp in ProvenanceImport.objects.all():
        imp_hash[imp.filename] = imp

    files = []
    for file in downloads.iterdir():
        files.append({"file": file, "import": imp_hash.get(file, None)})

    return {"files": files}


@imports_api.post("files/{file_id}/import")
def import_file(request, file_id):
    fileimporter = FileImporter(file_id)

    if not fileimporter.check_file():
        pass

    if not fileimporter.unzip_file():
        pass

    fileimporter.load_file()

    return {
        "import_id": fileimporter.imp.id,
        "file_stats": fileimporter.file_stats(),
        "import_stats": fileimporter.imp.stats(),
    }
