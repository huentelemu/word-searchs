from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView

from .forms import BookForm, WordsListForm
from .models import Book, WordsList

# Create your views here.
from django.template import loader

from .utils import read_words_file, WordSearch


def index(request):
    return render(request, 'puzzleprinter/index.html')


def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES["document"]
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
    return render(request, 'puzzleprinter/upload.html', context)


def book_list(request):
    books = Book.objects.all()
    return render(request, 'puzzleprinter/book_list.html', {
        'books': books,
    })


def upload_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'puzzleprinter/upload_book.html', {
        'form': form,
    })


def upload_list_words(request):
    if request.method == 'POST':
        form = WordsListForm(request.POST, request.FILES)
        if form.is_valid():
            word_list = form.save()
            print('asd', word_list.id)
            # return redirect('results')
            return HttpResponseRedirect(reverse('results', args=(word_list.id,)))
    else:
        form = WordsListForm()
    return render(request, 'puzzleprinter/upload_list_words.html', {
        'form': form,
    })


def results(request, pk):
    words_list = WordsList.objects.get(pk=pk)
    list_of_lists = words_list.deliver_list_of_lists()
    soups = []
    for soup_list in list_of_lists:
        soup = WordSearch(original_words=soup_list, shape=(29, 17))
        print(soup.string_representation)
        soups.append(soup)
    return render(request, 'puzzleprinter/results.html', {
        'soups': soups,
    })


def delete_book(request, pk):
    if request.method == 'POST':
        book = Book.objects.get(pk=pk)
        book.delete()
    return redirect('book_list')


class BookListView(ListView):
    model = Book
    template_name = 'class_book_list.html'
    context_object_name = 'books'


class UploadBookView(CreateView):
    model = Book
    fields = BookForm
    success_url = reverse_lazy('class_book_list')
    template_name = 'upload_book.html'
