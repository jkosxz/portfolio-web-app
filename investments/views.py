from django.shortcuts import render, redirect
from .models import Investment

def index(request):
    portfel = Investment.objects.all()
    return render(request, 'inwestycje/index.html', {'portfel': portfel})

def dodaj_inwestycje(request):
    if request.method == 'POST':
        nazwa = request.POST['nazwa']
        ilosc = request.POST['ilosc']
        Investment.objects.create(nazwa=nazwa, ilosc=ilosc)
        return redirect('index')
    return render(request, 'inwestycje/addInvestment.html')

def usun_inwestycje(request):
    if request.method == 'POST':
        nazwa = request.POST['nazwa']
        ilosc = request.POST['ilosc']
        inwestycja = Investment.objects.get(nazwa=nazwa)
        if inwestycja.ilosc >= float(ilosc):
            inwestycja.ilosc -= float(ilosc)
            inwestycja.save()
        else:
            error_message = "Brak wystarczających środków lub brak inwestycji w portfelu."
            return render(request, 'inwestycje/delInvestment.html', {'error_message': error_message})
        return redirect('index')
    return render(request, 'inwestycje/delInvestment.html')
