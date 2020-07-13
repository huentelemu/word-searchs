from django import forms
from .models import WordsList


class WordsListForm(forms.ModelForm):

    class Meta:
        model = WordsList
        fields = ['words_file', 'width', 'height', 'n_orientations']
        labels = {
            'words_file': 'Lista de palabras',
            'width': 'Ancho',
            'height': 'Alto',
            'n_orientations': 'Número de orientaciones',
        }
