from django.db import models

DIMENSION_CHOICES = [(i, i) for i in range(15, 36)]


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    pdf = models.FileField(upload_to='books/pdfs/')
    cover = models.ImageField(upload_to='books/covers/', null=True, blank=True)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.pdf.delete()
        self.cover.delete()
        super().delete(*args, **kwargs)


class WordsList(models.Model):
    words_file = models.FileField(upload_to='sopas/lista/')
    width = models.IntegerField(default=25, choices=DIMENSION_CHOICES)
    height = models.IntegerField(default=25, choices=DIMENSION_CHOICES)
