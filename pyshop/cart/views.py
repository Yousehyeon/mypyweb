from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from cart.cart import Cart
from cart.forms import AddProductForm
from shop.models import Product


def detail(request):
    cart = Cart(request)

    for product in cart:
        product['quantity_form'] = AddProductForm(
            initial={'quantity': product['quantity'],
                     'id_update':True}
        )
    context = {'cart': cart}
    return render(request, 'cart/detail.html')

#장바구니에 제품 추가
@require_POST
def add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    form = AddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'],
                 is_update=cd['is_update'])
        return redirect('cart:detail')