from django.shortcuts import render, HttpResponse
from django.template import loader
from django.views.generic.edit import CreateView
from .form import CityForm

from pprint import pprint as pp
# Create your views here.
import requests

API_URL = ("http://api.openweathermap.org/data/2.5/weather?"
"q={}&mode=json&units=metric&appid={}")

def home(request):
    city1 = False
    city2 = False
    if request.method == 'POST':
        form = CityForm(request.POST)
        
        if form.is_valid():
            city1 = query_api(form['city1'].value())
            city2 = query_api(form['city2'].value())
            print(city1['weather'][0]['description'])
            return render(request, 'api/search.html', {'form': form, 'city1': city1, 'city2': city2})

    else:
        form = CityForm()

    return render(request, 'api/search.html', {'form': form})
    

def query_api(city):
    try:
        data = requests.get(API_URL.format(city, "44eeb6fe82501cf0500f489b7d0d44db")).json()
    except Exception as exc:
        print(exc)
        data = None
    return data