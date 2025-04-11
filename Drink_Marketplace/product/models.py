from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=False)
    name = models.CharField(max_length= 20, null=True)
    email = models.CharField(max_length= 200, null=True)
    def __str__(self):
        return self.name
class Product(models.Model):
  
    name = models.CharField(max_length= 20, null=True)
    price = models.FloatField()
    description = models.TextField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    def __str__(self):
        return self.name
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Đơn hàng #{self.id} - {self.user.username}"
    def get_total_price(self):
        return sum(item.total_price() for item in self.items.all())
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.FloatField()

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    def total_price(self):
        return self.quantity * self.price
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200,null=True)
    city = models.CharField(max_length=200,null=True)
    Province = models.CharField(max_length=200,null=True)
    phoneNumber = models.CharField(max_length=10,null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.address
    