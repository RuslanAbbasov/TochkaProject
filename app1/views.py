from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponse
import re


# Create your views here.


def homePage(request):
    return render(request, 'homePage.html')
