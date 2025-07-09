import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    pass

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    @property
    def in_stock(self):
        return self.stock > 0
    
    def __str__(self):
        return self.name
    
class Order(models.Model):
    class Status_Choices(models.TextChoices):
        PENDING = 'Pending'
        CONFIRMED = 'Confirmed'
        CANCELLED = 'Cancelled'
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=Status_Choices.choices,
        default=Status_Choices.PENDING
    )
    products = models.ManyToManyField(Product, through='OrderItem',related_name='orders')
    def __str__(self):
        return f"Order {self.id} by {self.user.username}" 
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    order = models.ForeignKey(Order , on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    @property
    def Item_Subtotal(self):
        return self.quantity * self.Product.price
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.id}"
        