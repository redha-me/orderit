import os
from django.db import models
from django.dispatch import receiver
from users.models import User


days=(	
  ("Everyday","Everyday"),
	("Saturday","Saturday"),
	("Friday","Friday"),
	("Thursday","Thursday"),
	("Wednesday","Wednesday"),
	("Tuesday","Tuesday"),
	("Monday","Monday"),
	("Sunday","Sunday"),)

class DeliveryMan(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    nom=models.CharField(max_length=100,blank=True,null=True)
    avatar = models.ImageField(upload_to="driver_avatars", blank=True)
    plate_number = models.IntegerField(null=True, blank=True)
    prenom=models.CharField(max_length=100,blank=True,null=True)
    wilaya=models.CharField(max_length=100,blank=True,null=True)
    commune=models.CharField(max_length=100,blank=True,null=True)
    mobile=models.CharField(max_length=100,blank=True,null=True)
    email=models.EmailField()
    moyen_de_livraison=models.CharField(max_length=100,blank=True,null=True)
    heur_debut_desponible=models.TimeField()
    heur_fin_desponible=models.TimeField()
    jour_desponibilite=models.CharField(choices=days ,max_length=100,blank=True,null=True)
    # location = models.CharField(max_length=255, blank=True)
    lat=models.CharField(null=True,blank=True,max_length=120)
    long=models.CharField(null=True,blank=True,max_length=120)
    

    def __str__(self):
        return f'{self.nom}-{self.prenom}'
@receiver(models.signals.post_delete, sender=DeliveryMan)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.avatar:
        if os.path.isfile(instance.avatar.path):
            os.remove(instance.avatar.path)

class Delivery_mean(models.Model):
    name=models.CharField(max_length=15,blank=False)

    def __str__(self):
        return self.name