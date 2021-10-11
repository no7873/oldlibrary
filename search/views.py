from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render
from rental.models import *
from shop.models import *

# Create your views here.
def searchResult(request):
    rental_products = None
    buy_products=None
    query = None
    if 'q' in request.GET:
        query = request.GET.get('q')
        rental_products = Rentbook.objects.all().filter(Q(rtitle__icontains=query) | Q(rpublisher__icontains=query) | Q(rauthor__icontains=query))
        buy_products=Buybook.objects.all().filter(Q(btitle__icontains=query) | Q(bpublisher__icontains=query) | Q(bauthor__icontains=query))
        buy_product=buy_products.all()
        for a in rental_products:
            if rental_products.exists():
                buy_product = buy_products.exclude(
                    Q(btitle=a.rtitle) & Q(bpublisher=a.rpublisher) & Q(bauthor=a.rauthor))

        if not rental_products.exists() and not buy_product.exists():
            messages.add_message(request, messages.INFO, '검색결과가 없습니다.')
    return render(request, 'search.html', {'query':query, 'rental_products':rental_products, 'buy_products':buy_products, 'buy_product':buy_product})
