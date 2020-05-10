from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.template import loader


def index(request):
    return render(request, 'puzzleprinter/index.html')