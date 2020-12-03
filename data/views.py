from django.shortcuts import render
from django.http import HttpResponse

def data(request):
    return render(request, 'data/data.html', {'title': 'Data of the World'})

def data_details(request):
    return HttpResponse('<h1>Data-Details</h1>')

# Create your views here.
