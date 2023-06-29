# 장바구니  - 세션(session)
from django.conf import settings
from _decimal import Decimal
from shop.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_ID)
        if not cart:
            cart = self.session[settings.CART_ID] = {}
        self.cart = cart

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        for product in products:
            self.cart[str(product.id)] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            # 총합계 = 단위당 가격 * 수량
            item['total_price'] = item['price'] * item['quantity']

            yield item  # item을 반환(return)

    # 장바구니에 제품 추가
    def add(self, product, quantity=1, is_update=False):
        product_id = str(product.id)
        
        # 카트에 제품이 없는 경우
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                    'price': str(product.price)}
        # 카트에 제품이 있는 경우
        if is_update:
            self.cart[product_id]['quantity'] = quantity # 수량 변경
        else: # 수량 증가
            self.cart[product_id]['quantity'] += quantity
        
