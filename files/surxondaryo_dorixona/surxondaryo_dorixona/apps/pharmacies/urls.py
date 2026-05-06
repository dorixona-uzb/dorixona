from django.urls import path
from . import views

app_name = 'pharmacies'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('pharmacies/', views.PharmacyListView.as_view(), name='list'),
    path('pharmacy/<slug:slug>/', views.PharmacyDetailView.as_view(), name='detail'),
    path('region/<slug:slug>/', views.RegionDetailView.as_view(), name='region_detail'),
]
