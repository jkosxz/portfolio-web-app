import datetime

from django.shortcuts import render, redirect
from .models import Investment, Asset
from investments.api_utils.api_fetcher import get_all_symbols, get_prices, get_current_prices
from django.http import HttpResponse
from django.contrib.auth.models import User


def refresh_prices(request):
    users_investments = Investment.objects.filter(username=request.user)
    users_assets = []
    for asset in users_investments:
        users_assets.append(asset.symbol)

    current_prices = get_current_prices(users_assets)
    for asset_name, current_price in current_prices.items():
        asset = Asset.objects.get(symbol=asset_name)
        setattr(asset, 'current_price', current_price)
        asset.save()


def insert_assets(request):
    assets = get_all_symbols()
    assets_in_db = Asset.objects.all()
    records = []
    for asset in assets:
        if asset in assets_in_db:
            continue
        records.append(Asset(name=asset['description'], symbol=asset['symbol']))
    Asset.objects.bulk_create(records)
    return HttpResponse()


def delete_assets(request):
    Asset.objects.all().delete()
    return HttpResponse("Deleted all assets")


def index(request):
    portfolio = Investment.objects.all()
    return render(request, 'investments/index.html', {'portfolio': portfolio})


def add_investment(request):
    if request.method == 'POST':
        name = request.POST['inv_name']
        symbol = Asset.objects.get(symbol=request.POST['inv_symbol'])
        amount = request.POST['inv_amount']
        price = request.POST['inv_price']
        type = request.POST['inv_type']
        date_bought = datetime.datetime.now()

        Investment.objects.create(name=name, symbol=symbol, amount=amount, price_bought=price,
                                  type=type, username=request.user.username, date_bought=date_bought)
        return redirect('index')
    return render(request, 'investments/addInvestment.html')


def del_investment(request):
    investment = Investment.objects.get(id=request.GET.get('id', request.GET['id']))
    investment.delete()
    return render(request, 'investments/delInvestment.html')


def show_all_assets(request):
    assets = Asset.objects.all()

    return render(request, 'investments/show_assets.html', {'assets': assets})


def show_users_investments(request):
    refresh_prices(request)

    investments = Investment.objects.filter(username=request.user.username)
    users_assets = []
    for investment in investments:
        users_assets.append(investment.symbol)

    return render(request, 'investments/show_users_investments.html',
                  {'investments': investments, 'assets': users_assets})


def show_specific_investment(request):
    investment = Investment.objects.get(id=request.GET.get('id', request.GET['id']))
    return render(request, 'investments/investment.html', {'investment': investment})
