from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from users.models import details
from VT.models import newitem


class CatalogSmokeTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.shirt = newitem.objects.create(
            title='Red Printed Tshirt by HRX',
            rating=4,
            type='T-shirt',
            price=35,
            description='Tshirt',
            cart_items=0,
        )
        self.shoes = newitem.objects.create(
            title='HRX Sports Shoes',
            rating=5,
            type='Shoes',
            price=35,
            description='Good Product',
            cart_items=0,
        )
        self.regular = User.objects.create_user(username='shopper', password='pass12345')
        details.objects.create(user=self.regular, role='regular')
        self.admin = User.objects.create_user(username='storeadmin', password='pass12345')
        details.objects.create(user=self.admin, role='admin')

    def test_home_renders_catalog(self):
        response = self.client.get(reverse('VTessential:home_page'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.shirt.title)

    def test_clothing_list_and_sort(self):
        listing = self.client.get(reverse('VTessential:list_page'))
        self.assertEqual(listing.status_code, 200)
        sorted_list = self.client.get(reverse('VTessential:sort'))
        self.assertEqual(sorted_list.status_code, 200)

    def test_item_detail(self):
        response = self.client.get(reverse('VTessential:item_detail', args=[self.shirt.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.shirt.title)

    def test_register_login_logout(self):
        register = self.client.post(
            reverse('user:register'),
            {
                'username': 'newbie',
                'password': 'pass12345',
                'first_name': 'New',
                'last_name': 'User',
                'email': 'new@example.com',
                'role': 'regular',
            },
        )
        self.assertEqual(register.status_code, 302)
        login = self.client.post(
            reverse('VTessential:login'),
            {'username': 'newbie', 'password': 'pass12345'},
        )
        self.assertEqual(login.status_code, 302)
        home = self.client.get(reverse('VTessential:home_page'))
        self.assertEqual(home.status_code, 200)
        self.assertEqual(self.client.session.get('username'), 'newbie')
        logout = self.client.get(reverse('VTessential:logout'))
        self.assertEqual(logout.status_code, 302)

    def test_cart_increments(self):
        response = self.client.post(reverse('VTessential:cart_item'), {'item_id': self.shirt.id})
        self.assertEqual(response.status_code, 200)
        self.shirt.refresh_from_db()
        self.assertEqual(self.shirt.cart_items, 1)

    def test_admin_add_product(self):
        self.client.post(
            reverse('VTessential:login'),
            {'username': 'storeadmin', 'password': 'pass12345'},
        )
        response = self.client.post(
            reverse('VTessential:admin_add'),
            {
                'product_name': 'Campus Hoodie',
                'product_type': 'T-shirt',
                'price': '40',
                'rating': '4',
                'description': 'Warm hoodie',
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(newitem.objects.filter(title='Campus Hoodie').exists())
