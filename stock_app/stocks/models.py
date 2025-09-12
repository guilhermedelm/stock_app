from django.db import models

# Create your models here.

class StockPrice(models.Model):
    symbol = models.CharField(max_length = 10)
    name   =models.CharField(max_length = 100)
    price  = models.FloatField()
    timestampt = models.DateTimeField(auto_now_add = True)

    def  __str__(self):
        return f"{self.symbol} - {self.price}"
    

