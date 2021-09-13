import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count, Q
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.views.generic import FormView, DetailView
from datetime import datetime

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
    # reserve = get_object_or_404(Reservation, bookid=id)

    # try:
    reserve_count = Reservation.objects.filter(bookid=id).values('bookid').annotate(total=Count('bookid')).order_by('bookid')
    rental_count = Rental.objects.filter(bookid=id).values('bookid').annotate(total=Count('bookid')).order_by('bookid')
    # for r in reserve_count:
    #     for rt in rental_count:
    #         rc = r.get('total')
    #         rtc = rt.get('total')
    #         rcp = rc + 1
    #         if rtc > rc:#대여 인원수가 예약 인원수 보다 많은 경우
    #             rental_date = Rental.objects.filter(bookid=id).order_by('expdate')[rc:rcp]
    #             # print(rental_date)
    #             # rent_date = rental_date.get('expdate') + datetime.timedelta(days=1)
    #             # print(rent_date)
    #
    #             # return render(request, 'shop/rent_detail.html', {'rent_date':rent_date})
    #         else:
    #             rentals_date = Reservation.objects.filter(bookid=id).order_by('exrent')
    #             # print(rental_date)

    # except:
    #     reserve_count = Reservation(bookid=id, total=0)
    #     reserve_count.save()
    return render(request, 'shop/rent_detail.html', {'product':product, 'reserve_count':reserve_count, 'rental_count':rental_count})

@require_POST
def reserve(request, id):
    product = get_object_or_404(Rentbook, id=id)
    today = datetime.now()

    user = request.user
    if request.method == 'POST':
        reserve = Reservation.objects.create(
            bookid=product,
            custnum=user,
            exrent=today
        )
        reserve.save()
    return render(request, 'shop/reserve.html', {'product':product})