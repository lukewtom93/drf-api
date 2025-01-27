from django.contrib.auth.models import User
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase


class PostListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='luke', password='123')

    def test_can_list_posts(self):
        luke = User.objects.get(username='luke')
        Post.objects.create(owner=luke, title='title')
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))

    def test_logged_in_user_can_create_post(self):
        self.client.login(username='luke', password='123')
        response = self.client.post('/posts/', {'title': 'title'})
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logged_out_user_can_not_create_post(self):
        response = self.client.post('/posts/', {'title': 'title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PostDetailViewTests(APITestCase):
    def setUp(self):
        luke = User.objects.create_user(username='luke', password='123')
        james = User.objects.create_user(username='james', password='123')
        Post.objects.create(
            owner=luke, title='title a', content='lukes content'
        )
        Post.objects.create(
            owner=james, title='title b', content='james content'
        )

    def test_can_retrieve_post_using_valid_id(self):
        response = self.client.get('/posts/1/')
        self.assertEqual(response.data['title'], 'title a')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_fetch_post_by_invalid_id(self):
        response = self.client.get('/posts/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_post(self):
        self.client.login(username='luke', password='123')
        response = self.client.put('/posts/1/', {'title': 'new title'})
        post = Post.objects.filter(pk=1).first()
        self.assertEqual(post.title, 'new title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_other_users_posts(self):
        self.client.login(username='luke', password='123')
        response = self.client.put('/posts/2/', {'title': 'new title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
      

        

        