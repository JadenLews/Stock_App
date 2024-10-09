from django.db import models
import uuid

class Account(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=100)
    
class Stock(models.Model):
    symbol = models.CharField(primary_key=True, max_length=5)
    company_name = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
class Portfolio(models.Model):
    user = models.ForeignKey("Account", on_delete=models.CASCADE)
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
    user = models.ForeignKey("Account", on_delete=models.CASCADE)
    stock = models.ForeignKey("Stock", on_delete=models.CASCADE)
    date = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        unique_together = ('user', 'stock', 'date')

    def __str__(self):
        return f"{self.gameID} - {self.awayScore}- {self.homeScore}- {self.awayPos}- {self.homePos}"
