from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('sopas/', views.upload_list_words, name='upload_list_words'),
    path('sopas/resultados/<int:pk>/', views.results, name='results'),
]
