import random
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from django.contrib import messages
from .forms import CartAddProductForm
from .models import Orders, OrderItems


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart:cart_detail')


def cart_add_1(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product)
    return redirect('cart:cart_detail')


def cart_remove_1(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product, quantity=-1)
    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart.html', {'cart': cart})


def order(request):
    cart = Cart(request)
    return render(request, 'cart/order.html', {'cart': cart})


def confirm_order(request):
    city = request.GET.get('city')
    address = request.GET.get('address')
    delivery = Orders.object.get(name='express') if request.GET.get('delivery') == 'express' else Orders.object.get(name='normal')
    payment_method = 1 if request.GET.get('pay') == 'online' else 0
    new_order = Orders(city=city, address=address, delivery=delivery, payment_method=payment_method, user=request.user)
    new_order.save()
    cart = Cart(request)
    for i in cart:
        print(i)
        new_item = OrderItems(order=new_order, product=i['product'], price=i['price'], quantity=i['quantity'])
        new_item.save()
    card = ''
    if not payment_method:
        card = random.randint(10000000, 99999999)
    cart = Cart(request)
    cart.clear()
    return render(request, 'cart/payment.html', {'order': new_order, 'card': card})


def pay(request, orderid):
    card = int(request.GET.get('card'))
    member = Orders.objects.get(id=orderid)
    if card % 2 != 0 or card % 10 == 0:
        messages.error(request, 'Ошибка оплаты')
        member.paid = 2
        member.save()
        return render(request, 'cart/payment.html', {'order': member, 'card': card})
    member = Orders.objects.get(id=orderid)
    member.paid = 1
    member.save()
    return redirect(to="cart:cart_detail")


def payment(request, orderid):
    member = Orders.objects.get(id=orderid)
    card = ''
    if not member.payment_method:
        payment_method = 0
    else:
        payment_method = 1
    return render(request, 'cart/payment.html', {'order': member, 'payment_method': payment_method})
