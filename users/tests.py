from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from users.models import details


class UserFlowTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username='boss', password='pass12345')
        details.objects.create(user=self.admin, role='admin')

    def test_admin_user_list(self):
        self.client.post(reverse('VTessential:login'), {'username': 'boss', 'password': 'pass12345'})
        response = self.client.get(reverse('user:user_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'boss')
