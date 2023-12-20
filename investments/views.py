from django.shortcuts import render, redirect
from .models import Investment, Asset
from investments.api_utils.api_fetcher import get_all_symbols
from django.http import HttpResponse
from django.contrib.auth.models import User


def insert_assets(request):
    assets = get_all_symbols()
    assetsindb = Asset.objects.all()
    records = []
    for asset in assets:
        if asset in assetsindb:
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
        print(request.user.username)
        user = User.objects.get(username=request.user.username)

        Investment.objects.create(name=name, symbol=symbol, amount=amount, price_bought=price,
                                  type=type, username=request.user.username)
        return redirect('index')
    return render(request, 'investments/addInvestment.html')


def del_investment(request):
    if request.method == 'POST':
        name = request.POST['name']
        amount = request.POST['amount']
        investment = Investment.objects.get(nazwa=name)
        if investment.amount >= float(amount):
            investment.amount -= float(amount)
            investment.save()
        else:
            error_message = "Error"
            return render(request, 'investments/delInvestment.html', {'error_message': error_message})
        return redirect('index')

    return render(request, 'investments/delInvestment.html')

def show_all_assets(request):
    assets = Asset.objects.all()

    return render(request, 'investments/show_assets.html', {'assets': assets})


def show_users_investments(request):
    investments = Investment.objects.filter(username=request.user.username)

    return render(request, 'investments/show_users_investments.html', {'investments': investments})


def show_specific_investment(request):
    investment = Investment.objects.get(id=request.GET.get('id', request.GET['id']))
    return render(request, 'investments/show_users_investments.html', {'investments': [investment]})
