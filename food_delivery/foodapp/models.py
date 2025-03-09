from django.db import models
from django.contrib.auth.models import AbstractUser
from foodapp.choices import StatusChoices

class User(AbstractUser):

    phone_number = models.CharField(max_length=10)
    age = models.PositiveIntegerField(null=True , blank=True)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=50)

    def __str__(self):
        return self.username
        

class Restaurant(models.Model):

    name = models.CharField(max_length=20)
    address = models.TextField()
    contact_number = models.CharField( max_length=11)
    opening_time=models.TimeField(auto_now=True)
    closing_time=models.TimeField(auto_now=True)
    is_active=models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    

class MenuItem(models.Model):

    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits= 6,decimal_places=2)

    def __str__(self):
        return self.name
    

class Customer(models.Model):
    name = models.CharField(max_length=20)
    phone_number = models.CharField(max_length = 11)
    current_location = models.CharField(max_length=15)

    def __str__(self):
        return self.name
    

class DeliveryPerson(models.Model):

    name = models.CharField(max_length=20)
    phone_number = models.CharField(max_length = 11)
    vehicle_number = models.CharField(max_length = 15)

    def __str__(self):
        return self.name
        
           
class Order(models.Model):

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    restaurant=models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status= models.CharField(max_length=20,choices=StatusChoices.choices,default=StatusChoices.PENDING)


class OrderItem(models.Model):

    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


class Delivery(models.Model):

    order = models.OneToOneField(Order,models.CASCADE)
    delivery_person = models.ForeignKey(DeliveryPerson,models.CASCADE)
    delivery_address = models.CharField(max_length=15)
    estimated_delivery_time = models.IntegerField()
    actual_delivery_time = models.IntegerField()

    def __str__(self):
        return str(self.actual_delivery_time)


class Payment(models.Model):
 
    order = models.OneToOneField(Order,on_delete = models.CASCADE)
    amount = models.DecimalField(max_digits=6,decimal_places=2)
    payment_method = models.CharField(max_length=10)
    payment_status = models.CharField(max_length=20)
    payment_date = models.DateTimeField(auto_now_add=True)

