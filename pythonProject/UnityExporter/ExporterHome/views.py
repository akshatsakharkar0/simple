from django.shortcuts import render

def home(request):
    return render(request, 'ExporterHome/home.html')

