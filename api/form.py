from django import forms

class CityForm(forms.Form):
    city1 = forms.CharField(max_length=100)
    city2 = forms.CharField(max_length=100)

class SearchForm(forms.Form):
    city = forms.CharField(max_length=100)