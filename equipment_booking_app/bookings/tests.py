from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from bookings.models import LoginAttempt

class SecurityFeatureTests(TestCase):
    def setUp(self):
        self.csrf_client = Client(enforce_csrf_checks=True)
        self.client = Client()
        self.login_url = reverse('login')
        self.signup_url = reverse('signup')
        self.admin_url = '/admin-b4a939d29b7cda4b/'

    def test_csrf_protection_on_login(self):
        response = self.csrf_client.post(self.login_url, {
            'username': 'user',
            'password': 'pass'
        })
        self.assertEqual(response.status_code, 403)

    def test_password_strength_enforcement(self):
        weak_data = {
            'username': 'weakuser',
            'password1': '12345',
            'password2': '12345'
        }
        self.client.post(self.signup_url, weak_data)
        self.assertFalse(User.objects.filter(username='weakuser').exists())

    def test_login_lockout_after_failed_attempts(self):
        user = User.objects.create_user(username='lockuser', password='strongPass123')
        for _ in range(5):
            self.client.post(self.login_url, {
                'username': 'lockuser',
                'password': 'wrong'
            })
        attempt = LoginAttempt.objects.get(user=user)
        self.assertIsNotNone(attempt.lockout_until)
        self.assertGreater(attempt.lockout_until, timezone.now())

    def test_regular_user_cannot_access_admin(self):
        User.objects.create_user(username='regular', password='test1325')
        self.client.login(username='regular', password='test1325')
        response = self.client.get(self.admin_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_admin_access_to_hidden_admin_url(self):
        User.objects.create_superuser(username='admin', password='test1325', email='admin@example.com')
        self.client.login(username='admin', password='test1325')
        response = self.client.get(self.admin_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Site administration')

