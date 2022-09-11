from django.urls import path
from . import views

urlpatterns=[
    path('', views.index),
    path('demand/', views.demand, name='demand'),
    path('helmet/', views.helmet, name='helmet'),
    path('parking/', views.parking, name='parking'),
    path('accident/', views.accident, name='accident')
    ]