from decimal import Decimal
from django.conf import settings
from shop.models import Buybook
from rental.models import Rentbook

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_ID) # settings에 CART_ID를 만들어야함
        if not cart:
            cart = self.session[settings.CART_ID] = {}
        self.cart = cart

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Buybook.objects.filter(id__in=product_ids)

        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['total_price'] = item['price'] * item['quantity']
            item['price'] = Decimal(item['price'])

            yield item

    def add(self, product, quantity=1, is_update=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity':0, 'price':str(product.price)}

        if is_update:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session[settings.CART_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del (self.cart[product_id])
            self.save()

    def clear(self):
        self.session[settings.CART_ID] = {}
        self.session.modified = True

    def get_product_total(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    @property
    def get_total_price(self):
        return self.get_product_total() + 2500