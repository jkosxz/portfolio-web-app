from django.contrib import admin
from .models import Investment, Portfolio, Asset, Transaction

admin.site.register(Investment)
admin.site.register(Portfolio)
admin.site.register(Asset)
admin.site.register(Transaction)