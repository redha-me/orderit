from django import forms
from . import models
from core.models import Hour,Wilaya,Commune
from dynamic_forms import DynamicField,DynamicFormMixin
from django.utils.translation import gettext_lazy as _


days=(	
  ("Everyday",_("Everyday")),
	("Saturday",_("Saturday")),
	("Friday",_("Friday")),
	("Thursday",_("Thursday")),
	("Wednesday",_("Wednesday")),
	("Tuesday",_("Tuesday")),
	("Monday",_("Monday")),
	("Sunday",_("Sunday")),)
    

class DeliverySignup(DynamicFormMixin,forms.Form):
    def commune_choices(form):
        wilaya=form['wilaya'].value()
        return Commune.objects.filter(wilaya=wilaya)
    
    def initial_commune(form):
        wilaya=form['wilaya'].value()
        return Commune.objects.filter(wilaya=wilaya).first()
        
    
    wilaya=forms.ModelChoiceField(
        queryset=Wilaya.objects.all(),
        initial=Wilaya.objects.first())
    commune=DynamicField(
        forms.ModelChoiceField,
        queryset=commune_choices,
        initial=initial_commune,
    )
    nom=forms.CharField( max_length=100)
    prenom=forms.CharField()
    avatar=forms.ImageField()
    plate_number=forms.IntegerField()
    mobile=forms.CharField()
    email=forms.EmailField()
    moyen_de_livraison=forms.ModelChoiceField(queryset=models.Delivery_mean.objects.all())
    heur_debut_desponible=forms.ModelChoiceField(queryset=Hour.objects.all())
    heur_fin_desponible=forms.ModelChoiceField(queryset=Hour.objects.all())
    jour_desponibilite=forms.ChoiceField(choices=days)
    
  
    
    # '''so what this does it  making the field of communr empty'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['commune'].queryset = cl.models.City.objects.none()
        # self.fields['commune_travialle'].queryset = cl.models.City.objects.none()
        self.fields['jour_desponibilite'].label='Horaire de disponibilité'
        

    
   