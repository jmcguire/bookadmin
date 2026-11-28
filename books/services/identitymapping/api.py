from ninja import NinjaAPI
from ninja.errors import HttpError

from books.models import ProcessedAuthor

from .author_controller import AuthorController
from .results import IdentifyResults

identitymapping_api = NinjaAPI()


@identitymapping_api.put("authors", response=IdentifyResults)
def map_authors(request):
    if ProcessedAuthor.objects.count() == 0:
        raise HttpError(404, "no author processed records exist")

    author_controller = AuthorController()
    return author_controller.identify_all()
