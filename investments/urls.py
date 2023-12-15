from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_investment', views.add_investment, name='add_investment'),
    path('del_investment', views.del_investment, name='del_investment'),
    path('show_assets', views.show_all_assets, name='show_assets')
]
