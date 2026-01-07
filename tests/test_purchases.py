from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from apps.products.models import Product
from apps.purchases.models import Supplier, Purchase, PurchaseItem
from decimal import Decimal

User = get_user_model()


class SupplierModelTest(TestCase):
    """Test Supplier model"""
    
    def test_create_supplier(self):
        supplier = Supplier.objects.create(
            name="ABC Supplies",
            email="abc@example.com",
            phone="1234567890"
        )
        self.assertEqual(supplier.name, "ABC Supplies")
        self.assertEqual(supplier.email, "abc@example.com")


class PurchaseModelTest(TestCase):
    """Test Purchase model"""
    
    def setUp(self):
        self.user = User.objects.create_user(username='buyer', password='pass123')
        self.supplier = Supplier.objects.create(
            name="ABC Supplies",
            email="abc@example.com"
        )
    
    def test_create_purchase(self):
        purchase = Purchase.objects.create(
            supplier=self.supplier,
            user=self.user,
            total_amount=Decimal("500.00"),
            status='pending'
        )
        self.assertTrue(purchase.purchase_number.startswith('PO-'))
        self.assertEqual(purchase.status, 'pending')
    
    def test_purchase_auto_numbering(self):
        p1 = Purchase.objects.create(
            supplier=self.supplier,
            user=self.user,
            total_amount=Decimal("100.00")
        )
        p2 = Purchase.objects.create(
            supplier=self.supplier,
            user=self.user,
            total_amount=Decimal("200.00")
        )
        self.assertNotEqual(p1.purchase_number, p2.purchase_number)


class PurchaseItemModelTest(TestCase):
    """Test PurchaseItem model"""
    
    def setUp(self):
        self.user = User.objects.create_user(username='buyer', password='pass123')
        self.supplier = Supplier.objects.create(name="ABC Supplies")
        self.product = Product.objects.create(
            name="Test Product",
            sku="TEST001",
            price=Decimal("50.00")
        )
        self.purchase = Purchase.objects.create(
            supplier=self.supplier,
            user=self.user,
            total_amount=Decimal("1000.00")
        )
    
    def test_create_purchase_item(self):
        item = PurchaseItem.objects.create(
            purchase=self.purchase,
            product=self.product,
            quantity=10,
            unit_price=Decimal("45.00")
        )
        self.assertEqual(item.quantity, 10)
        self.assertEqual(item.subtotal, Decimal("450.00"))
    
    def test_subtotal_auto_calculation(self):
        item = PurchaseItem.objects.create(
            purchase=self.purchase,
            product=self.product,
            quantity=5,
            unit_price=Decimal("30.00")
        )
        self.assertEqual(item.subtotal, Decimal("150.00"))


class SupplierViewSetTest(TestCase):
    """Test Supplier API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='buyer', password='pass123')
    
    def test_list_suppliers(self):
        Supplier.objects.create(name="ABC Supplies")
        response = self.client.get('/api/suppliers/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_create_supplier_unauthenticated(self):
        data = {'name': 'XYZ Corp', 'email': 'xyz@example.com'}
        response = self.client.post('/api/suppliers/', data, format='json')
        self.assertIn(response.status_code, [401, 403])
    
    def test_create_supplier_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {'name': 'XYZ Corp', 'email': 'xyz@example.com', 'phone': '9876543210'}
        response = self.client.post('/api/suppliers/', data, format='json')
        self.assertEqual(response.status_code, 201)
    
    def test_retrieve_supplier(self):
        supplier = Supplier.objects.create(name="ABC Supplies")
        response = self.client.get(f'/api/suppliers/{supplier.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], "ABC Supplies")


class PurchaseViewSetTest(TestCase):
    """Test Purchase API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='buyer', password='pass123')
        self.supplier = Supplier.objects.create(name="ABC Supplies")
        self.product = Product.objects.create(
            name="Test Product",
            sku="TEST001",
            price=Decimal("50.00")
        )
    
    def test_list_purchases(self):
        Purchase.objects.create(
            supplier=self.supplier,
            user=self.user,
            total_amount=Decimal("500.00")
        )
        response = self.client.get('/api/purchases/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_create_purchase_unauthenticated(self):
        data = {
            'supplier': self.supplier.id,
            'total_amount': Decimal("500.00"),
            'status': 'pending'
        }
        response = self.client.post('/api/purchases/', data, format='json')
        self.assertIn(response.status_code, [401, 403])
    
    def test_create_purchase_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'supplier': self.supplier.id,
            'user': self.user.id,
            'total_amount': Decimal("1000.00"),
            'status': 'pending',
            'items': []
        }
        response = self.client.post('/api/purchases/', data, format='json')
        self.assertEqual(response.status_code, 201)
    
    def test_filter_by_status(self):
        Purchase.objects.create(
            supplier=self.supplier,
            user=self.user,
            total_amount=Decimal("500.00"),
            status='pending'
        )
        Purchase.objects.create(
            supplier=self.supplier,
            user=self.user,
            total_amount=Decimal("700.00"),
            status='received'
        )
        response = self.client.get('/api/purchases/?status=pending')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_filter_by_supplier(self):
        supplier2 = Supplier.objects.create(name="XYZ Corp")
        Purchase.objects.create(
            supplier=self.supplier,
            user=self.user,
            total_amount=Decimal("500.00")
        )
        Purchase.objects.create(
            supplier=supplier2,
            user=self.user,
            total_amount=Decimal("700.00")
        )
        response = self.client.get(f'/api/purchases/?supplier={self.supplier.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
