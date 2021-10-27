from django.shortcuts import render
from mainapp.models import Product, ProductCategory


def index(request):
    content = {
        'title': 'Главная',
        'products': Product.objects.all()[:4]
    }
    return render(request, 'mainapp/index.html', content)


def contact(request):
    content = {
        'title': 'Контакты'
    }
    return render(request, 'mainapp/contact.html', content)


def products(request, pk=None):
    content = {
        'links_menu': ProductCategory.objects.all(),
        'title': 'Продукты'
    }
    return render(request, 'mainapp/products.html', context=content)


