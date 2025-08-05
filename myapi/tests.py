from itertools import product
from os import name
from urllib import response
from django.test import TestCase
from .models import Order, Product , User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# Create your tests here.
class ProductAPITestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(username='admin', password='adminpass')
        self.normal_user = User.objects.create_user(username='user', password='userpass')
        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            price=9.99,
            stock=10
        )
        self.url = reverse('product-detail',kwargs={'product_id':self.product.pk})

    def test_get_product(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.product.name)

    def test_unauthorized_update_product(self):
        data = {'name':'Updated product'}
        response = self.client.put(self.url,data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_unauthorized_delete_product(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# class UserOrderTestCase(TestCase):
#     def setUp(self):
#         user1 = User.objects.create_user(username='user1', password='test')
#         user2 = User.objects.create_user(username='user2', password='test')
#         Order.objects.create(user=user1)
#         Order.objects.create(user=user1)
#         Order.objects.create(user=user2)
#         Order.objects.create(user=user2)
#     def test_user_order_retrive_only_auth_user_order(self):
#         user = User.objects.get(username = 'user2')
#         self.client.force_login(user)
#         response = self.client.get(reverse('user-orders'))

#         assert response.status_code == status.HTTP_200_OK 
#         orders = response.json()
#         print(orders)
#         self.assertTrue(all(order['user'] == user.id for order in orders))

#     def test_user_order_retrive_unauth_user_order(self):
#         response = self.client.get(reverse('user-orders'))
#         self.assertEqual(response.status_code , status.HTTP_401_UNAUTHORIZED)