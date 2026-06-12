from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Cart
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import Order

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'product_detail.html', {'product': product})

@login_required
def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)

    Cart.objects.create(
        user=request.user,
        product=product
    )

    return redirect('cart')

@login_required
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)

    total = 0

    for item in cart_items:
        total += item.product.price * item.quantity

    return render(
        request,
        'cart.html',
        {
            'cart_items': cart_items,
            'total': total
        }
    )
@login_required
def remove_from_cart(request, id):
    item = Cart.objects.get(id=id)
    item.delete()
    return redirect('cart')
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)
            return redirect('home')

    return render(request, 'login.html')
def user_logout(request):
    logout(request)
    return redirect('home')
@login_required
def checkout(request):

    cart_items = Cart.objects.filter(user=request.user)

    total = 0

    for item in cart_items:
        total += item.product.price * item.quantity

    Order.objects.create(
        user=request.user,
        total_price=total
    )

    cart_items.delete()

    return render(request, "success.html")