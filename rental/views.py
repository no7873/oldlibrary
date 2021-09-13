from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from .models import *
# Create your views here.
def rentbook_in_category(request, category_slug=None):
    current_category = None
    categories = Rentcategory.objects.all()
    products = Rentbook.objects.filter(available_display=True)

    if category_slug:
        current_category = get_object_or_404(Rentcategory, slug=category_slug)
        products = products.filter(category=current_category)

    return render(request, 'shop/rent_list.html',
                  {'current_category': current_category, 'categories': categories, 'products': products})

def rentbook_detail(request, id, product_slug=None):
    product = get_object_or_404(Rentbook, id=id, slug=product_slug)
    reserve = get_object_or_404(Reservation, bookid=id)
    reserve_count = Reservation.objects.filter(bookid=id).values('bookid').annotate(total=Count('bookid')).order_by('bookid')
    rental_date = Rental.objects.filter(bookid=id).order_by("expdate")[1:2]

    return render(request, 'shop/rent_detail.html', {'product':product, 'reserve':reserve, 'reserve_count':reserve_count, 'rental_date':rental_date})