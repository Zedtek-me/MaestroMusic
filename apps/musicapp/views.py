from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.views import View


class HomeView(View):
    '''loads the homepage and renders it'''

    def get(self, request):
        '''first template render'''
        