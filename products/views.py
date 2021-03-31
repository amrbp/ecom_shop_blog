from django.shortcuts import render,get_object_or_404
from .forms import UserRegisterForm
from .models import Category, Product
from django.http import HttpResponseRedirect,Http404
from products.models import *
from django.http import JsonResponse
import json
import datetime

def product_list(request):
    categories = Category.objects.all()
    products = Product.objects.all() 

    pro_category = Product.objects.filter(category=None).order_by('name')


    if request.user.is_authenticated:
        customer = request.user.profile
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_item': 0, 'shipping': False}
        cartItems = order['get_cart_item']


    context = {
        'categories': categories,
        'products': products,
        'pro_category': pro_category,
        'items': items, 
        'order': order, 
        'cartItems': cartItems
    }

    return render(request, 'products/product_list.htm',context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.htm', {'form': form})

    
def ProductDetailView(request, pk):
    try:
        p = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        raise Http404("does not exist")

    if request.user.is_authenticated:
        customer = request.user.profile
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_item': 0, 'shipping': False}
        cartItems = order['get_cart_item']

    context = {'items': items, 'order': order, 'cartItems': cartItems, 'product': p}
    return render(request, 'products/productDetail.htm', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.profile
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_item': 0, 'shipping': False}
        cartItems = order['get_cart_item']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'products/cart.htm', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.profile
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_item': 0, 'shipping': False}
        cartItems = order['get_cart_item']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'products/checkout.htm', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('productId:', productId)

    customer = request.user.profile
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.profile
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.shipping == True:
            ShoppingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )

    else:
        print('User is not logged in')
    return JsonResponse('Payment', safe=False)
