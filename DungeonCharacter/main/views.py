from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets


def home(request):
    return render(request, 'main/home.html')
