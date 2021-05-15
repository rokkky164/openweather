import requests
import json

from django.shortcuts import render
from django.conf import settings
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_json_api import serializers

from .models import Weather
# from .serializers import CitySerializer


CITIES = {
    'Keonjhar': [21.5, 85.5],
    'Mumbai': [19.075, 72.877],
    'Hyderabad' : [17.385, 78.486],
    'Bangalore': [12.97, 77.6],
    'Delhi': [28.7, 77.1],
    'Lucknow': [26.84, 80.95],
    'Pune': [18.52, 73.85],
    'Chennai': [13.08, 80.27],
    'Kolkata': [22.7, 88.4],
    'Bhubaneswar': [20.25, 85.8]
}


class CollectData(APIView):

    @staticmethod
    def get_weather_data(lat, lon):
        try:
            url = "https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={key}".format(
                    lat=lat, lon=lon, key=settings.WEATHER_KEY)
            response = json.loads(requests.get(url).content)
        except (TypeError, AttributeError):
            response = {}
        return response

    def get(self, request):
        for city, coord in CITIES.items():
            lat, lon = coord
            weather_response = self.get_weather_data(lat, lon)
            weather = {
                'city': city,
                'latitude': lat,
                'longitude': lon,
                'weather_data': weather_response.pop('hourly'),
                'time_frequency': 'hourly'
            }
            Weather.objects.create(**weather)
        return Response(data={'Weather object is created for {cities}'.format(cities=", ".join(
            [i for i in CITIES.keys()]))})


class SimilarCitiesView(APIView):

    weather_params = ['temp', 'feels_like', 'pressure', 'humidity', 'dew_point', 'uvi', 'wind_gust',
                      'wind_speed']
    @staticmethod
    def calculate_avg(obj, *args):
        arg = args[0]
        return {arg: sum([i[arg] for i in obj.weather_data])/len(obj.weather_data)}

    def get(self, request):
        city1 = self.request.query_params.get('city1')
        city2 = self.request.query_params.get('city2')
        cities = [i.capitalize() for i in [city1, city2]]
        for city in cities:
            if city not in CITIES.keys():
                raise serializers.ValidationError(
                    '{city} is not valid'.format(city=city) + '\n'
                    'Select city from this list {cities}'.format(cities=", ".join(CITIES.keys()))
                )
        weather_objs = Weather.objects.filter(city__in=cities).order_by('-time_stamp')
        get_avg_of_cities = {}
        for w in weather_objs:
            get_avg_of_cities.update({w.city: {}})
            for param in self.weather_params:
                get_avg_of_cities[w.city].update(self.calculate_avg(w, param))
        # random weight assign to various weather params
        wt_given = {'temp': 45, 'pressure': 5, 'humidity': 30, 'dew_point': 5, 'uvi': 5, 'wind_gust': 5,
            'wind_speed': 5}
        # get similarity percentages
        data = []
        weight = 0
        for city in cities:
            for param, wt in wt_given.items():
                city_data = get_avg_of_cities[city]
                weight += city_data[param] * wt
            data.append({'city': city, 'weight': weight/100})
        data = sorted(data, key = lambda i: i['weight'])
        similarity_percentage = (data[0]['weight']/data[1]['weight']) * 100
        data.append({'similarity_percentage': similarity_percentage})
        return Response(data=data)
