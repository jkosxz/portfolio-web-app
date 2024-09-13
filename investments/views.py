import datetime

from django.shortcuts import render, redirect
from reportlab.lib import pdfencrypt, colors
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch, mm

from .models import Investment, Asset, DeletedInvestment, FavouriteUsersAsset
from investments.api_utils.api_fetcher import get_all_symbols, get_prices, get_current_prices
from django.http import HttpResponse, FileResponse
from django.contrib.auth.models import User
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
import io
from datetime import datetime


def evaluate_users_investments(request):
    users_investments = Investment.objects.filter(username=request.user.username)
    if len(users_investments) == 0:
        return None

    res = 0
    for investment in users_investments:
        res += investment.profit

    return res / len(users_investments)


def refresh_price_of_asset(request, symbol):
    asset = Asset.objects.get(symbol=symbol)
    setattr(asset, 'current_price', get_current_prices([asset])[asset.symbol])
    asset.save()


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
    evaluation = evaluate_users_investments(request)
    fav_assets = FavouriteUsersAsset.objects.filter(username=request.user.username)
    return render(request, 'investments/index.html', {'portfolio_evaluation': evaluation,
                                                      'fav_assets': fav_assets})


def add_investment(request):
    if request.method == 'POST':
        name = request.POST['inv_name']
        symbol = Asset.objects.get(symbol=request.POST['inv_symbol'])
        amount = request.POST['inv_amount']
        price = request.POST['inv_price']
        type = request.POST['inv_type']
        date_bought = datetime.now()

        Investment.objects.create(name=name, symbol=symbol, amount=amount, price_bought=price,
                                  type=type, username=request.user.username, date_bought=date_bought)
        return redirect('index')
    return render(request, 'investments/addInvestment.html')


def del_investment(request):
    investment = Investment.objects.get(id=request.GET.get('id', request.GET['id']))
    deleted_investment = DeletedInvestment.objects.create(investment_username=investment.username,
                                                          investment_name=investment.name, symbol_d=investment.symbol,
                                                          price_bought=investment.get_current_price,
                                                          price_when_deleted=investment.get_current_price,
                                                          date_bought=investment.date_bought,
                                                          date_deleted=datetime.now())
    deleted_investment.save()
    investment.delete()
    return render(request, 'investments/delInvestment.html')


def show_all_assets(request):
    assets = Asset.objects.all()

    return render(request, 'investments/show_assets.html', {'assets': assets})


def show_users_investments(request):
    refresh_prices(request)

    investments = Investment.objects.filter(username=request.user.username)
    print(request.user.username, investments)
    users_assets = []
    for investment in investments:
        users_assets.append(investment.symbol)

    return render(request, 'investments/show_users_investments.html',
                  {'investments': investments, 'assets': users_assets})


def show_specific_investment(request):
    investment = Investment.objects.get(id=request.GET.get('id', request.GET['id']))
    return render(request, 'investments/investment.html', {'investment': investment})


def show_specific_asset(request):
    asset = Asset.objects.get(symbol=request.GET['symbol'])
    refresh_price_of_asset(request, asset.symbol)

    try:
        fav_asset = FavouriteUsersAsset.objects.get(username=request.user.username, symbol=asset.symbol)
    except:
        fav_asset = False

    return render(request, 'investments/asset.html', {'asset': asset,
                                                      'is_fav': fav_asset})


def save_to_pdf_investments(request):
    enc = pdfencrypt.StandardEncryption("pass", canPrint=0)
    buf = io.BytesIO()
    c = canvas.Canvas(buf, encrypt=enc, bottomup=0)
    width, height = letter
    lines = []
    investments = Investment.objects.filter(username=request.user.username)
    for investment in investments:
        lines.append((investment.name, investment.symbol, investment.get_current_price, investment.profit,
                      investment.date_bought))
    lines.append(("Name", "Symbol", "Current Price", "Profit", "Date bought"))
    table = Table(lines, colWidths=43 * mm)
    table.setStyle(TableStyle([
        ('SIZE', (0, 0), (-1, -1), 7),
        ('SIZE', (0, 0), (0, 0), 5.5),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ]))

    table.wrapOn(c, width, height)
    table.drawOn(c, 0 * mm, 5 * mm)

    c.save()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename=f'{datetime.now()}.pdf')


def save_to_pdf_history(request):
    enc = pdfencrypt.StandardEncryption("pass", canPrint=0)
    buf = io.BytesIO()
    c = canvas.Canvas(buf, encrypt=enc, bottomup=0)
    width, height = letter
    lines = []
    investments = DeletedInvestment.objects.filter(investment_username=request.user.username)
    for investment in investments:
        lines.append((investment.investment_name, investment.symbol_d, round(investment.price_bought),
                      round(investment.price_when_deleted, 2),
                      investment.date_bought, investment.date_deleted))
    lines.append(("Name", "Symbol", "Price when bought", "Price when deleted", "Date bought", "Date deleted"))
    table = Table(lines, colWidths=36 * mm)
    table.setStyle(TableStyle([
        ('SIZE', (0, 0), (-1, -1), 7),
        ('SIZE', (0, 0), (0, 0), 5.5),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ]))

    table.wrapOn(c, width, height)
    table.drawOn(c, 0 * mm, 5 * mm)

    c.save()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename=f'history-{datetime.now()}.pdf')


def show_users_history(request):
    users_deleted_investment = DeletedInvestment.objects.filter(investment_username=request.user.username)
    return render(request, 'investments/users_investment_history.html',
                  {'deleted_investments': users_deleted_investment})


def add_favourite_asset(request):
    pass


def delete_favourite_asset(request):
    pass
