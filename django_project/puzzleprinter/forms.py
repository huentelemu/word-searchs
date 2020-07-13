from django import forms
from .models import WordsList


class WordsListForm(forms.ModelForm):

    class Meta:
        model = WordsList
        fields = ['words_file', 'width', 'height']
        labels = {
            'words_file': 'Lista de palabras',
            'width': 'Ancho',
            'height': 'Alto',
        }
