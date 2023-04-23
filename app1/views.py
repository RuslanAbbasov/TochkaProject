from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponse
import re


# Create your views here.


def index(request):
    host = request.META["HTTP_HOST"]  # получаем адрес сервера
    user_agent = request.META["HTTP_USER_AGENT"]  # получаем данные бразера
    path = request.path  # получаем запрошенный путь
    header = request.headers

    regex = re.compile('^HTTP_')
    dict((regex.sub('', header), value) for (header, value)
         in request.META.items() if header.startswith('HTTP_'))

    return HttpResponse(f"""
        <p>Host: {host}</p>
        <p>Path: {path}</p>
        <p>User-agent: {user_agent}</p>
        <p>Headers: {regex}</p>
    """)
