from django.db import models

class Logs(models.Model):
    city1 = models.CharField(max_length=100)
    city2 = models.CharField(max_length=100)
    pub_date = models.DateTimeField('date searched') 