from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from mysio.models import *


# Create your views here.
def home(request):
    return render(request, 'sio.html', {})
