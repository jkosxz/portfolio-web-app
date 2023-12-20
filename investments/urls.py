from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_investment', views.add_investment, name='add_investment'),
    path('del_investment', views.del_investment, name='del_investment'),
<<<<<<< HEAD
    path('show_assets', views.show_all_assets, name='show_assets')
=======
    path('show_all_assets', views.show_all_assets, name='show_all_assets'),
    path('show_users_investments', views.show_users_investments, name='show_users_investments'),
    path('insert_assets', views.insert_assets),
    path('delete_assets', views.delete_assets),
    path('show_specific_investment', views.show_specific_investment, name='show_specific_investment')
>>>>>>> e97ad1182e0e4750a3a41a97d41dc3702f89046e
]
