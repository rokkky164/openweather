from datetime import datetime
from django.db import models
from jsonfield import JSONField
from collections import OrderedDict

Timechoices = (
	('Minutely', 'Minutely'),
	('Hourly', 'Hourly'),
	('Daily', 'Daily'),
)

class Weather(models.Model):
	latitude = models.FloatField(verbose_name="Latitude")
	longitude = models.FloatField(verbose_name="Longitude")
	weather_data = JSONField(default=list)
	time_frequency = models.CharField(max_length=50, null=True, choices=Timechoices)
	city = models.CharField(max_length=255, verbose_name="City")
	time_stamp = models.DateTimeField(verbose_name='TimeStamp', auto_now_add=True)

	def __str_(self):
		return self.city + ' ' + datetime.strftime(self.time_stamp, "%d-%b-%y")
