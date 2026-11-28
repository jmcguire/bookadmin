from django.db.models import Q
from django.db.models.functions import Length

from books.models import (
    CatalogAuthor,
    IdentityMappingAuthorProcessedToCatalog,
    ProcessedAuthor,
)

from .results import IdentifyResult, IdentifyResults


class AuthorController:
    def __init__(self):
        pass

    def identify_all(self) -> IdentifyResults:
        results = IdentifyResults()

        for process_author in ProcessedAuthor.objects.all():
            result = self.identify_single(process_author)
            field = result.name
            setattr(results, field, getattr(results, field) + 1)

        return results

    def identify_single(self, process_record: ProcessedAuthor) -> IdentifyResult:
        identitymap = IdentityMappingAuthorProcessedToCatalog.objects.filter(
            processed_author=process_record
        ).first()
        if identitymap and identitymap.manual_override:
            return IdentifyResult.existing_manual_override

        # convenient variables
        family_name = process_record.data["family_name"].lower()
        given_name = process_record.data["given_name"].lower()
        birthday = process_record.data["birthday"] if process_record.data["birthday"] else None
        birthyear = process_record.data["birthyear"]
        century_active = process_record.data["century_active"]

        possible_matches = CatalogAuthor.objects.filter(
            Q(family_name__iexact=family_name)
            & (
                (Q(birthday=birthday) | Q(birthyear=birthyear) | Q(birthyear=century_active))
                | (
                    Q(birthday__isnull=True)
                    & Q(birthyear__isnull=True)
                    & Q(century_active__isnull=True)
                )
            )
        )
        if possible_matches.count():
            # almost certainly a match
            # get all objects, and search for the one that matches the first name the best
            best_choice = None
            for author in possible_matches.order_by(Length("given_name")):
                if given_name == author.given_name.lower():
                    if identitymap:
                        identitymap.catalog_author = author
                        identitymap.save()
                        return IdentifyResult.existing_to_existing
                    else:
                        IdentityMappingAuthorProcessedToCatalog.objects.create(
                            processed_author=process_record,
                            catalog_author=author,
                        )
                        return IdentifyResult.new_to_existing
                elif (
                    author.given_name
                    and given_name[0:1] == author.given_name.lower()[0:1]
                    and not best_choice
                ):
                    # it's a good choice so far
                    best_choice = author

            if best_choice:
                # we didn't find an exact first name match, but we did find an partial match
                if identitymap:
                    identitymap.catalog_author = best_choice
                    identitymap.save()
                    return IdentifyResult.existing_to_existing
                else:
                    IdentityMappingAuthorProcessedToCatalog.objects.create(
                        processed_author=process_record,
                        catalog_author=best_choice,
                    )
                    return IdentifyResult.new_to_existing

        # otherwise, make a new record

        if identitymap:
            # just keep the existing mapping
            return IdentifyResult.existing_to_existing
        else:
            catalog_author = CatalogAuthor.objects.create(
                family_name=process_record.data["family_name"],
                given_name=process_record.data["given_name"],
                birthday=process_record.data["birthday"]
                if process_record.data["birthday"]
                else None,
                birthyear=process_record.data["birthyear"],
                century_active=process_record.data["century_active"],
            )

            IdentityMappingAuthorProcessedToCatalog.objects.create(
                processed_author=process_record,
                catalog_author=catalog_author,
            )
            return IdentifyResult.new_to_new
