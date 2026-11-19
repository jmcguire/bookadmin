from django.db import models

# various normalized information about books and authors


class EditionISBN(models.Model):
    edition = models.ForeignKey("books.Edition", on_delete=models.PROTECT)
    isbn13 = models.CharField(max_length=13)


class Cover(models.Model):
    cover = models.BigAutoField(primary_key=True)
    cover_filename = models.CharField(max_length=200)
    edition_id = models.ForeignKey("books.Edition", on_delete=models.PROTECT)


class Nationality(models.Model):
    nationality_code = models.CharField(max_length=3, primary_key=True)
    nation = models.CharField(max_length=200)


class Language(models.Model):
    language_code = models.CharField(max_length=2, primary_key=True)
    language_name = models.CharField(max_length=200)


class Publisher(models.Model):
    publisher = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    nationality = models.ForeignKey("books.Nationality", on_delete=models.PROTECT)


# I might want to change all of these to tags like "genre:scifi" and "movement:existentalism"?
# any searching can be on a separate searching database? or a periodically updated and denormalized tagging table?


# for a book. e.g. lit fic, fantasy, gonzo, i dunno just whatever
# class Genre(models.Model):
#    genre = models.BigAutoField(primary_key=True)
#    genre_name = models.CharField(max_length=200)


# class WorkXGenre(models.Model):
#    work = models.ForeignKey("Work", on_delete=models.PROTECT)
#    genre = models.ForeignKey("Genre", on_delete=models.PROTECT)


# for authors. e.g. modernism, conservative, existentialism. i dunno, another thing to think about
# class Movement(models.Model):
#    movement = models.BigAutoField(primary_key=True)
#    movement_name = models.CharField(max_length=200)


# class AuthorXMovement(models.Model):
#    author = models.ForeignKey("Author", on_delete=models.PROTECT)
#    movement = models.ForeignKey("Movement", on_delete=models.PROTECT)
