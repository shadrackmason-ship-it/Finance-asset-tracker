from django.test import TestCase, Client
from django.urls import reverse
from .models import User


class UserRegistrationTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_register_new_user(self):
        res = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })
        self.assertEqual(User.objects.filter(username='newuser').count(), 1)

    def test_register_redirects_to_dashboard(self):
        res = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })
        self.assertRedirects(res, reverse('dashboard'))

    def test_duplicate_username_rejected(self):
        User.objects.create_user(username='existing', password='Pass123!', email='e@test.com')
        res = self.client.post(reverse('register'), {
            'username': 'existing',
            'email': 'other@test.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })
        self.assertEqual(User.objects.filter(username='existing').count(), 1)


class UserLoginTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='mason', password='TestPass123!', email='mason@test.com')

    def test_login_with_username(self):
        res = self.client.post(reverse('login'), {
            'username': 'mason',
            'password': 'TestPass123!',
        })
        self.assertRedirects(res, reverse('dashboard'))

    def test_login_with_wrong_password(self):
        res = self.client.post(reverse('login'), {
            'username': 'mason',
            'password': 'wrongpassword',
        })
        self.assertEqual(res.status_code, 200)
        self.assertFalse(res.wsgi_request.user.is_authenticated)

    def test_dashboard_requires_login(self):
        res = self.client.get(reverse('dashboard'))
        self.assertRedirects(res, f"{reverse('login')}?next={reverse('dashboard')}")

    def test_authenticated_user_can_access_dashboard(self):
        self.client.force_login(self.user)
        res = self.client.get(reverse('dashboard'))
        self.assertEqual(res.status_code, 200)


class UserProfileTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='mason', password='TestPass123!', email='mason@test.com')
        self.client.force_login(self.user)

    def test_profile_page_loads(self):
        res = self.client.get(reverse('profile'))
        self.assertEqual(res.status_code, 200)

    def test_update_currency_preference(self):
        res = self.client.post(reverse('profile'), {
            'first_name': '',
            'last_name': '',
            'email': 'mason@test.com',
            'preferred_currency': 'NGN',
            'timezone': 'Africa/Lagos',
            'country': 'Nigeria',
        })
        self.user.refresh_from_db()
        self.assertEqual(self.user.preferred_currency, 'NGN')
