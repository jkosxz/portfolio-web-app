from django.contrib import admin
from .models import Investment, Portfolio, Asset, Transaction, DeletedInvestment


class AssetAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol', 'last_fetched')


class InvestmentAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'symbol', 'amount', 'price_bought', 'type')


class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('username', 'investments')


class DeletedInvestmentAdmin(admin.ModelAdmin):
    list_display = ('investment_name', 'investment_username')


admin.site.register(Asset, AssetAdmin)
admin.site.register(Investment, InvestmentAdmin)
admin.site.register(DeletedInvestment, DeletedInvestmentAdmin)
