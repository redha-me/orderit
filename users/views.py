from django.utils import translation
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,redirect,reverse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import FormView,UpdateView,DetailView
from django.urls import reverse_lazy
from cart.cart import Cart
from config import settings
from core.models import Address
from partner_restaurent.models import MenuItem, Order, OrderDetails, Restaurent
from . import forms,models,mixins
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
import os
from django.utils.translation import gettext_lazy as _




                                        #----------#
                                        #  USER    # 
                                        #----------#
class SignUpView(mixins.LoggedOutOnly,FormView):
    template_name='users/signup.html'
    form_class=forms.SignUpForm
    success_url=reverse_lazy('core:home')

    def form_valid(self, form):
        form.save()
        email=form.cleaned_data.get('email')
        password=form.cleaned_data.get('password1')
        username=form.cleaned_data.get('username')
        avatar=form.cleaned_data.get('avatar')
        user=authenticate(self.request,username=username,password=password,avatar=avatar)
        if user is not None:
                login(self.request,user)
            
        user.verify_email()
        messages.info(self.request,_('verify your email'))
        return super().form_valid(form)
        
def complete_verification(request,key):
    
    try:
        user=models.User.objects.get(email_pass=key)
        user.email_confirmed=True
        user.email_pass=''
        user.save()
        messages.success(request,_('email verified'))
    except models.User.DoesNotExist:
        messages.warning(request,_('email not verified'))
        
    return redirect(reverse('core:home'))



   

def log_out(request):
    logout(request)
    return redirect(reverse('users:login'))

class LoginView(mixins.LoggedOutOnly,FormView):
    template_name='users/login.html'
    form_class=forms.LoginForm
    # success_url=reverse_lazy('core:home')

    def form_valid(self,form):
            email=form.cleaned_data.get('email')
            password=form.cleaned_data.get('password')
            username=models.User.objects.get(email=email).username
            user=authenticate(self.request,username=username,password=password)
            if user is not None:
                 login(self.request,user)
            return super().form_valid(form)
    def get_success_url(self):
        next_url=self.request.GET.get('next')
        if next_url is not None:
            return next_url
        else:
            return reverse('core:home')


class Account(DetailView):
    model = models.User
    context_object_name = "user_obj"
    template_name='users/account.html'


class AccountUpdate(mixins.UserInfo,UpdateView):
    model=models.User
    fields=['avatar','username',]
    template_name='users/accountUpdate.html'
    def get_success_url(self):
        messages.success(self.request,_('successfully updated'))
        return reverse_lazy('core:home')
    def get_object(self, queryset=None):
        return self.request.user

class UpdatePassword(mixins.UserInfo,PasswordChangeView):
    # form_class=PasswordChangeForm
    template_name = "users/update-password.html"
    
    def get_success_url(self):
        messages.success(self.request,_('successfully updated'))
        return reverse_lazy('core:home')
    
    






@login_required(login_url='/users/login/')
def add_order(request):
    """
    params:
    1-restaurent_id
    2-restaurent_address
    3-order_details:[{"meal_id":277,"quantity":1},{"meal_id":279,"quantity":2}]
    return: message('success')
    """
    if request.method!="POST":
        return redirect('core:home')

    if request.method=="POST":
        customer=request.user
        if Order.objects.filter(customer=customer).exclude(status=Order.DELIVERED):
             messages.error(request,_("your last order must be completed"))
             return redirect('core:home')

        #Check order's addresse

        if not request.POST['address'] or request.POST['address']== 'nn':
             messages.error(request,_("the Address is required"))
             messages.info(request,_("activate location"))
             return redirect('cart:checkout')
        
        #Get order details
        order_details=[]
        cart=Cart(request)
        for item in cart:
            order_details.append(item)
        tmp=request.POST['address']
        tmp=list(tmp.split(','))
        add=[]
        for i in tmp:
            add.append(float(i))
        

        #Check if the meals in only one restaurent and then calculate the order total
        order_total=0
        meal=MenuItem.objects.get(pk=order_details[0]['id'])
        restaurent_id=meal.restaurent.pk
       
        #if partner try to order from his restaurent
        if request.user.is_partner:
            current_res=Restaurent.objects.get(user=request.user)
            if meal.restaurent == current_res:
                messages.info(request,_("can't do that"))
                return redirect('core:home')

        for meal in order_details:
            if not MenuItem.objects.filter(id=meal['id'],restaurent_id=restaurent_id):
                messages.warning(request,_('the meal must be only in one restaurent'))

                return redirect('core:home')

            else:
                order_total+=MenuItem.objects.get(id=meal['id']).price * meal['quantity']
        
        #Create Order
        if len(order_details)>0:
            #Step-1: Create an Order
            order=Order.objects.create(
                customer=customer,
                restaurent_id=restaurent_id,
                total=order_total,
                status=Order.COOKING,

                address=Address.objects.create(address=add,wilaya=request.POST['wilaya'],commune=request.POST['commune']),
            )
            #Step-2: Create  Order Details
            for meal in order_details:
                OrderDetails.objects.create(
                    order=order,
                    meal_id=meal['id'],
                    quantity=meal['quantity'],
                    sub_total=MenuItem.objects.get(id=meal['id']).price * meal['quantity'],
                )
            messages.success(request,_('success'))
            return redirect('users:deliverys')
        

            

@login_required(login_url='/users/login/')
def deliverys(request):
    customer = request.user
    order_status =Order.objects.filter(customer=customer).last()
    if order_status:
        if order_status.status != Order.DELIVERED:
            restaurent_address=[float(order_status.restaurent.long),float(order_status.restaurent.lat)]#geotransformer(order_status.restaurent.address_exacte)
            customer_address=order_status.address.address 
        else:
            return redirect('core:home')
        if order_status.status==4:
            messages.info(request,_('there is no deliverys'))
            return redirect('core:home')
        cart = Cart(request)
        cart.clear_cart()
        mapbox_api=os.environ.get('MAPBOX_API_KEY')
        if order_status.driver:
            driver_address=[float(order_status.driver.long),float(order_status.driver.lat)]
            context={
                'access_token':mapbox_api,
                'order':order_status,
                'driver_address':driver_address,
                'condition':True,
                "status":order_status.status,
                'restaurent_address':restaurent_address,
                'cutomer_address':customer_address,

            }
        else:
            context={
                'access_token':mapbox_api,
                'condition':False,
                'driver_address':None,
                'order':order_status,
                "status":order_status.status,
                'restaurent_address':restaurent_address,
                'cutomer_address':customer_address,

            }

        response= render(request,'users/deliverys.html',context)
        return response
    else:
        return redirect("core:home")
    



        
@csrf_exempt
@login_required(login_url='/users/login/')
def update_delivery_menu(request):
    customer = request.user
    order_status=Order.objects.filter(customer=customer).last()
    if request.method =='POST':
        context={
                    "status":order_status.status,
                    'order':order_status,

                }
        return render(request,'users/status.html',context)
    else:
        messages.error(request,_("can't go there"))
        return redirect('core:home')
        
