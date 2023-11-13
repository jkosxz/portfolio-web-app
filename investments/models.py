from django.db import models


class Investment(models.Model):
    name = models.CharField(max_length=100)
    amount = models.FloatField()

    def __str__(self):
        return self.amount
