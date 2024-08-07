from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from rest_framework.viewsets import ViewSet


def render_homepage(request):
    '''renders the homepage'''
    pass
    # return render(request, "index.html")
        