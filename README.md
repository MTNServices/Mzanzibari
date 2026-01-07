# Mzanzibari POS System

A fully functional Django REST Framework-based Point of Sale system with comprehensive test coverage, permissions, and validation.

## Features

- ✅ **Django 4.0+** with REST Framework
- ✅ **Product Management API** with authentication & validation
- ✅ **Django Admin Interface** for managing products
- ✅ **13 Comprehensive Tests** (models, serializers, views, permissions, validation)
- ✅ **DRF Permissions** (GET open, POST requires authentication)
- ✅ **Price Validation** (non-negative prices enforced at model & serializer level)
- ✅ **Sample Data** (5 agricultural products pre-loaded)

## Quick Start (Testing Locally)

### 1. Clone & Setup

```bash
git clone https://github.com/MTNServices/Mzanzibari.git
cd Mzanzibari
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
python manage.py migrate
python manage.py setup_demo
```

### 2. Run Tests

```bash
python manage.py test -v2
```

**Expected Output:** `Ran 13 tests in ~2s - OK`

Tests cover:
- Product model validation
- Serializer validation (negative prices)
- API permissions (authenticated vs anonymous)
- Edge cases (duplicate SKU, missing fields, empty list)

### 3. Start Dev Server

```bash
python manage.py runserver 8000
```

### 4. Test Endpoints

**GET Products** (anonymous, no auth required):
```bash
curl http://127.0.0.1:8000/api/products/
```

**POST Product** (requires authentication):
```bash
curl -X POST http://127.0.0.1:8000/api/products/ \
  -H "Content-Type: application/json" \
  -u admin:password123 \
  -d '{"name":"Cassava","sku":"CS-001","price":"120.00"}'
```

**Admin Dashboard**:
- Visit http://127.0.0.1:8000/admin/
- Login: `admin` / `password123`
- Manage products, view audit trail

## Project Structure

```
mzanzibari_pos/
├── config/              # Django settings & WSGI
├── apps/
│   ├── products/        # Product model, API, admin
│   ├── inventory/       # (scaffolded)
│   ├── sales/           # (scaffolded)
│   ├── purchases/       # (scaffolded)
│   └── ...
├── tests/               # 13 comprehensive tests
├── templates/           # HTML templates
├── static/              # CSS, JS, images
├── manage.py
└── requirements.txt
```

## Test Coverage

| Test | File | Status |
|------|------|--------|
| Project structure validation | `tests/test_project.py` | ✅ 2/2 pass |
| Product models & serializers | `tests/test_products.py` | ✅ 4/4 pass |
| API permissions | `tests/test_products_permissions.py` | ✅ 5/5 pass |
| Price validation | `tests/test_product_validations.py` | ✅ 2/2 pass |
| **Total** | | **✅ 13/13 pass** |

## API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/products/` | ❌ No | List all products |
| POST | `/api/products/` | ✅ Yes | Create new product |
| GET | `/admin/` | ✅ Yes | Django admin panel |

## Authentication

- **Type:** Session-based (Django default)
- **Default User:** `admin` / `password123` (created by `setup_demo`)
- **Change Password:** Visit `/admin/` and update profile

## Troubleshooting

**"Database file not found"**
```bash
python manage.py migrate
```

**"No such table: products_product"**
```bash
python manage.py migrate
```

**"Cannot POST product"**
- Ensure you're authenticated (use `-u admin:password123` with curl)
- Check DRF permission classes in `apps/products/views.py`

**Tests fail**
- Verify all migrations applied: `python manage.py migrate`
- Check Python 3.10+: `python --version`
- Fresh venv: `pip install -r requirements.txt --upgrade`

## Development Commands

```bash
# Run tests with verbose output
python manage.py test -v2

# Run specific test
python manage.py test tests.test_products.ProductTests.test_list_view

# Create superuser
python manage.py createsuperuser

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create sample data
python manage.py setup_demo

# Django shell (interactive)
python manage.py shell
```

## Next Steps

- [ ] Add more models (Inventory, Sales, Purchases)
- [ ] Implement viewsets with DRF routers
- [ ] Add filtering & pagination
- [ ] Deploy to production (Gunicorn + Nginx)
- [ ] Add GitHub Actions CI/CD
- [ ] Add frontend (React/Vue)

## License

MIT

## Support

For issues or questions, open a GitHub issue: https://github.com/MTNServices/Mzanzibari/issues
