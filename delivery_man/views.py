import os
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render
from django.views.generic import FormView
from django.utils import timezone
from core.models import Address, Commune, Wilaya
from partner_restaurent.models import Order
from . import forms,mixins
from django.views.generic.edit import UpdateView 
from django.urls import reverse_lazy
from django.http import HttpResponse
from .models import DeliveryMan
from users.models import User
from django.contrib import messages
from core.views import distance_calc
from django.utils.translation import gettext_lazy as _



      


#----------#
#  Driver  # 
#----------#




class  SignUpView(mixins.SignUpPartnerOnly,FormView):
    template_name='delivery_man/signup.html'
    form_class=forms.DeliverySignup
    success_url=reverse_lazy('delivery_man:home')
    def form_valid(self, form):
        wilaya=form.cleaned_data.get('wilaya')
        commune=form.cleaned_data.get('commune')
        nom=form.cleaned_data.get('nom')
        prenom=form.cleaned_data.get('prenom')
        avatar=form.cleaned_data.get('avatar')
        plate_number=form.cleaned_data.get('plate_number')
        mobile=form.cleaned_data.get('mobile')
        email=form.cleaned_data.get('email')
        moyen_de_livraison=form.cleaned_data.get('moyen_de_livraison')
        heur_debut_desponible=form.cleaned_data.get('heur_debut_desponible')
        heur_fin_desponible=form.cleaned_data.get('heur_fin_desponible')
        jour_desponibilite=form.cleaned_data.get('jour_desponibilite')
        user=User.objects.get(username=self.request.user)
        if user is not None:
            user.is_delivery_man=True
            user.save()
            DeliveryMan.objects.create(user=user,wilaya=str(wilaya),commune=str(commune),nom=str(nom),prenom=str(prenom),mobile=str(mobile),email=str(email),moyen_de_livraison=moyen_de_livraison,heur_debut_desponible=str(heur_debut_desponible),heur_fin_desponible=str(heur_fin_desponible),jour_desponibilite=str(jour_desponibilite),avatar=avatar,
plate_number=plate_number)
        return super().form_valid(form)

    
@csrf_exempt
@login_required(login_url='/users/login/')
def load_commune(request):
    if request.method == 'POST':
        form=forms.DeliverySignup(request.POST)
        return HttpResponse(form['commune'])
    else:
        return redirect('core:home')


@login_required(login_url='/users/login/')
def dashbord(request):
    if request.user.is_delivery_man:
        delivery_man=DeliveryMan.objects.get(user=request.user)
        context={
        'deliveryman':delivery_man 
        }
        return render(request, 'delivery_man/sidebar.html',context)
    else:
        messages.error(request,_("can't go there"))
        return redirect('delivery_man:signup')

@login_required(login_url='/users/login/')
def driver_get_profile(request):
    if request.user.is_delivery_man:
        driver=DeliveryMan.objects.get(user=request.user)
        context={
            'deliveryman':driver,
        }
        return render(request,'delivery_man/account.html',context)
    else:
        messages.error(request,_("can't go there"))
        return redirect('delivery_man:signup')


class driver_update_profile(mixins.RegistredPartnerOnly,UpdateView):
    model=DeliveryMan
    fields=['nom','prenom','plate_number','avatar','wilaya','commune','mobile','email','moyen_de_livraison','heur_debut_desponible','heur_fin_desponible','jour_desponibilite',]
    template_name='delivery_man/accountUpdate.html'
    def get_success_url(self):
        messages.success(self.request,_('successfully updated'))
        return reverse_lazy('delivery_man:account')
    def get_object(self ):
        deliveryman=DeliveryMan.objects.get(user=self.request.user)
        return deliveryman
    
@csrf_exempt
@login_required(login_url='/users/login/')
def get_ready_orders(request):
    try:
    
        if  request.user.is_delivery_man:
            deliveryman=DeliveryMan.objects.get(user=request.user)
            if request.method == "POST":
                deliveryman.lat=request.POST['lat']
                deliveryman.long=request.POST['long']
                deliveryman.save()
            wilaya,commune=str(Wilaya.objects.get(name__icontains=deliveryman.wilaya).id),str(Commune.objects.get(name__icontains=deliveryman.commune).id)
            orders=Order.objects.all().filter(status=Order.READY,driver= None)
            order_list=[]
            
            
            for order in orders.iterator():
                if order.address.wilaya==wilaya and order.address.commune==commune:
                
                        order.address.wilaya=Wilaya.objects.get(id=order.address.wilaya).name
                        order.address.commune=Commune.objects.get(id=order.address.commune).name
                        order_list.append(order)
            
                
                    


        else:
            messages.error(request,_("can't go there"))
            return redirect('delivery_man:signup')

    except Order.DoesNotExist:
         messages.info(request,_('there is no ready order yet'))
         return redirect('delivery_man:home')
        
    context={
        'orders':order_list
    }
    response=render(request,"delivery_man/orders.html",context)
    return response

@login_required(login_url='/users/login/')   
def pick_order(request,order_id):
    """
    params:
    1-order_id
    return success
"""
    if request.user.is_delivery_man:
        #get the delivery man
        deliveryman=DeliveryMan.objects.get(user=request.user)
        #check if the delivery man has outstanding orders
        if Order.objects.filter(driver=deliveryman,status=Order.ONTHEWAY):
            messages.info(request,_('your outstanding order is not delivered yet'))
            return redirect('delivery_man:deliverys')
        
                    
        #processing the picking up order
        try:
            order=Order.objects.get(id=order_id,
            driver=None,
            status=Order.READY)
            Drivers=DeliveryMan.objects.all()
            dist=[]
            driver_list=[]
            for driver in Drivers:
                driver_list.append(driver)
                dist.append(distance_calc([float(driver.long),float(driver.lat)],[float(order.restaurent.long),float(order.restaurent.lat)]))
            index=dist.index(min(dist))
            target=driver_list[index]
            # print(index)
            # print(driver_list)
            # print(dist)
            # print(target)
            if deliveryman==target:
                order.driver=target
                if order.driver.user == order.customer:
                        messages.info(request,_("can't do that"))
                        return redirect('core:home')
            else:
                messages.info(request,_('your a bit to far'))
                return redirect('delivery_man:account')
            

            order.status=Order.ONTHEWAY
            order.picked_at=timezone.now()
            order.save()
           
        except Order.DoesNotExist:
            messages.warning(request,_('this order has been picked up by another driver'))
            return redirect('delivery_man:account')
        return redirect('delivery_man:deliverys')
    else:
        return redirect('delivery_man:signup')

@csrf_exempt
@login_required(login_url='/users/login/')   
def deliverys(request):
    if request.user.is_delivery_man:
        try:
            mapbox_api=os.environ.get('MAPBOX_API_KEY')
            driver=DeliveryMan.objects.get(user=request.user)
            order=Order.objects.get(driver=driver,status=Order.ONTHEWAY)
            if request.method=="POST":
                    driver.lat=request.POST['lat']
                    driver.long=request.POST['long']
                    driver.save()
            
            restaurent_address=[float(order.restaurent.long),float(order.restaurent.lat)]#geotransformer(order.restaurent.address_exacte)
            cutomer_address=order.address.address
            driver_address=[float(driver.long),float(driver.lat)]
            context={
               'access_token':mapbox_api,
                'driver_address':driver_address,
                'restaurent_address':restaurent_address,
                'cutomer_address':cutomer_address,
                'order':order
            }
        except Order.DoesNotExist:
            messages.info(request,_('there  is no  avaliable deliverys'))
            return redirect('delivery_man:account')

        return render(request,'delivery_man/deliverys.html',context)
    else:
        messages.error(request,_("can't go there"))
        return redirect('delivery_man:signup')
        

@login_required(login_url='/users/login/')   
def complete_order(request,pk):
    if request.user.is_delivery_man:
        #get the driver
        driver=DeliveryMan.objects.get(user=request.user)
        #get the order to complete
        order=Order.objects.get(id=pk,
        driver=driver,)
        order.status=Order.DELIVERED
        order.save()
        messages.success(request,_('success'))
        return redirect('delivery_man:account')
    else:
        messages.error(request,_("can't go there"))
        return redirect('delivery_man:signup')



# def get_revenue(request):
#     driver=DeliveryMan.objects.get(user=User.objects.get(id=1))
#     revenue = {}
#     today = timezone.now()
#     from datetime import timedelta
#     current_weekdays = [today + timedelta(days = i) for i in range(0 - today.weekday(), 7 - today.weekday())]

#     for day in current_weekdays:
#         orders = Order.objects.filter(
#         driver = driver,
#         status = Order.DELIVERED,
#         created_at__year = day.year,
#         created_at__month = day.month,
#         created_at__day = day.day,
#         )

#         revenue[day.strftime("%a")] = sum(order.total for order in orders)

#     return JsonResponse({
#         "revenue": revenue
#     })



    
