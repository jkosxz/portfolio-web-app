from django.urls import path, include
from . import views

urlpatterns = [
    # multi Jinja generated templates
    path('', views.index, name='index'),
    path('show_users_investments', views.show_users_investments, name='show_users_investments'),
    path('show_assets', views.show_all_assets, name='show_assets'),
    path('show_all_assets', views.show_all_assets, name='show_all_assets'),
    path('users_history', views.show_users_history, name='users_history'),

    # Actions
    path('insert_assets', views.insert_assets),
    path('delete_assets', views.delete_assets),
    path('add_investment', views.add_investment, name='add_investment'),
    path('del_investment', views.del_investment, name='del_investment'),
    path('refresh_prices', views.refresh_prices, name='refresh_prices'),
    path('convert_to_pdf', views.save_to_pdf_investments, name='convert_to_pdf'),
    path('convert_to_pdf_history', views.save_to_pdf_history, name='convert_to_pdf_history'),

    # single Jinja generated templates
    path('investment', views.show_specific_investment, name='investment'),
    path('asset', views.show_specific_asset, name='asset')

]
