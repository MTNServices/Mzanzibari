from django.test import TestCase
from rest_framework.test import APIClient
from apps.products.models import Product
from apps.products.serializers import ProductSerializer


class ProductTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        from django.contrib.auth import get_user_model
        self.user = get_user_model().objects.create_user('tester2', 'pass')
        self.p1 = Product.objects.create(name='Apple', sku='APL-001', price='0.50')

    def test_product_str(self):
        self.assertEqual(str(self.p1), 'Apple (APL-001)')

    def test_serializer(self):
        data = ProductSerializer(self.p1).data
        self.assertEqual(data['sku'], 'APL-001')

    def test_list_view(self):
        res = self.client.get('/api/products/')
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json(), list)

    def test_create_view(self):
        self.client.force_authenticate(user=self.user)
        payload = {'name': 'Banana', 'sku': 'BNA-001', 'price': '1.20'}
        res = self.client.post('/api/products/', payload, format='json')
        self.assertEqual(res.status_code, 201)
        self.assertTrue(Product.objects.filter(sku='BNA-001').exists())
