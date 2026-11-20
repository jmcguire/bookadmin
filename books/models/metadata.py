from django.db import models

# various normalized information about books and authors


class EditionISBN(models.Model):
    edition = models.ForeignKey("books.Edition", on_delete=models.PROTECT)
    isbn13 = models.CharField(max_length=13)


class Cover(models.Model):
    cover = models.BigAutoField(primary_key=True)
    cover_filename = models.CharField(max_length=200)  # ImageField?
    edition_id = models.ForeignKey("books.Edition", on_delete=models.PROTECT)


# replace with a Field.choices
class Nationality(models.Model):
    nationality_code = models.CharField(max_length=3, primary_key=True)
    nation = models.CharField(max_length=200)


# replace with a Field.choices
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
#    genre_name = models.CharField(max_length=200)

# for authors. e.g. modernism, conservative, existentialism. i dunno, another thing to think about
# class Movement(models.Model):
#    movement_name = models.CharField(max_length=200)
