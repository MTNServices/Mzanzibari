import os
import django

# Ensure Django settings are available for all tests
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
