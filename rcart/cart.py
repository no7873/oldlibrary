from decimal import Decimal
from django.conf import settings
from rental.models import Rentbook

class Rcart(object):
    def __init__(self, request): # 초기화, Django view에서 사용한 request로 그 안에 session 정보가 들어있음
        self.session = request.session
        rcart = self.session.get(settings.CART_ID) # settings에 CART_ID를 만들어야함
        if not rcart: # cart 정보가 없을때는 새로운 dictionary 만들어줌
            rcart = self.session[settings.CART_ID] = {}
        self.rcart = rcart

    def __len__(self): # 장바구니에 들어있는 제품의 quantity 항목들을 전부 더한 결과 제공
        return sum(ritem['quantity'] for ritem in self.rcart.values())

    def __iter__(self): # for 문 등 사용할 때 어떤 요소들을 건네줄 것인지 지정
        product_ids = self.rcart.keys() # 제품들 번호 목록을 가져옴

        products = Rentbook.objects.filter(id__in=product_ids) # 장바구니에 들어있는 제품들 정보만 Product database에서 가져옴

        for product in products: # 제품들 정보 하나씩 읽어옴
            self.rcart[str(product.id)]['product'] = product # session에 키 값들을 넣을때는 문자로 넣어줌

        for ritem in self.rcart.values(): # 장바구니에 들어있는 제품들을 하나씩 꺼내는 것
            # 제품 가격, Decimal : 숫자형으로 바꿔서 item에 넣어줌
            ritem['total_price'] = ritem['price'] * ritem['quantity'] # price x item 수
            ritem['price'] = Decimal(ritem['price'])

            yield ritem

    # 제품 장바구니에 넣기
    # is_update : 제품 정보를 업데이트하는지 아닌지 확인하는 것
    def add(self, product, quantity=1, is_update=False):
        product_id = str(product.id)
        if product_id not in self.rcart:
            self.rcart[product_id] = {'quantity':0, 'price':str(product.price)}

        if is_update:
            self.rcart[product_id]['quantity'] = quantity
        else:
            self.rcart[product_id]['quantity'] += quantity
        self.save()


    def save(self):
        self.session[settings.CART_ID] = self.rcart
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.rcart:
            del (self.rcart[product_id])
            self.save()

    def clear(self):
        self.session[settings.CART_ID] = {}
        self.session.modified = True

    def get_product_total(self):
        return sum(Decimal(ritem['price']) * ritem['quantity'] for ritem in self.rcart.values())

    @property
    def get_total_price(self):
        return self.get_product_total()