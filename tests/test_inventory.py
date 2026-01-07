from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from apps.products.models import Product
from apps.inventory.models import StockLevel, StockMovement
from decimal import Decimal

User = get_user_model()


class StockLevelModelTest(TestCase):
    """Test StockLevel model"""
    
    def setUp(self):
        self.product = Product.objects.create(
            name="Test Product",
            sku="TEST001",
            price=Decimal("50.00")
        )
    
    def test_create_stock_level(self):
        stock = StockLevel.objects.create(
            product=self.product,
            quantity_on_hand=100,
            reorder_level=20
        )
        self.assertEqual(stock.quantity_on_hand, 100)
        self.assertEqual(stock.reorder_level, 20)
    
    def test_needs_reorder_property(self):
        stock = StockLevel.objects.create(
            product=self.product,
            quantity_on_hand=10,
            reorder_level=20
        )
        self.assertTrue(stock.needs_reorder)
    
    def test_not_needs_reorder_property(self):
        stock = StockLevel.objects.create(
            product=self.product,
            quantity_on_hand=100,
            reorder_level=20
        )
        self.assertFalse(stock.needs_reorder)


class StockMovementModelTest(TestCase):
    """Test StockMovement model"""
    
    def setUp(self):
        self.product = Product.objects.create(
            name="Test Product",
            sku="TEST001",
            price=Decimal("50.00")
        )
        self.stock = StockLevel.objects.create(
            product=self.product,
            quantity_on_hand=100,
            reorder_level=20
        )
    
    def test_create_stock_in_movement(self):
        movement = StockMovement.objects.create(
            stock=self.stock,
            movement_type='in',
            quantity=50,
            reason="New shipment"
        )
        self.assertEqual(movement.movement_type, 'in')
        self.assertEqual(movement.quantity, 50)
    
    def test_create_stock_out_movement(self):
        movement = StockMovement.objects.create(
            stock=self.stock,
            movement_type='out',
            quantity=10,
            reason="Sale"
        )
        self.assertEqual(movement.movement_type, 'out')
        self.assertEqual(movement.quantity, 10)
    
    def test_movement_ordering(self):
        m1 = StockMovement.objects.create(
            stock=self.stock,
            movement_type='in',
            quantity=50
        )
        m2 = StockMovement.objects.create(
            stock=self.stock,
            movement_type='out',
            quantity=10
        )
        movements = StockMovement.objects.all()
        self.assertEqual(movements[0].id, m2.id)  # Latest first


class StockLevelViewSetTest(TestCase):
    """Test StockLevel API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.product = Product.objects.create(
            name="Test Product",
            sku="TEST001",
            price=Decimal("50.00")
        )
        self.stock = StockLevel.objects.create(
            product=self.product,
            quantity_on_hand=100,
            reorder_level=20
        )
    
    def test_list_stock_levels(self):
        response = self.client.get('/api/stock-levels/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_retrieve_stock_level(self):
        response = self.client.get(f'/api/stock-levels/{self.stock.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['quantity_on_hand'], 100)
    
    def test_create_stock_level_unauthenticated(self):
        data = {
            'product': self.product.id,
            'quantity_on_hand': 50,
            'reorder_level': 10
        }
        response = self.client.post('/api/stock-levels/', data, format='json')
        self.assertIn(response.status_code, [401, 403])
    
    def test_create_stock_level_authenticated(self):
        self.client.force_authenticate(user=self.user)
        product2 = Product.objects.create(
            name="Test Product 2",
            sku="TEST002",
            price=Decimal("60.00")
        )
        data = {
            'product': product2.id,
            'quantity_on_hand': 50,
            'reorder_level': 10
        }
        response = self.client.post('/api/stock-levels/', data, format='json')
        self.assertEqual(response.status_code, 201)
    
    def test_filter_stock_levels(self):
        response = self.client.get('/api/stock-levels/?quantity_on_hand=100')
        self.assertEqual(response.status_code, 200)


class StockMovementViewSetTest(TestCase):
    """Test StockMovement API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.product = Product.objects.create(
            name="Test Product",
            sku="TEST001",
            price=Decimal("50.00")
        )
        self.stock = StockLevel.objects.create(
            product=self.product,
            quantity_on_hand=100,
            reorder_level=20
        )
    
    def test_list_movements(self):
        StockMovement.objects.create(
            stock=self.stock,
            movement_type='in',
            quantity=50
        )
        response = self.client.get('/api/stock-movements/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_create_movement_unauthorized(self):
        """StockMovement is read-only"""
        data = {
            'stock': self.stock.id,
            'movement_type': 'in',
            'quantity': 50
        }
        response = self.client.post('/api/stock-movements/', data, format='json')
        self.assertIn(response.status_code, [401, 403, 405])
    
    def test_filter_by_movement_type(self):
        StockMovement.objects.create(
            stock=self.stock,
            movement_type='in',
            quantity=50
        )
        StockMovement.objects.create(
            stock=self.stock,
            movement_type='out',
            quantity=10
        )
        response = self.client.get('/api/stock-movements/?movement_type=in')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
