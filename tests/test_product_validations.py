from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from apps.products.models import Product


class ProductValidationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user('validator', 'pass')

    def test_model_rejects_negative_price(self):
        p = Product(name='Bad', sku='BAD-001', price='-1.00')
        with self.assertRaises(ValidationError):
            p.full_clean()

    def test_api_rejects_negative_price(self):
        self.client.force_authenticate(user=self.user)
        payload = {'name': 'Bad', 'sku': 'BAD-001', 'price': '-1.00'}
        res = self.client.post('/api/products/', payload, format='json')
        self.assertEqual(res.status_code, 400)
        self.assertIn('price', res.json())