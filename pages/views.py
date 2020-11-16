from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render


def index(request: WSGIRequest):
    return render(request, 'pages/index.html', {
        'active_menu': 'index',
    })


def presentation(request: WSGIRequest):
    return render(request, 'pages/presentation.html', {
        'active_menu': 'presentation',
    })


def mentions(request: WSGIRequest):
    return render(request, 'pages/mentions-legales.html')
