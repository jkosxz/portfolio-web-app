from django.db import models


class Asset(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=100)
    last_fetched = models.DateField(default="2000-1-1")

    def __str__(self):
        return str(self.name)


class Investment(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.ForeignKey(Asset, on_delete=models.CASCADE)
    amount = models.FloatField()
    type = models.CharField(max_length=100)

    def __str__(self):
        return str(self.amount)


class Portfolio(models.Model):
    name = models.CharField(max_length=100)
    investments = models.ManyToManyField(Investment)

    def __str__(self):
        return str(self.name)


class Transaction(models.Model):
    name = models.CharField(max_length=100)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=[('buy', 'Buy'), ('sell', 'Sell')])
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

