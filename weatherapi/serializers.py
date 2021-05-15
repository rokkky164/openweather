import logging

from django.apps import apps
from django.conf import settings
from rest_framework_json_api import serializers
from .models import Weather

class WeatherSerializer(serializers.ModelSerializer):
    """Related to Weather"""
    class Meta:
    	model = Weather
    	fields = '__all__'
