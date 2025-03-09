from django.test import TestCase
from django.contrib.auth import get_user_model
from foodapp.models import Customer, DeliveryPerson, Order, OrderItem, Delivery, Payment, Restaurant, MenuItem
from datetime import datetime
from django.db import models

class UserModelTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='password123',
            phone_number='1234567890',
            age=25,
            email='testuser@example.com',
            address='123 Test St'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.phone_number, '1234567890')
        self.assertEqual(self.user.age, 25)
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertEqual(self.user.address, '123 Test St')

    def test_user_str(self):
        self.assertEqual(str(self.user), 'testuser')


class RestaurantModelTest(TestCase):

    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            address='456 Test Ave',
            contact_number='0987654321',
            opening_time=datetime.now().time(),
            closing_time=datetime.now().time(),
            is_active=True
        )

    def test_restaurant_creation(self):
        self.assertEqual(self.restaurant.name, 'Test Restaurant')
        self.assertEqual(self.restaurant.address, '456 Test Ave')
        self.assertEqual(self.restaurant.contact_number, '0987654321')
        self.assertTrue(self.restaurant.is_active)

    def test_restaurant_str(self):
        self.assertEqual(str(self.restaurant), 'Test Restaurant')


class MenuItemModelTest(TestCase):

    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            address='456 Test Ave',
            contact_number='0987654321',
            opening_time=datetime.now().time(),
            closing_time=datetime.now().time(),
            is_active=True
        )
        self.menu_item = MenuItem.objects.create(
            restaurant=self.restaurant,
            name='Test Menu Item',
            description='Test Description',
            price=9.99
        )

    def test_menu_item_creation(self):
        self.assertEqual(self.menu_item.restaurant, self.restaurant)
        self.assertEqual(self.menu_item.name, 'Test Menu Item')
        self.assertEqual(self.menu_item.description, 'Test Description')
        self.assertEqual(self.menu_item.price, 9.99)

    def test_menu_item_str(self):
        self.assertEqual(str(self.menu_item), 'Test Menu Item')


class CustomerModelTest(TestCase):

    def setUp(self):
        self.customer = Customer.objects.create(
            name='Test Customer',
            phone_number='12345678901',
            current_location='Test Location'
        )

    def test_customer_creation(self):
        self.assertEqual(self.customer.name, 'Test Customer')
        self.assertEqual(self.customer.phone_number, '12345678901')
        self.assertEqual(self.customer.current_location, 'Test Location')

    def test_customer_str(self):
        self.assertEqual(str(self.customer), 'Test Customer')


class DeliveryPersonModelTest(TestCase):

    def setUp(self):
        self.delivery_person = DeliveryPerson.objects.create(
            name='Test Delivery Person',
            phone_number='12345678901',
            vehicle_number='ABC123'
        )

    def test_delivery_person_creation(self):
        self.assertEqual(self.delivery_person.name, 'Test Delivery Person')
        self.assertEqual(self.delivery_person.phone_number, '12345678901')
        self.assertEqual(self.delivery_person.vehicle_number, 'ABC123')

    def test_delivery_person_str(self):
        self.assertEqual(str(self.delivery_person), 'Test Delivery Person')


class OrderModelTest(TestCase):

    def setUp(self):
        self.customer = Customer.objects.create(
            name='Test Customer',
            phone_number='12345678901',
            current_location='Test Location'
        )
        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            address='Test Address',
            contact_number='12345678901',
            opening_time='10:00:00',
            closing_time='22:00:00',
            is_active=True
        )
        self.order = Order.objects.create(
            customer=self.customer,
            restaurant=self.restaurant,
            status='Pending'
        )

    def test_order_creation(self):
        self.assertEqual(self.order.customer, self.customer)
        self.assertEqual(self.order.restaurant, self.restaurant)
        self.assertEqual(self.order.status, 'Pending')


class OrderItemModelTest(TestCase):

    def setUp(self):
        self.customer = Customer.objects.create(
            name='Test Customer',
            phone_number='12345678901',
            current_location='Test Location'
        )
        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            address='Test Address',
            contact_number='12345678901',
            opening_time='10:00:00',
            closing_time='22:00:00',
            is_active=True
        )
        self.menu_item = MenuItem.objects.create(
            restaurant=self.restaurant,
            name='Test Menu Item',
            description='Test Description',
            price=9.99
        )
        self.order = Order.objects.create(
            customer=self.customer,
            restaurant=self.restaurant,
            status='Pending'
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            menu_item=self.menu_item,
            quantity=2
        )

    def test_order_item_creation(self):
        self.assertEqual(self.order_item.order, self.order)
        self.assertEqual(self.order_item.menu_item, self.menu_item)
        self.assertEqual(self.order_item.quantity, 2)


class DeliveryModelTest(TestCase):

    def setUp(self):
        self.customer = Customer.objects.create(
            name='Test Customer',
            phone_number='12345678901',
            current_location='Test Location'
        )
        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            address='Test Address',
            contact_number='12345678901',
            opening_time='10:00:00',
            closing_time='22:00:00',
            is_active=True
        )
        self.delivery_person = DeliveryPerson.objects.create(
            name='Test Delivery Person',
            phone_number='12345678901',
            vehicle_number='ABC123'
        )
        self.order = Order.objects.create(
            customer=self.customer,
            restaurant=self.restaurant,
            status='Pending'
        )
        self.delivery = Delivery.objects.create(
            order=self.order,
            delivery_person=self.delivery_person,
            delivery_address='Test Address',
            estimated_delivery_time=30,
            actual_delivery_time=25
        )

    def test_delivery_creation(self):
        self.assertEqual(self.delivery.order, self.order)
        self.assertEqual(self.delivery.delivery_person, self.delivery_person)
        self.assertEqual(self.delivery.delivery_address, 'Test Address')
        self.assertEqual(self.delivery.estimated_delivery_time, 30)
        self.assertEqual(self.delivery.actual_delivery_time, 25)

    def test_delivery_str(self):
        self.assertEqual(str(self.delivery), '25')


class PaymentModelTest(TestCase):

    def setUp(self):
        self.customer = Customer.objects.create(
            name='Test Customer',
            phone_number='12345678901',
            current_location='Test Location'
        )
        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            address='Test Address',
            contact_number='12345678901',
            opening_time='10:00:00',
            closing_time='22:00:00',
            is_active=True
        )
        self.order = Order.objects.create(
            customer=self.customer,
            restaurant=self.restaurant,
            status='Pending'
        )
        self.payment = Payment.objects.create(
            order=self.order,
            amount=100.00,
            payment_method='Credit Card',
            payment_status='Completed'
        )

    def test_payment_creation(self):
        self.assertEqual(self.payment.order, self.order)
        self.assertEqual(self.payment.amount, 100.00)
        self.assertEqual(self.payment.payment_method, 'Credit Card')
        self.assertEqual(self.payment.payment_status, 'Completed')