from django.shortcuts import render, redirect
from .models import Investment


def index(request):
    portfolio = Investment.objects.all()
    return render(request, 'investments/index.html', {'portfolio': portfolio})


def add_investment(request):
    if request.method == 'POST':
        name = request.POST['name']
        amount = request.POST['amount']
        Investment.objects.create(name=name, amount=amount)
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
