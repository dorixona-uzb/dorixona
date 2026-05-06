from django.urls import path
from . import views

app_name = 'medicines'

urlpatterns = [
    path('', views.MedicineListView.as_view(), name='list'),
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category'),
    path('<slug:slug>/', views.MedicineDetailView.as_view(), name='detail'),
]
