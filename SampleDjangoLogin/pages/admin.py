from django.contrib import admin
from .models import PriceHistory, Transaction, Portfolio, Stock, Watchlist, Notification

# Register your models here.
admin.site.register(PriceHistory)
admin.site.register(Transaction)
admin.site.register(Portfolio)
admin.site.register(Stock)
admin.site.register(Watchlist)
admin.site.register(Notification)


