from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Sum, Count
from openpyxl import Workbook
from reportlab.pdfgen import canvas
import csv
import pandas as pd

from product.models import Product
from product.forms import ProductForm


# ✅ LOGIN VIEW
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'login.html')


# ✅ LOGOUT VIEW
@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')


# ✅ DASHBOARD VIEW WITH ANALYTICS
@login_required(login_url='login')
def dashboard(request):
    products = Product.objects.all()

    # Summary calculations
    total_products = products.count()
    total_stock = products.aggregate(Sum('quantity'))['quantity__sum'] or 0
    low_stock_products = products.filter(quantity__lte=5).count()

    # Group products by category
    category_summary = (
        products.values('category')
        .annotate(total_stock=Sum('quantity'), count=Count('id'))
        .order_by('-count')
    )

    # DataFrame for visual table
    df = pd.DataFrame(list(products.values('name', 'category', 'price', 'quantity')))
    if not df.empty:
        df_html = df.to_html(classes='table table-striped table-bordered', index=False)
    else:
        df_html = "<p>No product data available.</p>"

    context = {
        'username': request.user.username,
        'products': products,
        'total_products': total_products,
        'total_stock': total_stock,
        'low_stock_products': low_stock_products,
        'category_summary': category_summary,
        'df': df_html,
    }
    return render(request, 'dashboard.html', context)


# ✅ ADD PRODUCT
@login_required(login_url='login')
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully!")
            return redirect('dashboard')
        else:
            messages.error(request, "Error adding product. Check your input.")
    else:
        form = ProductForm()
    return render(request, 'product_form.html', {'form': form, 'action': 'Add'})


# ✅ UPDATE PRODUCT
@login_required(login_url='login')
def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully!")
            return redirect('dashboard')
        else:
            messages.error(request, "Error updating product.")
    else:
        form = ProductForm(instance=product)
    return render(request, 'product_form.html', {'form': form, 'action': 'Update'})


# ✅ DELETE PRODUCT
@login_required(login_url='login')
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, "Product deleted successfully!")
        return redirect('dashboard')
    return render(request, 'confirm_delete.html', {'product': product})


# ✅ EXPORT AS CSV
@login_required(login_url='login')
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="products.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Category', 'Price', 'Quantity'])
    for product in Product.objects.all():
        writer.writerow([product.name, product.category, product.price, product.quantity])
    return response


# ✅ EXPORT AS EXCEL
@login_required(login_url='login')
def export_excel(request):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = 'Products'
    sheet.append(['Name', 'Category', 'Price', 'Quantity'])

    for product in Product.objects.all():
        sheet.append([product.name, product.category, product.price, product.quantity])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="products.xlsx"'
    workbook.save(response)
    return response


# ✅ EXPORT AS PDF
@login_required(login_url='login')
def export_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="products.pdf"'

    p = canvas.Canvas(response)
    p.setFont("Helvetica-Bold", 14)
    y = 820
    p.drawString(100, y, "Zanzibari Product List")
    p.setFont("Helvetica", 11)
    y -= 30

    for product in Product.objects.all():
        text = f"{product.name} | {product.category} | {product.price} | Qty: {product.quantity}"
        p.drawString(80, y, text)
        y -= 20
        if y < 50:
            p.showPage()
            p.setFont("Helvetica", 11)
            y = 820

    p.showPage()
    p.save()
    return response
