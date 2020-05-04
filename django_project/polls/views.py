from django.http import HttpResponse
from django.utils import timezone


def index(request):
    return HttpResponse('Hello world. Polls index. '+str(timezone.now()))