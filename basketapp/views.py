from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.template.loader import render_to_string

from basketapp.models import Basket
from mainapp.models import Product


@login_required
def basket(request):
    baskets_list = Basket.objects.filter(user=request.user)
    content = {
        'baskets': baskets_list
    }
    return render(request, 'basketapp/basket.html', content)


@login_required
def add(request, pk):
    product_item = get_object_or_404(Product, pk=pk)
    basket_item = Basket.objects.filter(product=product_item, user=request.user).first()
    if not basket_item:
        basket_item = Basket(product=product_item, user=request.user)
    basket_item.quantity += 1
    basket_item.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def remove(request, pk):
    basket_item = get_object_or_404(Basket, pk=pk)
    basket_item.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def edit(request, pk, quantity):
    if request.is_ajax():
        quantity = int(quantity)
        basket_item = Basket.objects.get(pk=pk)

        if quantity > 0:
            basket_item.quantity = quantity
            basket_item.save()
        else:
            basket_item.delete()

        basket_list = Basket.objects.filter(user=request.user)

        content = {
            'baskets': basket_list
        }
        result = render_to_string('basketapp/includes/inc_baskets_list.html', content)

        return JsonResponse({'result': result})
