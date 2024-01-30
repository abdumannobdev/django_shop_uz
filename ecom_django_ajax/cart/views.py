from django.shortcuts import render
from .models import Product, Cart, Cartitems
from django.http import JsonResponse
import json

# Create your views here.
def store(request):
    if request.user.is_authenticated:
        customer = request.user
        cart, created = Cart.objects.get_or_create(owner=customer, completed = False)
        cartitems = cart.cartitems_set.all()
    else:
        cart = []
        cartitems = []
        cart = {'cartquantity': 0}

    products = Product.objects.all()
    context = {'products': products, 'cart': cart, 'cartitems': cartitems}
    return render(request, 'cart/store.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        cart, created = Cart.objects.get_or_create(owner=customer, completed = False)
        cartitems = cart.cartitems_set.all()
    else:
        cart = []
        cartitems = []
        cart = {'cartquantity': 0}
    context = {'cart': cart, 'cartitems': cartitems}
    return render(request, 'cart/cart.html', context)

def updateCart(request):
    data = json.loads(request.body)
    product_id = data['product_id']
    action = data['action']
    if request.user.is_authenticated:
        customer = request.user
        product = Product.objects.get(product_id= product_id)
        cart, created = Cart.objects.get_or_create(owner=customer, completed=False)
        cartitems, created = Cartitems.objects.get_or_create(product=product, cart=cart)

        if action == 'add':
            cartitems.quantity += 1
        cartitems.save()

        msg = {
            'quantity': cart.cartquantity
        }

    return JsonResponse(msg, safe=False)

def updateQuantity(request):
    data = json.loads(request.body)
    inputval = int(data['in_val'])
    product_id = data['p_id']
    if request.user.is_authenticated:
        customer = request.user
        product = Product.objects.get(product_id= product_id)
        cart, created = Cart.objects.get_or_create(owner=customer, completed=False)
        cartitems, created = Cartitems.objects.get_or_create(product=product, cart=cart)

        cartitems.quantity = inputval
        cartitems.save()

        msg = {
            'subtotal':cartitems.subtotal,
            'grandtotal': cart.grandtotal,
            'quantity': cart.cartquantity
        }

    return JsonResponse(msg, safe=False)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        cart, created = Cart.objects.get_or_create(owner=customer, completed = False)
        cartitems = cart.cartitems_set.all()
    else:
        cart = []
        cartitems = []
        cart = {'cartquantity': 0}
    context = {'cart': cart, 'cartitems': cartitems}
    return render(request, 'cart/checkout.html', context)

def payment(request):
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user
        cart, created = Cart.objects.get_or_create(owner=customer, completed=False)
        total = float(data['cart_total'])
        
        if total == cart.grandtotal:
            cart.completed = True
            cart.save()
        
        
        
    return JsonResponse('It is working', safe=False)

from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def HomePage(request):
    return render(request, 'cart/cart.html')

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')


        if pass1!=pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')

    return render(request, 'cart/signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user = authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse("Username or Password is Incorrect !!")

    return render(request, 'cart/login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')