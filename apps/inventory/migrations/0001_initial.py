# Generated initial migration for inventory
from django.db import migrations, models
import django.core.validators
import django.db.models.deletion

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_on_hand', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('reorder_level', models.IntegerField(default=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('last_counted', models.DateTimeField(auto_now=True)),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='stock', to='products.product')),
            ],
        ),
        migrations.CreateModel(
            name='StockMovement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movement_type', models.CharField(choices=[('in', 'Stock In'), ('out', 'Stock Out'), ('adjustment', 'Adjustment')], max_length=20)),
                ('quantity', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('reason', models.CharField(blank=True, max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movements', to='inventory.stocklevel')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
