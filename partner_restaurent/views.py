from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect,render,reverse
from django.views.generic.edit import UpdateView
from django.views.generic import FormView
from django.urls import reverse_lazy
from . import models,forms,mixins
from django.views.generic import ListView,DetailView,FormView
from django.http import HttpResponse, JsonResponse
from .models import MenuItem, Order, Restaurent,Restaurent_owner
from users.models import User
from partner_restaurent import models
from django.contrib import messages
from .forms import MealForm
from django.utils.translation import gettext_lazy as _




class DishCreate(mixins.RegistredPartnerOnly,FormView):
    form_class = forms.CreateFoodForm
    template_name = "restaurent/dish_create.html"
    def form_valid(self, form):
        food = form.save()
        food.restaurent = Restaurent.objects.get(user=self.request.user)
        food.save()
        return redirect(reverse("restaurent:meals" ,kwargs={'pk' : self.request.user.pk}))
    def get(self, request, *args, **kwargs):
        if self.request.method == 'GET':
            messages.error(self.request,_("can't go there"))
            return redirect('core:home')




@csrf_exempt
@login_required(login_url='/users/login/')
def DishUpdate(request,pk): 
    if request.method == "POST":    
        meal_form = MealForm(request.POST, request.FILES, instance=MenuItem.objects.get(id=pk))

        if meal_form.is_valid():
            meal_form.save()
            pk=request.user.pk
            return redirect('restaurent:meals',pk)
    else:
        if not request.user.is_partner:
            return redirect('restaurent:signup')
        else:
            messages.error(request,_("can't go there"))
            return redirect('core:home')
    meal_form = MealForm(instance=MenuItem.objects.get(id=pk))
    return render(request, 'restaurent/dish_update.html', {
    "form": meal_form,
    'pk':pk})


  
@login_required(login_url='/users/login/')
def DishDelete(request,pk):
    if request.method == "POST":
        item=MenuItem.objects.filter(pk=pk).delete()
        pk=request.user.pk
        return redirect('restaurent:meals',pk)
    else:
        if not request.user.is_partner:
            return redirect('restaurent:signup')
        else:
            messages.error(request,_("can't go there"))
            return redirect('core:home')

   

        
class DishDetail(mixins.LoggedInOnly,DetailView):
    model= models.Restaurent
    context_object_name='restaurent'
    template_name='restaurent/dish_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menuitem']=models.MenuItem.objects.all()
        return context
    def get_success_url(self):
        next_url=self.request.GET.get('next')
        if next_url is not None:
            return next_url
        else:
            return reverse('core:home')
    


class HomeView(mixins.LoggedInOnly,ListView):
    model= models.Restaurent
    template_name='core/store.html'
    paginate_by=9
    ordering='name'
    context_object_name='restaurents'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['restaurents']=Restaurent.objects.all().exclude(user=self.request.user)
        return context
    


        

class  SignUpView(mixins.SignUpPartnerOnly,FormView):
    template_name='restaurent/signup.html'
    form_class=forms.PartenerSignup
    success_url=reverse_lazy('core:home')
    def form_valid(self, form):
        Nom=form.cleaned_data.get('Nom')
        logo=form.cleaned_data.get('logo')
        lat=form.cleaned_data.get('lat')
        long=form.cleaned_data.get('long')
        # type_res=form.cleaned_data.get('type_res')
        res_owner_nom=form.cleaned_data.get('res_owner_nom')
        res_owner_prenom=form.cleaned_data.get('res_owner_prenom')
        mobile=form.cleaned_data.get('mobile')
        email=form.cleaned_data.get('email')
        wilaya=form.cleaned_data.get('wilaya')
        commune=form.cleaned_data.get('commune')
        heur_debut_desponible=form.cleaned_data.get('heur_debut_desponible')
        heur_fin_desponible=form.cleaned_data.get('heur_fin_desponible')
        jour_desponibilite=form.cleaned_data.get('jour_desponibilite')
        # adresse_exacte=form.cleaned_data.get('adresse_exacte')
        user=User.objects.get(username=self.request.user)
        if user is not None:
            user.is_partner=True
            user.save()
            restaurent_owner=Restaurent_owner.objects.create(nom=res_owner_nom,prenom=res_owner_prenom)
            Restaurent.objects.create(logo=logo,name=Nom,user=user,restaurent_owner=restaurent_owner,mobile=str(mobile),email=str(email),heur_debut_desponible=str(heur_debut_desponible),heur_fin_desponible=str(heur_fin_desponible),jour_desponibilite=str(jour_desponibilite),wilaya=str(wilaya),commune=str(commune),lat=str(lat),long=str(long))
        return super().form_valid(form)

@csrf_exempt
@login_required(login_url='/users/login/')
def load_commune(request):
    if request.method == "POST":
        form=forms.PartenerSignup(request.POST)
        return HttpResponse(form['commune'])
    else:
        return redirect('core:home')

@login_required(login_url='/users/login/')
def  dashbord(request):
    if request.user.is_partner:
        restaurent=Restaurent.objects.get(user=request.user)
        menuitem=MenuItem.objects.all().filter(restaurent=restaurent)
        context={'restaurent':restaurent,
        }
        return render(request,"restaurent/sidebar.html",context)
    else:
        messages.error(request,_("can't go there"))
        return redirect('restaurent:signup')


@login_required(login_url='/users/login/')
def dishs(request,pk):
    if request.user.is_partner:
        user=User.objects.get(pk=pk)
        restaurent=Restaurent.objects.get(user=user)
        menuitem=MenuItem.objects.all().filter(restaurent=restaurent)
        food=menuitem.all()
        context={'foods':food,'restaurent':restaurent}
        return render(request,"restaurent/dishs.html",context)
    else:
        return redirect('restaurent:signup')

@login_required(login_url='/users/login/')
def search(request):
    if request.method == "POST":
        search_text=request.POST.get('search')
        if len(search_text)>=1 and search_text!= ' ':
            results=Restaurent.objects.filter(name__icontains=search_text)
            context={'results':results,'restaurents':results}
            # menu=MenuItem.objects.all()
        else:
            results=None
            context={'results':results,'restaurents':results}

        
        return render(request,'partiels/search_results.html',context)
    else:
        return redirect('core:home')


@csrf_exempt
@login_required(login_url='/users/login/')     
def get_search(request):
    if request.method == "POST":
       return render(request,'partiels/search.html')
    else:
       return redirect('core:home')

class AccountUpdate(mixins.RegistredPartnerOnly,UpdateView):
    model=models.Restaurent
    fields=['logo','name','mobile','email','heur_debut_desponible','heur_fin_desponible','jour_desponibilite','wilaya','commune',]
    template_name='restaurent/accountUpdate.html'
    def get_success_url(self):
        messages.success(self.request,_('successfully updated'))
        return reverse_lazy('restaurent:account')
    def get_object(self ):
        return Restaurent.objects.get(user=self.request.user)
    
        
@login_required(login_url='/users/login/')
def Account(request):
    if request.user.is_partner:
        restaurent=Restaurent.objects.get(user=request.user)
        context={
            'restaurent':restaurent
        }
        return render(request,'restaurent/account.html',context)
    else:
        return redirect('restaurent:signup')

@login_required(login_url='/users/login/')
def orders(request):
    if  request.user.is_partner:
        if request.method == "POST":
            order = Order.objects.get(id=request.POST["id"])
            if order.status == Order.COOKING:
                order.status = Order.READY
                order.save()
        restaurent=Restaurent.objects.get(user=request.user)
        orders=Order.objects.filter(restaurent=restaurent)
        context={
            "orders":orders  ,"restaurent":restaurent  }
        response=render(request,'restaurent/orders.html',context)
        return response
    else:
        messages.error(request,_("can't go there"))
        return redirect('restaurent:signup')

@csrf_exempt
@login_required(login_url='/users/login/')
def restaurant_order_notification(request, last_request_time):
    if request.method == 'POST':
        restaurent=Restaurent.objects.get(user=request.user)
        notification = Order.objects.filter(
            restaurent = restaurent, 
            created_at__gt = last_request_time
        ).count()
        return JsonResponse({'notification':notification})
    else:
        return redirect('core:home')

@login_required(login_url='/users/login/')
def search_by_citys(request,city):
    results=Restaurent.objects.filter(wilaya__icontains=city)
    context={'restaurents':results}
    return render(request,'core/store.html',context)



