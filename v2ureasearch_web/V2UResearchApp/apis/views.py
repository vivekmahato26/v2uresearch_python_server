from django.http import HttpResponse
from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class SetCookieApiView(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        print(request)
        if request.method == 'POST':
            if 'region' in request.COOKIES:
                value = request.COOKIES['region']
                response = Response('Works')
                return response
            else:
                response = Response('Does Not Works')
                response.set_cookie('region', '')
                return response
