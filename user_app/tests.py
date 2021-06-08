from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class RegisterTestCase(APITestCase):
    def test_register(self):
        data = {
            'username': 'testcase',
            'email': 'testcase@example.com',
            'password': 'Password@123',
            'password2': 'Password@123',
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LoginTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testcase', password='Password@123')

    def test_login(self):
        data = {
            'username': 'testcase',
            'password': 'Password@123',
        }
        response = self.client.post(reverse('token_obtain_pair'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
