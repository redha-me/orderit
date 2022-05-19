from django import forms
from .models import Type_cuisine ,Type_Resturent,MenuItem
from core.models import Wilaya,Commune,Hour,Day
from dynamic_forms import DynamicField,DynamicFormMixin

from partner_restaurent import models


class PartenerSignup(DynamicFormMixin,forms.Form):
    def commune_choices(form):
        wilaya=form['wilaya'].value()
        return Commune.objects.filter(wilaya=wilaya)
    
    def initial_commune(form):
        wilaya=form['wilaya'].value()
        return Commune.objects.filter(wilaya=wilaya).first()

    Nom=forms.CharField(max_length=30)
    lat=forms.CharField(max_length=30)
    long=forms.CharField(max_length=30)
    # type_res=forms.MultipleChoiceField(
    #     choices=Type_Resturent.objects.values_list('name','name'))
    logo=forms.ImageField(required=True)
    res_owner_nom=forms.CharField(max_length=30)
    res_owner_prenom=forms.CharField(max_length=30)
    mobile=forms.CharField(max_length=10)
    email=forms.CharField(max_length=40)
    # type_cuisine=forms.MultipleChoiceField(
    #     choices=Type_cuisine.objects.values_list('name','name'))
    wilaya=forms.ModelChoiceField(
        queryset=Wilaya.objects.all(),
        initial=Wilaya.objects.first())
    commune=DynamicField(
        forms.ModelChoiceField,
        queryset=commune_choices,
        initial=initial_commune,
    )
    # adresse_exacte=forms.CharField()
    # Page Facebook
    #Page Instagram
    heur_debut_desponible=forms.ModelChoiceField(queryset=Hour.objects.all())
    heur_fin_desponible=forms.ModelChoiceField(queryset=Hour.objects.all())
    jour_desponibilite=forms.ModelChoiceField(queryset=Day.objects.all())
    #photo:logo
    
  
    
    # '''so what this does it  making the field of communr empty'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['jour_desponibilite'].label='Horaires de Travail'
        self.fields['Nom'].label="Facility Name"
        self.fields['res_owner_nom'].label='Restaurent_owner_FirstName'
        self.fields['res_owner_prenom'].label='Restaurent_owner_LastName'
        # self.fields['type_res'].label='Restaurent Type'

class CreateFoodForm(forms.ModelForm):
    class Meta:
        model = models.MenuItem
        fields = (
            "name",
            "description",
            "price",
            "photo",)

    def save(self, *args, **kwargs):
        food = super().save(commit=False)
        return food

class MealForm(forms.ModelForm):
  class Meta:
    model = MenuItem
    exclude = ("restaurent",)