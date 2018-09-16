from django.shortcuts import render, HttpResponse
from .form import CityForm, SearchForm
from django.views.generic import View

from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
import time
from background_task import background
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import components

from .models import Logs
from django.utils import timezone
from datetime import datetime, timedelta
import pytz

# Create your views here.
import requests

API_URL = ("http://api.openweathermap.org/data/2.5/weather?"
"q={}&mode=json&units=metric&appid={}")
FORECAST_URL = ("http://api.openweathermap.org/data/2.5/forecast?"
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
    
def query_forcast(city):
    try:
        data = requests.get(FORECAST_URL.format(city, "44eeb6fe82501cf0500f489b7d0d44db")).json()
    except Exception as exc:
        print(exc)
        data = None
    return data
class HistoryView(View):
    form = SearchForm
    template_name = 'api/history.html'

      
    def get(self, request):
        form =self.form(None)
        return render(request, self.template_name, { 'form': form })

    def post(self, request):
        form = self.form(request.POST)

        if form.is_valid():
            
            forceasts = query_forcast(form['city'].value())
            x = []
            y = []
            for forecast in forceasts['list']:
                x.append(forecast['dt'])
                y.append(forecast['main']['temp'])

            plot = figure(title="simple line example", x_axis_label='time', y_axis_label='temp')
            plot.line(x, y, legend="Temp.", line_width=2)

            script, div = components(plot, CDN)
            return render(request, self.template_name,{'form': form, 'script' : script , 'div' : div })

        return render(request, self.template_name,{'form': form })

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

@background(schedule=timedelta(minutes=1440))
def sendEmails():
    users = User.objects.all()
    apiCalls = {}
    for user in users:
        if(user.profile.location != ''):
            if user.profile.location not in apiCalls:
                apiCalls[user.profile.location] = query_api(user.profile.location)
            
            subject = 'Todays weather'
            message = ' todays weather in ' + user.profile.location + ' is ' + apiCalls[user.profile.location]['weather'][0]['description']
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email,]
            print('sending email ....' + message)
            send_mail( subject, message, email_from, recipient_list )
    return

