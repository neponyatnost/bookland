from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    published_year = models.IntegerField()
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
        # ordering = ["-date_added"]


    def __str__(self):
        return self.title


