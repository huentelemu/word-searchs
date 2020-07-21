from django.db import models

from .utils import read_words_file

DIMENSION_CHOICES = [(i, i) for i in range(8, 36)]
N_ORIENTATION_CHOICES = [(i, i) for i in range(1, 9)]


class WordsList(models.Model):
    words_file = models.FileField(upload_to='sopas/lista/')
    width = models.IntegerField(default=17, choices=DIMENSION_CHOICES)
    height = models.IntegerField(default=29, choices=DIMENSION_CHOICES)
    n_orientations = models.IntegerField(default=8, choices=N_ORIENTATION_CHOICES)
    font_size = models.IntegerField(default=90)
    square_size = models.IntegerField(default=80)

    created_at = models.DateTimeField(auto_now_add=True)

    def deliver_list_of_lists(self):
        file_path = '/vol/web/media/' + self.words_file.name
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