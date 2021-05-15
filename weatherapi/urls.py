from django.urls import path

from .views import CollectData
from .views import SimilarCitiesView


app_name = 'weather-api'

urlpatterns = [
    path('collect-data/', CollectData.as_view(), name='collect_data'),
    path('similar-cities/', SimilarCitiesView.as_view(), name='similar_cities'),
]
