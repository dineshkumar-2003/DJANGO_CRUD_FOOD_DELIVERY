from django.contrib import admin
from foodapp.models import *
admin.site.register(Restaurant)
admin.site.register(User)
admin.site.register(MenuItem)
admin.site.register(Customer)
admin.site.register(DeliveryPerson)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Delivery)
admin.site.register(Payment)
