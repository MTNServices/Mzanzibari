from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from apps.products.models import Product
from apps.sales.models import Sale, SaleItem
from decimal import Decimal
from datetime import datetime

User = get_user_model()


class SaleModelTest(TestCase):
    """Test Sale model"""
    
    def setUp(self):
        self.user = User.objects.create_user(username='cashier', password='pass123')
        self.product = Product.objects.create(
            name="Test Product",
            sku="TEST001",
            price=Decimal("50.00")
        )
    
    def test_create_sale(self):
        sale = Sale.objects.create(
            user=self.user,
            total_amount=Decimal("100.00"),
            payment_method='cash'
        )
        self.assertTrue(sale.sale_number.startswith('SALE-'))
        self.assertEqual(sale.payment_method, 'cash')
    
    def test_sale_auto_numbering(self):
        sale1 = Sale.objects.create(
            user=self.user,
            total_amount=Decimal("100.00"),
            payment_method='cash'
        )
        sale2 = Sale.objects.create(
            user=self.user,
            total_amount=Decimal("150.00"),
            payment_method='card'
        )
        self.assertNotEqual(sale1.sale_number, sale2.sale_number)


class SaleItemModelTest(TestCase):
    """Test SaleItem model"""
    
    def setUp(self):
        self.user = User.objects.create_user(username='cashier', password='pass123')
        self.product = Product.objects.create(
            name="Test Product",
            sku="TEST001",
            price=Decimal("50.00")
        )
        self.sale = Sale.objects.create(
            user=self.user,
            total_amount=Decimal("500.00"),
            payment_method='cash'
        )
    
    def test_create_sale_item(self):
        item = SaleItem.objects.create(
            sale=self.sale,
            product=self.product,
            quantity=5,
            unit_price=Decimal("50.00")
        )
        self.assertEqual(item.quantity, 5)
        self.assertEqual(item.subtotal, Decimal("250.00"))
    
    def test_subtotal_auto_calculation(self):
        item = SaleItem.objects.create(
            sale=self.sale,
            product=self.product,
            quantity=3,
            unit_price=Decimal("25.00")
        )
        self.assertEqual(item.subtotal, Decimal("75.00"))


class SaleViewSetTest(TestCase):
    """Test Sale API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='cashier', password='pass123')
        self.product = Product.objects.create(
            name="Test Product",
            sku="TEST001",
            price=Decimal("50.00")
        )
    
    def test_list_sales(self):
        Sale.objects.create(
            user=self.user,
            total_amount=Decimal("100.00"),
            payment_method='cash'
        )
        response = self.client.get('/api/sales/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_create_sale_unauthenticated(self):
        data = {
            'total_amount': Decimal("100.00"),
            'payment_method': 'cash'
        }
        response = self.client.post('/api/sales/', data, format='json')
        self.assertIn(response.status_code, [401, 403])
    
    def test_create_sale_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'user': self.user.id,
            'total_amount': Decimal("200.00"),
            'payment_method': 'card',
            'items': []
        }
        response = self.client.post('/api/sales/', data, format='json')
        self.assertEqual(response.status_code, 201)
    
    def test_filter_sales_by_payment_method(self):
        Sale.objects.create(
            user=self.user,
            total_amount=Decimal("100.00"),
            payment_method='cash'
        )
        Sale.objects.create(
            user=self.user,
            total_amount=Decimal("200.00"),
            payment_method='card'
        )
        response = self.client.get('/api/sales/?payment_method=cash')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_daily_sales_action(self):
        today = datetime.now().strftime('%Y-%m-%d')
        Sale.objects.create(
            user=self.user,
            total_amount=Decimal("100.00"),
            payment_method='cash'
        )
        Sale.objects.create(
            user=self.user,
            total_amount=Decimal("150.00"),
            payment_method='cash'
        )
        response = self.client.get(f'/api/sales/daily_sales/?date={today}')
        self.assertEqual(response.status_code, 200)
    
    def test_total_by_method_action(self):
        Sale.objects.create(
            user=self.user,
            total_amount=Decimal("100.00"),
            payment_method='cash'
        )
        Sale.objects.create(
            user=self.user,
            total_amount=Decimal("150.00"),
            payment_method='card'
        )
        response = self.client.get('/api/sales/total_by_method/')
        self.assertEqual(response.status_code, 200)
