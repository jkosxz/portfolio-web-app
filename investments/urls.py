from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_investment', views.add_investment, name='add_investment'),
    path('del_investment', views.del_investment, name='del_investment'),
    path('show_assets', views.show_all_assets, name='show_assets'),
    path('show_all_assets', views.show_all_assets, name='show_all_assets'),
    path('show_users_investments', views.show_users_investments, name='show_users_investments'),
    path('insert_assets', views.insert_assets),
    path('delete_assets', views.delete_assets),
    path('investment', views.show_specific_investment, name='investment')
]
