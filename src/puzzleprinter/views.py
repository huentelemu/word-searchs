import zipfile
from io import BytesIO

from django.core.files.base import ContentFile
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.conf import settings

from .forms import WordsListForm
from .models import WordsList, Sopa, SopaMedia

from .utils import WordSearch


def index(request):
    return render(request, 'puzzleprinter/index.html')


def upload_list_words(request):
    if request.method == 'POST':
        form = WordsListForm(request.POST, request.FILES)
        if form.is_valid():
            word_list = form.save()
            list_of_lists = word_list.deliver_list_of_lists()
            for list_of_words in list_of_lists:
                soup = Sopa(list_of_words="\n".join(list_of_words),
                            words_list_object=word_list,
                            soup='deprecated')
                soup.save()

            return HttpResponseRedirect(reverse('results', args=(word_list.id,)))
    else:
        form = WordsListForm()
    return render(request, 'puzzleprinter/upload_list_words.html', {
        'form': form,
    })


def results(request, pk):
    words_list = WordsList.objects.get(pk=pk)
    if request.method == 'POST':
        response = HttpResponse(content_type='application/zip')
        zip_file = zipfile.ZipFile(response, 'w')
        for soup in words_list.sopa_set.all():
            zip_file.write(f'{settings.MEDIA_ROOT}/' + soup.media.first().soup_image.name, str(soup.pk) + '-sopa.png')
            zip_file.write(f'{settings.MEDIA_ROOT}/' + soup.media.first().solution_image.name, str(soup.pk) + '-solucion.png')
            zip_file.write(f'{settings.MEDIA_ROOT}/' + soup.media.first().list_file.name, str(soup.pk) + '-lista.txt')

        zip_file.close()
        response['Content-Disposition'] = 'attachment; filename={}'.format('/vol/web/media/zipfile.zip')
        return response
    else:

        # Delete all previous media
        for sopamedia in SopaMedia.objects.all():
            sopamedia.delete()

        # Prepare Sopa media
        height = words_list.height
        width = words_list.width
        n_orientations = words_list.n_orientations
        font_size = words_list.font_size
        square_size = words_list.square_size
        for soup in words_list.sopa_set.all():
            ws = WordSearch(original_words=soup.list_of_words.split("\n"),
                            shape=(height, width),
                            n_orientations=n_orientations,
                            font_size=font_size,
                            square_size=square_size)

            soup_image = ws.draw_soup()
            soup_image_io = BytesIO()
            soup_image.save(soup_image_io, format='png')

            solution_image = ws.draw_solution()
            solution_image_io = BytesIO()
            solution_image.save(solution_image_io, format='png')

            soup_media = SopaMedia(soup=soup)

            soup_media.soup_image.save(str(soup.pk) + '-soup.png', ContentFile(soup_image_io.getvalue()))
            soup_media.solution_image.save(str(soup.pk) + '-solution.png', ContentFile(solution_image_io.getvalue()))
            soup_media.list_file.save(str(soup.pk) + '-list.txt', ContentFile(soup.list_of_words))

            soup_media.save()

            soup_image_io.close()
            solution_image_io.close()

        return render(request, 'puzzleprinter/results.html', {
            'soups': words_list.sopa_set.all(),
        })
