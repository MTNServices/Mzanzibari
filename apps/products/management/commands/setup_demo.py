from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.products.models import Product


class Command(BaseCommand):
    help = 'Set up demo data: superuser and sample products'

    def handle(self, *args, **options):
        User = get_user_model()

        # Create superuser if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@mzanzibari.local', 'password123')
            self.stdout.write(self.style.SUCCESS('✓ Created superuser: admin / password123'))
        else:
            self.stdout.write(self.style.WARNING('✓ Superuser admin already exists'))

        # Create sample products
        products = [
            {'name': 'Maize', 'sku': 'MZ-001', 'price': '150.00'},
            {'name': 'Beans', 'sku': 'BN-001', 'price': '200.00'},
            {'name': 'Wheat', 'sku': 'WH-001', 'price': '180.00'},
            {'name': 'Rice', 'sku': 'RC-001', 'price': '250.00'},
            {'name': 'Sorghum', 'sku': 'SG-001', 'price': '170.00'},
        ]

        for p in products:
            obj, created = Product.objects.get_or_create(
                sku=p['sku'],
                defaults={'name': p['name'], 'price': p['price']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created product: {obj.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'✓ Product already exists: {obj.name}'))

        self.stdout.write(self.style.SUCCESS('\n✓ Demo setup complete!'))
        self.stdout.write('\nAdmin URL: http://127.0.0.1:8000/admin/')
        self.stdout.write('API URL: http://127.0.0.1:8000/api/products/')
