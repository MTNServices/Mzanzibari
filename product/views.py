from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category
from .forms import ProductForm

def dashboard(request):
    total_products = Product.objects.count()
    total_stock = sum(p.quantity for p in Product.objects.all())
    low_stock_items = Product.objects.filter(quantity__lte=5).count()
    categories = Category.objects.all()

    return render(request, 'dashboard.html', {
        'total_products': total_products,
        'total_stock': total_stock,
        'low_stock_items': low_stock_items,
        'categories': categories,
    })


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProductForm()
    return render(request, 'product/add_product.html', {'form': form})


def edit_product(request, product_id):
    """Edit an existing product."""
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProductForm(instance=product)
    return render(request, 'product/edit_product.html', {'form': form, 'product': product})
