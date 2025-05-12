from django.db import models
from django.conf import settings
from main.common.models import BaseModel


class Order(BaseModel):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("canceled", "Canceled"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders"
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    def __str__(self):
        return f"Order {self.pk} - {self.user.username} - {self.status}"


class OrderItem(models.Model):
    orders = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    products = models.ForeignKey("products.Products", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.products.name} in Order {self.orders.id}"
