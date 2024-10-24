from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from posts_app.models import Post, Comment

class APITests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user_model = get_user_model()

        # URL for endpoints
        self.create_post_url = reverse('api:create_post')
        self.create_comment_url = reverse('api:create_comment')
        self.analytics_url = reverse('api:comments_daily_breakdown')
        self.login_url = reverse('api:login_user')
        self.register_url = reverse('api:register_user')
        self.set_autoreply_url = reverse('api:set_autoreply')

        # Register user via api
        register_payload = {
            "username": "testuser",
            "password": "testpassword"
        }
        register_response = self.client.post(self.register_url, register_payload, content_type='application/json')
        self.user = self.user_model.objects.get(username='testuser')
        self.assertEqual(register_response.status_code, 200)

        # Login user for fetching JWT
        login_payload = {
            "username": "testuser",
            "password": "testpassword"
        }
        login_response = self.client.post(self.login_url, login_payload, content_type='application/json')
        self.assertEqual(login_response.status_code, 200)
        self.token = login_response.json().get('access_token')

    def test_register_user(self):
        payload = {
            "username": "newuser",
            "password": "testpassword"
        }
        response = self.client.post(self.register_url, payload, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('id', response.json())
        self.assertIn('username', response.json())

    def test_login_user(self):
        payload = {
            "username": "testuser",
            "password": "testpassword"
        }
        response = self.client.post(self.login_url, payload, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.json())

    def test_create_post(self):
        self.client.defaults['HTTP_AUTHORIZATION'] = 'Bearer ' + self.token

        payload = {
            "title": "Test Post",
            "content": "This is a test post"
        }
        response = self.client.post(self.create_post_url, payload, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('id', response.json())
        self.assertIn('blocked', response.json())

    def test_create_comment(self):
        post = Post.objects.create(author=self.user, title="Test Post", content="Test content", blocked=False)

        self.client.defaults['HTTP_AUTHORIZATION'] = 'Bearer ' + self.token

        payload = {
            "post_id": post.id,
            "content": "This is a test comment"
        }
        response = self.client.post(self.create_comment_url, payload, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('id', response.json())
        self.assertIn('blocked', response.json())

    def test_comment_analytics(self):
        test_post, _ = Post.objects.get_or_create(author=self.user, title="Test Post", content="Test content", blocked=False)

        Comment.objects.create(author=self.user, post=test_post, content="Comment 1", blocked=False)
        Comment.objects.create(author=self.user, post=test_post, content="Comment 2", blocked=True)

        params = {
            'date_from': '2022-01-01',
            'date_to': '2022-12-31'
        }
        response = self.client.get(self.analytics_url, params)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_set_autoreply(self):
        self.client.defaults['HTTP_AUTHORIZATION'] = 'Bearer ' + self.token

        payload = {
            "autoreply": True,
            "autoreply_delay": 5
        }
        response = self.client.post(self.set_autoreply_url, payload, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json())
