from django.shortcuts import render

def home(request):
    return render(request, 'main.html')

def dashboard(request):
    return render(request, 'dashboard.html')
