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
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL, blank=True, null=True)
    date_Order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,null=True,blank=False)
    transaction_id = models.CharField(max_length=200, null=True)
    def __str__(self):
        return f"Order {self.id} by {self.customer.username}"

    def get_total(self):
        # Tính tổng tiền của đơn hàng
        return sum(item.quantity * item.product.price for item in self.orderitem_set.all())
class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.id}"
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
    