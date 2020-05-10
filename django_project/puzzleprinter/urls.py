from django.urls import path

from . import views

app_name = 'puzzleprinter'
urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
]
