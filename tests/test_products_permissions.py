from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from apps.products.models import Product


class ProductPermissionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user('tester', 'pass')
        self.p1 = Product.objects.create(name='Apple', sku='APL-001', price='0.50')

    def test_unauthenticated_cannot_create(self):
        payload = {'name': 'Orange', 'sku': 'ORG-001', 'price': '0.99'}
        res = self.client.post('/api/products/', payload, format='json')
        # DRF with default authentication may return 403 for session/CSRF
        self.assertIn(res.status_code, (401, 403))

    def test_authenticated_can_create(self):
        self.client.force_authenticate(user=self.user)
        payload = {'name': 'Orange', 'sku': 'ORG-001', 'price': '0.99'}
        res = self.client.post('/api/products/', payload, format='json')
        self.assertEqual(res.status_code, 201)

    def test_duplicate_sku_returns_400(self):
        self.client.force_authenticate(user=self.user)
        payload = {'name': 'Apple2', 'sku': 'APL-001', 'price': '1.00'}
        res = self.client.post('/api/products/', payload, format='json')
        self.assertEqual(res.status_code, 400)

    def test_missing_field_returns_400(self):
        self.client.force_authenticate(user=self.user)
        payload = {'sku': 'NEW-001', 'price': '1.00'}
        res = self.client.post('/api/products/', payload, format='json')
        self.assertEqual(res.status_code, 400)

    def test_empty_list(self):
        Product.objects.all().delete()
        res = self.client.get('/api/products/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json(), [])
