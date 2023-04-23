from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponse
# Create your views here.


def index(request):
    host = request.META["HTTP_HOST"]  # получаем адрес сервера
    user_agent = request.META["HTTP_USER_AGENT"]  # получаем данные бразера
    path = request.path  # получаем запрошенный путь
    headers = request.headers
    return HttpResponse(f"""
        <p>Host: {host}</p>
        <p>Path: {path}</p>
        <p>User-agent: {user_agent}</p>
        <p>Headers: {headers}</p>
    """)
