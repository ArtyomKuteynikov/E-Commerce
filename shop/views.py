from django.shortcuts import get_object_or_404
from .models import Category, Product, Reviews
from django.db.models import Max, Min
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UpdateUserForm, UpdateProfileForm, CommentForm
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from cart.forms import CartAddProductForm

from cart.models import Orders, OrderItems


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'shop/password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('profile')


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'shop/profile.html', {'user_form': user_form, 'profile_form': profile_form})


def post_comment(request, slug):
    comment_form = CommentForm(data=request.POST)
    if comment_form.is_valid():
        new_comment = comment_form.save(commit=False)
        new_comment.name = request.user.first_name + ' ' + request.user.last_name
        new_comment.product = Product.objects.filter(slug=slug)[0]
        new_comment.save()
        member = Product.objects.get(slug=slug)
        member.reviews_num = member.reviews_num + 1
        member.save()
        return redirect(f'/product/{slug}')


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


def main_page(request, category_slug=None):
    categories = Category.objects.filter(primary=True)[:3]
    print(categories)
    top_products = Product.objects.all().order_by('sorting_index', 'bought')[:8]
    limited = Product.objects.filter(limited=True)
    return render(request,
                  'shop/main.html',
                  {'categories': categories,
                   'top_products': top_products,
                   'limited': limited})


def product_list(request, category_slug=None):
    name = ''
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if request.GET.get("q"):
        name = request.GET.get("q")
        products = products.filter(name__icontains=name)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    price = request.GET.get('price')
    if price:
        min_price = int(price.split(';')[0])
        max_price = int(price.split(';')[1])
        products = products.filter(price__range=(min_price, max_price))
    stock = request.GET.get('stock')
    if stock:
        products = products.filter(stock__range=(1, 1e9))
    producer = request.GET.get('producer')
    if producer:
        products = products.filter(producer__icontains=producer)
    sort = request.GET.get('sort')
    if request.GET.get('sort'):
        products = products.order_by(request.GET.get('sort'))
    choclates = Product.objects.all()
    price_min = choclates.aggregate(Min('price'))['price__min']
    price_max = choclates.aggregate(Max('price'))['price__max']
    if not price:
        min_price = price_min
        max_price = price_max
    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products,
                   'name': name,
                   'price_min': price_min,
                   'price_max': price_max,
                   'min_price': min_price,
                   'max_price': max_price,
                   'producer': producer,
                   'sort': sort})


def product_detail(request, slug):
    product = get_object_or_404(Product,
                                slug=slug,
                                available=True)
    comments = Reviews.objects.filter(product=product)
    cart_product_form = CartAddProductForm()
    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'comments': comments,
                   'comment_form': CommentForm(),
                   'cart_product_form': cart_product_form})


def profile(request):
    orders = list(Orders.objects.filter(user=request.user))
    print(orders)
    last_order = orders[0]
    return render(request, 'shop/account.html', {'orders': orders, 'last_order': last_order})


def history(request):
    orders = list(Orders.objects.filter(user=request.user))
    print(orders)
    return render(request, 'shop/historyorder.html', {'orders': orders})


def order(request, order_id):
    order = Orders.objects.get(id=order_id)
    orderitems = OrderItems.objects.filter(order_id=order)
    return render(request, 'shop/oneorder.html', {'order': order, 'orderitems': orderitems})
