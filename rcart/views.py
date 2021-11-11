from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from rental.models import Rentbook
from .forms import AddProductForm
from .cart import Rcart

# Create your views here.

@require_POST
def add(request, product_id):
    cart = Rcart(request)
    product = get_object_or_404(Rentbook, id=product_id)

    form = AddProductForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], is_update=cd['is_update'])

    return redirect('rcart:detail')

def remove(request, product_id):
    cart = Rcart(request)
    product = get_object_or_404(Rentbook, id=product_id)
    cart.remove(product)

    return redirect('rcart:detail')


def detail(request):
    cart = Rcart(request)

    for product in cart:
        product['quantity_form'] = AddProductForm(initial={'quantity':product['quantity'], 'is_update':True})
    return render(request, 'cart/detail.html', {'rcart':cart})