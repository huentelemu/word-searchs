from django.db import models

from .utils import read_words_file

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
    width = models.IntegerField(default=17, choices=DIMENSION_CHOICES)
    height = models.IntegerField(default=29, choices=DIMENSION_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)

    def deliver_list_of_lists(self):
        file_path = 'media/' + self.words_file.name
        return read_words_file(file_path)


class Sopa(models.Model):
    words_list_object = models.ForeignKey(WordsList, on_delete=models.CASCADE)
    list_of_words = models.TextField()
    soup = models.TextField(null=True)


class SopaMedia(models.Model):
    soup_image = models.ImageField(upload_to='sopas/', null=True, blank=True)
    solution_image = models.ImageField(upload_to='sopas/', null=True, blank=True)
    list_file = models.FileField(upload_to='sopas/', null=True, blank=True)
    soup = models.ForeignKey(Sopa, on_delete=models.CASCADE, related_name="media")

    def delete(self, *args, **kwargs):
        self.soup_image.delete()
        self.solution_image.delete()
        self.list_file.delete()
        super().delete(*args, **kwargs)
