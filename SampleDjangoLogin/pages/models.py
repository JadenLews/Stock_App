from django.db import models
from django.contrib.auth.models import User  # Import the built-in User model
import uuid

class Stock(models.Model):
    symbol = models.CharField(primary_key=True, max_length=5)
    company_name = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Use built-in User model
    stock = models.ForeignKey("Stock", on_delete=models.CASCADE)
    num_shares = models.DecimalField(max_digits=10, decimal_places=5)
    
    class Meta:
        unique_together = ('user', 'stock')

class PriceHistory(models.Model):
    stock = models.ForeignKey("Stock", on_delete=models.CASCADE)
    date = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        unique_together = ('stock', 'date')

class Transaction(models.Model):
    transaction_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Use built-in User model
    stock = models.ForeignKey("Stock", on_delete=models.CASCADE)
    date = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        unique_together = ('user', 'stock', 'date')

    def __str__(self):
        return f"Transaction {self.transaction_id} - {self.user.username} - {self.stock.symbol} - {self.date}"
    
class Watchlist(models.Model):
    stock = models.ForeignKey("Stock", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Use built-in User model
    
    class Meta:
        unique_together = ('stock', 'user')

class Notification(models.Model):
    STATUS_CHOICES = [
        ('unviewed', 'Unviewed'),
        ('viewed', 'Viewed'),
    ]

    message = models.TextField()  # Notification message
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')  # User receiving the notification
    stock = models.ForeignKey('Stock', null=True, blank=True, on_delete=models.CASCADE, related_name='notifications')  # Stock related to the notification, nullable for system notifications
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unviewed')  # Status of the notification
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set the timestamp when created
    