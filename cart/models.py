from django.db import models
from app1.models import Product
from django.contrib.auth.models import User
from decimal import Decimal

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.user:
            return f"سبد {self.user.username}"
        return f"سبد مهمان ({self.session_key})"

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def get_unit_price(self):
        return self.product.get_final_price() 

    def get_unit_price(self):
        if hasattr(self.product, 'sale') and self.product.sale:
            return self.product.sale_price
        return self.product.price

    def get_total_price(self):
        return Decimal(self.get_unit_price()) * self.quantity

    def __str__(self):
        return f"{self.quantity} × {self.product.name}"