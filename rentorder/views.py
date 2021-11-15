from datetime import date, timedelta

from django.shortcuts import render, get_object_or_404

from rcart.models import *
from rental.models import Rentbook, Rental
from .models import *
from .forms import *

def cart_id(request):
    cart = request.session.session_key
    return cart

def rent_create(request):
    rcart = Cart.objects.get(cart_id=cart_id(request))
    rcart_items = CartItem.objects.filter(cart=rcart, active=True)
    print(rcart_items)

    # product = Buybook.objects.get(id=id)
    if request.method == 'POST': #입력받은 정보를 후처리 하는 부분
        form = RentCreateForm(request.POST) # 입력받은 정보를 넣어서 form 생성
        if form.is_valid():
            order = form.save()
            order.save()




            # total = cart.get_total_price / 100
            # user = request.user
            # user.point = user.point + total
            # user.save()

            return render(request, 'rorder/created.html', {'order':order})

    else:
        form = RentCreateForm()

    return render(request, 'rorder/create.html', {'rcart_items':rcart_items, 'form':form})

def rent_complete(request):
    rorder_id = request.GET.get('order_id')
    rorder = Rent.objects.get(id=rorder_id)
    rcart = Cart.objects.get(cart_id=cart_id(request))
    rcart_items = CartItem.objects.filter(cart=rcart, active=True)
    rentdate = date.today()
    duedate = date.today() + timedelta(days=14)
    rentalstate = '대여중'
    for item in rcart_items:
        rproduct = Rentbook.objects.get(id=item.product_id)
        rent_item = RentItem.objects.create(order=rorder, product=rproduct.id, rent_date=rentdate, due=duedate,
                                            rental_state=rentalstate)
        rentbook = Rentbook.objects.get(id=rent_item.product_id)
        rentbook.rstock = rentbook.rstock - 1
        rentbook.save()

    rcart_items.delete()

    return render(request, 'rorder/created.html', {'rorder':rorder})


from django.views.generic.base import View
from django.http import JsonResponse

class RentCreateAjaxView(View):
    def post(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return JsonResponse({"authenticated":False}, status=403)

        # cart = Cart(request)

        form = RentCreateForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)

            order.save()

            # for item in cart:
            #     order_item = OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
            #     buybook = Buybook.objects.get(id=order_item.product_id)
            #     buybook.bstock = buybook.bstock - order_item.quantity
            #     buybook.save()
            #
            # cart.clear()

            data = {
                "order_id": order.id
            }
            return JsonResponse(data)

        else:
            return JsonResponse({}, status=401)

class RentCheckoutAjaxView(View):
    def post(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return JsonResponse({"authenticated":False}, status=403)

        order_id = request.POST.get('order_id')
        order = Rent.objects.get(id=order_id)
        amount = request.POST.get('amount')

        try:
            merchant_order_id = RentTransaction.objects.create_new(order=order, amount=amount)
        except:
            merchant_order_id = None

        if merchant_order_id is not None:
            data = {
                "works": True,
                "merchant_id": merchant_order_id
            }
            return JsonResponse(data)
        else:
            return JsonResponse({}, status=401)


class RentImpAjaxView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"authenticated":False}, status=403)

        order_id = request.POST.get('order_id')
        order = Rent.objects.get(id=order_id)
        merchant_id = request.POST.get('merchant_id')
        imp_id = request.POST.get('imp_id')
        amount = request.POST.get('amount')
        rcart = Cart.objects.get(cart_id=cart_id(request))
        rcart_items = CartItem.objects.filter(cart=rcart, active=True)
        rentdate = date.today()
        duedate = date.today() + timedelta(days=14)
        rentalstate = '대여중'
        user = request.user

        for item in rcart_items:
            custid = User.objects.get(id=user.id)
            rproduct = Rentbook.objects.get(id=item.product_id)
            rent_item = RentItem.objects.create(order=order, product=rproduct, rent_date=rentdate, due=duedate, rental_state=rentalstate, cust=custid)
            Rental.objects.create(due=duedate, rental_state=rentalstate,rent_date=rentdate,cust_num=custid,rbook_id=rproduct)
            rentbook = Rentbook.objects.get(id=rent_item.product_id)
            rentbook.rstock = rentbook.rstock - 1
            rentbook.save()

        rcart_items.delete()
        try:
            trans = RentTransaction.objects.get(
                order=order,
                merchant_order_id=merchant_id,
                amount=amount
            )
        except:
            trans = None

        if trans is not None:
            trans.transaction_id = imp_id
            trans.success = True
            trans.save()

            order.paid = True
            order.save()

            data = {
                "works": True
            }
            return JsonResponse(data)
        else:
            return JsonResponse({}, status=401)

from django.contrib.admin.views.decorators import staff_member_required
@staff_member_required
def admin_rent_detail(request, order_id):
    order = get_object_or_404(Rent, id=order_id)
    return render(request, 'rorder/admin/detail.html', {'order':order})

from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint

@staff_member_required
def admin_rent_pdf(request, order_id):
    order = get_object_or_404(Rent, id=order_id)
    html = render_to_string('rorder/admin/pdf.html', {'order':order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=order_{}.pdf'.format(order.id)
    weasyprint.HTML(string=html).write_pdf(response, stylesheets=[weasyprint.CSS(str(settings.STATICFILES_DIRS[0])+'/css/pdf.css')])
    return response