from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('autocomplete/', views.search_autocomplete, name='autocomplete'),
    path('nearby/', views.nearby_pharmacies, name='nearby'),
    path('medicine/<int:medicine_id>/availability/', views.medicine_availability, name='medicine_availability'),
    path('regions/', views.regions_list, name='regions'),
]
