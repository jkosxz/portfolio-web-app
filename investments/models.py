from django.db import models
from django.contrib.auth.models import User


class Asset(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=100, unique=True)
    last_fetched = models.DateField(default="2000-1-1")
    current_price = models.FloatField(default=0.0)

    def __str__(self):
        return str(self.symbol)


class Investment(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.ForeignKey(Asset, on_delete=models.CASCADE)
    amount = models.FloatField()
    price_bought = models.FloatField()
    date_bought = models.DateField(default="2000-1-1")
    type = models.CharField(max_length=100)
    username = models.CharField(max_length=100, default="")

    def __str__(self):
        return str(self.symbol)

    @property
    def get_current_price(self):
        price = Asset.objects.get(symbol=self.symbol).current_price
        return price

    @property
    def profit(self):
        price = Asset.objects.get(symbol=self.symbol).current_price
        return price - self.price_bought


class Portfolio(models.Model):
    name = models.CharField(max_length=100)
    investments = models.ManyToManyField(Investment)

    def __str__(self):
        return str(self.name)


# ?
class Transaction(models.Model):
    name = models.CharField(max_length=100)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=[('buy', 'Buy'), ('sell', 'Sell')])
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)


class DeletedInvestment(models.Model):
    investment_name = models.CharField(max_length=100, default="")
    investment_username = models.CharField(max_length=100, default="")
    symbol_d = models.ForeignKey(Asset, to_field='symbol', on_delete=models.CASCADE, default=None)
    price_bought = models.FloatField(default=0.0)
    price_when_deleted = models.FloatField(default=0.0)
    date_bought = models.DateField(default='2000-1-1')
    date_deleted = models.DateField(default='2000-1-1')


    def __str__(self):
        return f'Deleted {self.investment_name}'


class FavouriteUsersAsset(models.Model):
    username = models.CharField(max_length=100, default='')
    symbol = models.ForeignKey(Asset, default=None, on_delete=models.CASCADE)
