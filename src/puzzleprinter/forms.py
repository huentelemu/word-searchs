from django import forms
from .models import WordsList


class WordsListForm(forms.ModelForm):

    class Meta:
        model = WordsList
        fields = ['words_file', 'width', 'height', 'n_orientations', 'font_size', 'square_size', 'encoding']
        labels = {
            'words_file': 'Lista de palabras',
            'width': 'Ancho',
            'height': 'Alto',
            'n_orientations': 'Número de orientaciones',
            'font_size': 'Tamaño de fuente',
            'square_size': 'Tamaño de cuadro',
            'encoding': 'Codificación',
            'fill': 'Rellenar con',
        }
