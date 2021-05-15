import requests
import json

from django.shortcuts import render
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Weather


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
    divisions = None
    report_type = ''
    REPORT_DATE_FORMAT = '%B %Y'
    DATE_RANGE_FORMAT = '%m/%d/%Y'

    def get_months(self, parameters: dict):
        try:
            start, end = get_range(parameters)
        except KeyError:
            return []
        if self.settings.spend_by_month:
            months = [
                month_start.strftime(self.REPORT_DATE_FORMAT) for month_start, month_end in get_months(start, end)
            ]
        else:
            months = [' - '.join([start.strftime(self.DATE_RANGE_FORMAT), end.strftime(self.DATE_RANGE_FORMAT)])]
        return months

    def post(self, request):
        paramters = request.POST or request.data
        company = request.company
        self.report_type = paramters.get('report_type')
        self.settings = TierOneReportSettings.objects.get(company=company)
        self.divisions = paramters.get('divisions')
        if self.divisions == '':
            self.divisions = None
        result = {
            'line_chart_type': self.report_type in LINE_CHART_TYPE,
            'pie_chart_type': self.report_type in PIE_CHART_TYPE,
            'spend_chart_type': self.report_type in SPEND_CHART_TYPE,
            'table_chart_type': self.report_type in TABLE_CHART_TYPE,
            'show_date_range': self.report_type in LINE_CHART_TYPE or self.report_type in SPEND_CHART_TYPE
        }

        if self.report_type in LINE_CHART_TYPE or self.report_type in SPEND_CHART_TYPE:
            months = self.get_months(paramters)
        else:
            months = []
        result.update({'months': months})
        result.update({'report_url': reverse('mobile_' + self.report_type)})
        return Response(data=result)