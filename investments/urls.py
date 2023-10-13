from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dodaj_inwestycje', views.dodaj_inwestycje, name='dodaj_inwestycje'),
    path('usun_inwestycje', views.usun_inwestycje, name='usun_inwestycje'),
]
