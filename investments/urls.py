from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_investment', views.add_investment, name='add_investment'),
    path('del_investment', views.del_investment, name='del_investment'),
    path('show_all_assets', views.show_all_assets, name='show_all_assets'),
    path('insert_assets', views.insert_assets),
    path('delete_assets', views.delete_assets)
]
