import json
from foodapp.models import *
from foodapp.serializers import * 
from rest_framework import status,generics
from django.contrib.auth.models import Group
from rest_framework.views import APIView
from geopy.geocoders import Nominatim
from geopy.distance import geodesic 
from datetime import datetime, timedelta
from rest_framework.response import Response
from django.utils.timezone import now
from foodapp.choices import StatusChoices
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse


def is_normal_user(user):
    return user.groups.filter(name='Normal users').exists()

def is_customer(user):
    return user.groups.filter(name='customers').exists()

def is_normal_or_customer(user):
    return user.groups.filter(name__in=['Normal users', 'customers']).exists()

def example(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'example.html',{"restaurants":restaurants})
def index(request):
    return render(request, 'index.html')

@user_passes_test(is_normal_or_customer)
def restaurants(request):
    object_list=Restaurant.objects.all()
    paginator=Paginator(object_list,1)
    page_number=request.GET.get('page') 
    page_obj=paginator.get_page(page_number)
    return render(request, 'restaurants.html',{'page_obj':page_obj})

@user_passes_test(is_normal_user)
def add_restaurant(request):
    return render(request, 'add_restaurant.html',{'user':request.user})
@user_passes_test(is_normal_user)
def users(request):
    return render(request, 'users.html')
@user_passes_test(is_customer)
def menu(request):
    return render(request, 'menu.html')
@user_passes_test(is_normal_or_customer)
def base(request):
    return render(request, 'base.html')
@user_passes_test(is_customer)
def order(request):
    return render(request, 'orders.html')
def group(request):
    return render(request, 'groups.html')   

def add_user_group(request):
    if request.method=="POST":
        data=json.loads(request.body)
        username=data.get("username")
        user=User.objects.get(username=username)
        group_name=data.get("groupname")
        group,created=Group.objects.get_or_create(name=group_name)
        user.groups.add(group)
        return JsonResponse({"message": f"User {username} added to {group_name}"}, status=200)

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        age = request.POST["age"]
        phone_number = request.POST["phone_no"]
        email = request.POST["email"]
        address = request.POST["address"]
        user = User.objects.create_user(username=username, password=password, age=age, phone_number=phone_number, email=email, address=address)
        user.save()
        return redirect("/login/")
    return render(request, "register.html")

def custom_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect("http://127.0.0.1:8000/index.html")  # Redirect to home page after login
        else:
            return render(request, "login.html", {"error": "User ID or Password is incorrect"})

    return render(request, "login.html")



class GroupListCreate(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class UserListCreate(APIView):
    #permission_classes = [AllowAny]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetail(APIView):
    #permission_classes = [AllowAny]

    def get_object(self,pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None
        
    def get(self,request,pk):
        user=self.get_object(pk)
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user = self.get_object(pk)
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class RestaurantListCreate(APIView):
    #permission_classes = [IsAuthenticated]

    def get(self, request):
        current_time= now().time()
        restaurants = Restaurant.objects.filter(
            is_active =True,
            #opening_time__lte=current_time,
            #closing_time__gte=current_time

        )
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RestaurantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RestaurantDetail(APIView):
    #permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Restaurant.objects.get(pk=pk)
        except Restaurant.DoesNotExist:
            return None

    def get(self, request, pk):
        restaurant = self.get_object(pk)
        if restaurant is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = RestaurantSerializer(restaurant)
        return Response(serializer.data)

    def put(self, request, pk):
        restaurant = self.get_object(pk)
        if restaurant is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = RestaurantSerializer(restaurant, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        restaurant = self.get_object(pk)
        if restaurant is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        restaurant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class MenuItemListCreate(APIView):
    #permission_classes = [IsAuthenticated]

    def get(self, request):
        restaurant_id=request.query_params.get('restaurant',None)
        if restaurant_id:
            try:
                menu_items=MenuItem.objects.filter(restaurant=restaurant_id)
                if not menu_items.exists():
                    return Response({"detail": "No menu items found for this restaurant."}, status=status.HTTP_404_NOT_FOUND)
            except Restaurant.DoesNotExist:
                return Response({"detail": "Restaurant not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            # If no restaurant_id is provided, return all menu items
            menu_items = MenuItem.objects.all()
        serializer = MenuItemSerializer(menu_items, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = MenuItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MenuItemDetail(APIView):
    #permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return MenuItem.objects.get(pk=pk)
        except MenuItem.DoesNotExist:
            return None

    def get(self, request, pk):
        menu_item = self.get_object(pk)
        if menu_item is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MenuItemSerializer(menu_item)
        return Response(serializer.data)

    def put(self, request, pk):
        menu_item = self.get_object(pk)
        if menu_item is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MenuItemSerializer(menu_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        menu_item = self.get_object(pk)
        if menu_item is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        menu_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CustomerListCreate(APIView):
    #permission_classes = [IsAuthenticated]

    def get(self, request):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomerDetail(APIView):
    #permission_classes = [IsAuthenticated]

    def get_object(self, pk,user):
        try:
            customer= Customer.objects.get(pk=pk)
            if customer.user !=user:
                raise PermissionError("You don't habe permission to access this resource")
            return customer
        except Customer.DoesNotExist:
            return None

    def get(self, request, pk):
        customer = self.get_object(pk,request.user)
        if customer is None:
            return Response({"error":"Customer not found"},status=status.HTTP_404_NOT_FOUND)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def put(self, request, pk):
        customer = self.get_object(pk)
        if customer is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        customer = self.get_object(pk)
        if customer is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class DeliveryPersonListCreate(APIView):
    #permission_classes = [IsAuthenticated]

    def get(self, request):
        delivery_persons = DeliveryPerson.objects.all()
        serializer = DeliveryPersonSerializer(delivery_persons, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DeliveryPersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeliveryPersonDetail(APIView):
    #permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return DeliveryPerson.objects.get(pk=pk)
        except DeliveryPerson.DoesNotExist:
            return None

    def get(self, request, pk):
        delivery_person = self.get_object(pk)
        if delivery_person is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = DeliveryPersonSerializer(delivery_person)
        return Response(serializer.data)

    def put(self, request, pk):
        delivery_person = self.get_object(pk)
        if delivery_person is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = DeliveryPersonSerializer(delivery_person, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        delivery_person = self.get_object(pk)
        if delivery_person is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        delivery_person.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class OrderListCreate(APIView):
    #permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderDetail(APIView):
    #permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return None

    def get(self, request, pk):
        order = self.get_object(pk)
        if order is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def put(self, request, pk):
        order = self.get_object(pk)
        if order is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        order = self.get_object(pk)
        if order is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderActionsView(APIView):
    #permission_classes = [IsAuthenticated]

    """
    Handles custom actions for specific orders: calculating delivery time, marking as delivered, canceling.
    """

    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return None

    def calculate_delivery_time(self, order):
        """
        A function to calculate the estimated delivery time for an order.
        It uses the geolocation of the restaurant and the customer.
        """
        geolocator = Nominatim(user_agent="food_delivery_app")
        restaurant_location = geolocator.geocode(order.restaurant.address)
        customer_location = geolocator.geocode(order.customer.current_location)

        if restaurant_location and customer_location:
            restaurant_coords = (restaurant_location.latitude, restaurant_location.longitude)
            customer_coords = (customer_location.latitude, customer_location.longitude)
            distance = geodesic(restaurant_coords, customer_coords).km
            
            # Assuming average delivery speed is 40 km/h
            estimated_time = distance / 40 * 60  # Time in minutes
            return datetime.now() + timedelta(minutes=estimated_time)
        return None

    def get(self, request, pk, action):
        """
        GET method for actions like 'estimated_time'.
        Accessible at: /orders/{pk}/actions/{action}/ (e.g., /orders/1/actions/estimated_time/)
        """
        order = self.get_object(pk)
        if order is None:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        if action == 'estimated_time':
            estimated_time = self.calculate_delivery_time(order)
            if estimated_time:
                return Response({"estimated_delivery_time": estimated_time.strftime("%Y-%m-%d %H:%M:%S")}, status=status.HTTP_200_OK)
            return Response({"error": "Could not calculate delivery time"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, pk, action):
        """
        POST method for actions like 'mark_as_delivered' and 'cancel_order'.
        Accessible at: /orders/{pk}/actions/{action}/ (e.g., /orders/1/actions/mark_as_delivered/)
        """
        order = self.get_object(pk)
        if order is None:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        if action == 'mark_as_delivered':
            if order.status == StatusChoices.DELIVERED:
                return Response({"message": "Order already delivered"}, status=status.HTTP_400_BAD_REQUEST)
            order.status = StatusChoices.DELIVERED
            order.save()
            return Response({"message": "Order marked as delivered"}, status=status.HTTP_200_OK)

        elif action == 'cancel_order':
            if order.status in [StatusChoices.DELIVERED, StatusChoices.CANCELLED]:
                return Response({"error": "Order cannot be canceled"}, status=status.HTTP_400_BAD_REQUEST)
            order.status = StatusChoices.CANCELLED
            order.save()
            return Response({"message": "Order canceled successfully"}, status=status.HTTP_200_OK)

        return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)



class OrderFilterView(APIView):
    #permission_classes = [IsAuthenticated]

    """
    Filter orders by status. Accessible at: /orders/filter_by_status/?status=PENDING
    """

    def get(self, request):
        status_param = request.query_params.get('status')
        if not status_param:
            return Response({"error": "Status query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        orders = Order.objects.filter(status=status_param.upper())
        if orders.exists():
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "No orders found with the given status"}, status=status.HTTP_404_NOT_FOUND)



class DeliveryListCreate(APIView):
    #permission_classes = [IsAuthenticated]

    def get(self, request):
        deliveries = Delivery.objects.all()
        serializer = DeliverySerializer(deliveries, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DeliverySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeliveryDetail(APIView):
    #permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Delivery.objects.get(pk=pk)
        except Delivery.DoesNotExist:
            return None

    def get(self, request, pk):
        delivery = self.get_object(pk)
        if delivery is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = DeliverySerializer(delivery)
        return Response(serializer.data)

    def put(self, request, pk):
        delivery = self.get_object(pk)
        if delivery is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = DeliverySerializer(delivery, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        delivery = self.get_object(pk)
        if delivery is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        delivery.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PaymentListCreate(APIView):
    #permission_classes = [IsAuthenticated]

    def get(self, request):
        payments = Payment.objects.all()
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PaymentDetail(APIView):
    #permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Payment.objects.get(pk=pk)
        except Payment.DoesNotExist:
            return None

    def get(self, request, pk):
        payment = self.get_object(pk)
        if payment is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PaymentSerializer(payment)
        return Response(serializer.data)

    def put(self, request, pk):
        payment = self.get_object(pk)
        if payment is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PaymentSerializer(payment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        payment = self.get_object(pk)
        if payment is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        payment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)