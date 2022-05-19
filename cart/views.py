from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render
from core import forms
from partner_restaurent.models import MenuItem
from .cart import Cart
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _



@login_required(login_url='/users/login/')
def add_to_cart(request, dish_id):
    cart = Cart(request)
    cart.add(dish_id)
    return render(request, 'cart/menu_cart.html')

@login_required(login_url='/users/login/')
def cart(request):
    cart = Cart(request)
    if cart.length()==0:
        messages.info(request,_('your cart is empty'))
        return redirect('core:home')
    return render(request, 'cart/cart.html')

@login_required(login_url='/users/login/')
def Checkout(request):
    context={'form':forms.addressForm,
            'lang':request.LANGUAGE_CODE
        }
    return render(request, 'cart/checkout.html',context)
    

@login_required(login_url='/users/login/')
@csrf_exempt
def update_cart(request, product_id, action):
    if request.method == 'POST':
        cart = Cart(request)

        if action == 'increment':
            cart.add(product_id, 1, True)
        else:
            cart.add(product_id, -1, True)
        
        product = MenuItem.objects.get(pk=product_id)
        quantity = cart.get_item(product_id)
        if quantity:
            quantity = quantity['quantity']
            item = {
                'Dish':product,
                'total_price': (quantity * product.price) ,
                'quantity': quantity,
            }
        else:
            item=None

        response = render(request, 'cart/cart_item.html',{'item':item})
        response['HX-Trigger'] = 'update-menu-cart'
        return response
    else:
        return redirect('core:home')

def hx_menu_cart(request):
    return render(request, 'cart/menu_cart.html')

def hx_cart_total(request):
    return render(request, 'cart/cart_total.html')