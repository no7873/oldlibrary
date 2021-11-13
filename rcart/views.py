from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from rental.models import Rentbook
from .forms import AddProductForm
from .models import Cart, CartItem

# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    product = Rentbook.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
        cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            cart = cart
        )
        cart_item.save()
    return redirect('rcart:rdetail')

def cart_detail(request, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)
    except ObjectDoesNotExist:
        pass
    return render(request, 'rcart/detail.html', {'cart_items':cart_items})

def cart_remove(request, product_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Rentbook, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('rcart:rdetail')


<<<<<<< Updated upstream
=======
    if form.is_valid():
        cd = form.cleaned_data
        rcart.add(product=product, quantity=cd['quantity'], is_update=cd['is_update'])

    return redirect('rcart:detail')

def remove(request, product_id):
    rcart = Rcart(request)
    product = get_object_or_404(Rentbook, id=product_id)
    rcart.remove(product)

    return redirect('rcart:detail')


def detail(request):
    rcart = Rcart(request)

    for product in rcart:
        product['quantity_form'] = AddProductForm(initial={'quantity':product['quantity'], 'is_update':True})
    return render(request, 'rcart/detail.html', {'rcart':rcart})
>>>>>>> Stashed changes
