from django.shortcuts import render, HttpResponse
from .form import CityForm, SearchForm
from django.views.generic import View


from .models import Logs
from django.utils import timezone
from datetime import datetime
import pytz

# Create your views here.
import requests

API_URL = ("http://api.openweathermap.org/data/2.5/weather?"
"q={}&mode=json&units=metric&appid={}")
DEFAULT_TIME = 'Europe/Madrid'
TIME_FMT = '%H:%M:%S %Z%z'

def home(request):
    city1 = False
    city2 = False
    userWeather = []
    if request.user.is_authenticated:
        if request.user.profile.location is not None:
            userWeather = query_api(request.user.profile.location)
    if request.method == 'POST':
        form = CityForm(request.POST)
        
        if form.is_valid():
            city1 = query_api(form['city1'].value())
            city2 = query_api(form['city2'].value())
            l = Logs(city1=form['city1'].value(), city2=form['city2'].value())
            l.save()
            return render(request, 'api/search.html', {'form': form, 'city1': city1, 'city2': city2,
            'sunrise1': get_local_time( city1['sys']['sunrise'] , city1['sys']['country'], city1['name']),
            'sunset1': get_local_time( city1['sys']['sunset'] , city1['sys']['country'], city1['name']),
            'sunrise2': get_local_time( city2['sys']['sunrise'] , city2['sys']['country'], city2['name']),
            'sunset2': get_local_time( city2['sys']['sunset'] , city2['sys']['country'], city2['name']),
            'userWeather': userWeather
            })

    else:
        form = CityForm()

    return render(request, 'api/search.html', {'form': form, 'userWeather': userWeather})
    
class HistoryView(View):
    form = SearchForm
    template_name = 'api/history.html'
    def get(self, request):
        form =self.form(None)
        return render(request, self.template_name, { 'form': form })

    def post(self, request):
        form = self.form(request.POST)

        if form.is_valid():
            pass

        return render(request, self.template_name,{'form': form})

def query_api(city):
    try:
        data = requests.get(API_URL.format(city, "44eeb6fe82501cf0500f489b7d0d44db")).json()
    except Exception as exc:
        print(exc)
        data = None
    return data

def get_local_time(utstamp, country, city):
    utc_dt = datetime.utcfromtimestamp(int(utstamp)).replace(tzinfo=pytz.utc)

    timezones = pytz.country_timezones.get(country.upper(), [])
    closest_timezone = [tz for tz in timezones if city.lower() in tz.lower()]

    if closest_timezone:
        tz = closest_timezone[0]  # tz + city
    elif timezones:
        tz = timezones[0]  # just tz
    else:
        tz = DEFAULT_TIME  # emea

    loc_tz = pytz.timezone(tz)
    dt = utc_dt.astimezone(loc_tz)
    return dt.strftime(TIME_FMT)