from enum import unique
from telnetlib import STATUS
import uuid
from django.conf import settings
from django.db import models
from cart.models import Coupon
from product.models import Product

class OrderItem(models.Model):
    product = models.ForeignKey(Product, related_name='ordered', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField()
    
    class Meta:
        ordering = ['-id']
        
    def __str__(self) -> str:
        return f"{self.product.title} x {self.quantity}"
    
class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
        ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="orders", on_delete=models.CASCADE)
    order_item = models.ManyToManyField(OrderItem)
    coupon = models.ForeignKey(Coupon, null=True, blank=True, on_delete=models.SET_NULL)
    
    order_id = models.CharField(max_length=12, unique=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=150)
    city =  models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    address = models.TextField()
    total = models.DecimalField(max_digits=8, decimal_places=2)
    paid = models.BooleanField(default=True)
    status = models.CharField(max_length=15, choices=list(zip(STATUS, STATUS)))
    created_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_date']
        
        
    def __str__(self) -> str:
        return f"Order {self.order_id} - {self.first_name} {self.last_name}"
    
    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = self.generate_unique_order_id()
        super().save(*args, **kwargs)
        
    def generate_unique_order_if(self):
        order_id = uuid.uuid4().hex[:12].upper()
        while Order.objects.filter(order_id = order_id).excists():
            order_id = uuid.uuid4.hex[:12].upper()
        return order_id