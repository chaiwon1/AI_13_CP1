from django.shortcuts import render
from django.conf import settings

def index(request):
    return render(request, 'main/index.html')

def demand(request):
    return render(request, 'main/demand.html')

def helmet(request):
    return render(request, 'main/helmet.html')

def parking(request):
    return render(request, 'main/parking.html')