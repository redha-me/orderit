import os
from django.db import models
from users.models import User
from django.urls import reverse
from django.db.models.signals import post_delete
from django.dispatch import receiver
from delivery_man.models import DeliveryMan
from django.utils import timezone
from core.models import Address
from django.utils.translation import gettext_lazy as _


class Type_cuisine(models.Model):
    name = models.CharField(max_length=100,)

    def __str__(self):
        return self.name


class Type_Resturent(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name
class Restaurent_owner(models.Model):
	nom=models.CharField(max_length=100,blank=True,null=True)
	prenom=models.CharField(max_length=100,blank=True,null=True)
	def __str__(self):
		return f'{self.nom}-{self.prenom}'
days=(	
  ("Everyday",_("Everyday")),
	("Saturday",_("Saturday")),
	("Friday",_("Friday")),
	("Thursday",_("Thursday")),
	("Wednesday",_("Wednesday")),
	("Tuesday",_("Tuesday")),
	("Monday",_("Monday")),
	("Sunday",_("Sunday")),)

class Restaurent(models.Model):
	user=models.ForeignKey(User, on_delete=models.CASCADE,null=True,related_name='restaurent')
	logo=models.ImageField(upload_to='restaurent_logo',null=True, blank=True)
	restaurent_owner=models.ForeignKey(Restaurent_owner,on_delete=models.CASCADE,blank=True,null=True)
	# address_exacte= models.CharField(max_length=200, null=False)
	name=models.CharField(max_length=30,null=True)
	mobile=models.CharField(max_length=200, null=False)
	email=models.EmailField()
	# type_restaurent=models.CharField(max_length=200,blank=True,null=True)
	heur_debut_desponible=models.TimeField(blank=True,null=True)
	heur_fin_desponible=models.TimeField(blank=True,null=True)
	jour_desponibilite=models.CharField(choices=days ,max_length=100,blank=True,null=True)
	wilaya=models.CharField(max_length=100,blank=True,null=True)
	commune=models.CharField(max_length=100,blank=True,null=True)
	lat=models.CharField(null=True,blank=True,max_length=120)
	long=models.CharField(null=True,blank=True,max_length=120)
	# menu=models.ForeignKey(MenuItem,on_delete=models.CASCADE,null=True)

	def get_absolute_url(self):
		return reverse('restaurent:detail',kwargs={"pk":self.pk})


	def __str__(self):
		return str(self.name)
@receiver(models.signals.post_delete, sender=Restaurent)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.logo:
        if os.path.isfile(instance.logo.path):
            os.remove(instance.logo.path)
	
class MenuItem(models.Model):
	name=models.CharField(max_length=200)
	price=models.FloatField()
	description=models.TextField(("description"), blank=True)
	photo=models.ImageField(upload_to='dish_photos' ,null=True, blank=True)
	# Type_cuisine = models.ManyToManyField(Type_cuisine)
  
	restaurent=models.ForeignKey(Restaurent,on_delete=models.CASCADE, null=True,related_name="res")
	
	def __str__(self):
		return self.name

@receiver(models.signals.post_delete, sender=MenuItem)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.photo:
        if os.path.isfile(instance.photo.path):
            os.remove(instance.photo.path)
	



class Order(models.Model):
  COOKING = 1
  READY = 2
  ONTHEWAY = 3
  DELIVERED = 4

  STATUS_CHOICES = (
    (COOKING, _("Cooking")),
    (READY, _("Ready")),
    (ONTHEWAY, _("On the way")),
    (DELIVERED, _("Delivered")),
  )

  customer = models.ForeignKey(User, on_delete=models.PROTECT,blank=True, null=True)
  restaurent = models.ForeignKey(Restaurent, on_delete=models.PROTECT,blank=True, null=True)
  driver = models.ForeignKey(DeliveryMan, models.SET_NULL, blank=True, null=True)
  address = models.OneToOneField(Address,on_delete=models.CASCADE,max_length=500,blank=True, null=True)
  total = models.IntegerField(blank=True, null=True)
  status = models.IntegerField(choices=STATUS_CHOICES,blank=True, null=True)
  created_at = models.DateTimeField(default=timezone.now)
  picked_at = models.DateTimeField(blank=True, null=True)

  def __str__(self):
    return str(self.id)

class OrderDetails(models.Model):
  order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='order_details',blank=True, null=True)
  meal = models.ForeignKey(MenuItem, on_delete=models.PROTECT,blank=True, null=True)
  quantity = models.IntegerField(blank=True, null=True)
  sub_total = models.IntegerField(blank=True, null=True)

  def __str__(self):
    return str(self.id)

