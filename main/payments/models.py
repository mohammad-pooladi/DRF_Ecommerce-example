from django.db import models
from django.conf import settings
from main.orders.models import Order
from main.common.models import BaseModel



class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="addresses")
    country = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=255)
    house_number = models.CharField(max_length=20)
    postal_code = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.city}, {self.street}, {self.house_number}"


class Payment(BaseModel):
    STATUS_CHOICES = (
        ('pending', 'Panding'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, blank=True, null=True, unique=True)
    pyment_method = models.CharField(max_length=50, choices=[('crypto', 'Crypto')])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='panding')
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f'Payment {self.id} - {self.status}'
