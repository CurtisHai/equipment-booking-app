from django.test import TestCase
from django.contrib.auth.models import User
from django.middleware.csrf import get_token

class BookingAppTests(TestCase):
    def setUp(self):
        self.reg_user = User.objects.create_user(username='testingreg', password='test1325')
        self.admin_user = User.objects.create_superuser(username='testing', password='test1325', email='admin@example.com')

    def test_login_lockout_after_five_failures(self):
        """After 5 failed attempts the account should be locked."""
        login_url = '/login/'
        for _ in range(5):
            self.client.post(login_url, {'username': 'testingreg', 'password': 'wrong'})
        response = self.client.post(login_url, {'username': 'testingreg', 'password': 'wrong'})
        self.assertContains(response, 'Account locked', status_code=200)

    def test_admin_panel_access_control(self):
        admin_url = '/admin-b4a939d29b7cda4b/'
        # admin user should have access
        self.client.login(username='testing', password='test1325')
        admin_response = self.client.get(admin_url)
        self.assertEqual(admin_response.status_code, 200)
        self.client.logout()
        # regular user should be redirected or forbidden
        self.client.login(username='testingreg', password='test1325')
        reg_response = self.client.get(admin_url)
        self.assertIn(reg_response.status_code, [302, 403])

    def test_successful_booking_form_submission(self):
        form_url = '/bookings/form/'
        submit_url = '/bookings/submit/'
        # Fetch CSRF token
        self.client.login(username='testingreg', password='test1325')
        get_response = self.client.get(form_url)
        token_cookie = self.client.cookies.get('csrftoken')
        csrf_token = token_cookie.value if token_cookie else get_token(get_response.wsgi_request)
        post_data = {
            'name': 'Test Name',
            'message': 'Test message',
            'csrfmiddlewaretoken': csrf_token,
        }
        post_response = self.client.post(submit_url, post_data)
        self.assertIn(post_response.status_code, [200, 302])
