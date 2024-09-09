from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            email='user1@example.com',
            password='password',
            username='user1'
        )
        self.user2 = User.objects.create_user(
            email='user2@example.com',
            password='password',
            username='user2'
        )
        self.token = RefreshToken.for_user(self.user1).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {self.token}')

    def test_create_user(self):
        url = reverse('user-list')  # Actualiza según el nombre de la URL
        data = {
            'email': 'newuser@example.com',
            'password': 'password',
            'username': 'newuser'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(User.objects.get(email='newuser@example.com').username, 'newuser')

    def test_get_users(self):
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_user_details(self):
        url = reverse('user-detail', args=[self.user1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user1.email)

    def test_follow_user(self):
        url = reverse('user-follow', args=[self.user1.id, self.user2.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIn(self.user2, self.user1.following.all())
        self.assertIn(self.user1, self.user2.followers.all())