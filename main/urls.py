from django.conf import settings
from django.urls import url
from django.conf.urls.static import static
from . import views

urlpatterns=[
    url(r'^index/$', views.index, name='index'),
    url(r'^demand/$', views.demand, name='demand'),
    url(r'^helmet/$', views.helmet, name='helmet'),
    url(r'^parking/$', views.parking, name='parking'),
    ]