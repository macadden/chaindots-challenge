from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from apps.post.models import Post, Comment
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class PostTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='user@example.com',
            password='password',
            username='user'
        )
        self.token = RefreshToken.for_user(self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {self.token}')

        self.post = Post.objects.create(
            author=self.user,
            content='This is a test post'
        )
        self.comment = Comment.objects.create(
            author=self.user,
            post=self.post,
            content='This is a test comment'
        )

    def test_create_post(self):
        url = reverse('post-list')  # Actualiza según el nombre de la URL
        data = {
            'content': 'New post content'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)
        self.assertEqual(Post.objects.get(content='New post content').content, 'New post content')

    def test_get_posts(self):
        url = reverse('post-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_post_details(self):
        url = reverse('post-detail', args=[self.post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], self.post.content)
        self.assertEqual(len(response.data['comments']), 1)

    def test_get_post_comments(self):
        url = reverse('post-comments', args=[self.post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_add_comment_to_post(self):
        url = reverse('post-comments', args=[self.post.id])
        data = {
            'content': 'Another comment'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)
        self.assertEqual(Comment.objects.get(content='Another comment').content, 'Another comment')