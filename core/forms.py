from django import forms
from core.models import Wilaya,Commune
from dynamic_forms import DynamicField,DynamicFormMixin



class addressForm(DynamicFormMixin,forms.Form):
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
    address=forms.CharField( max_length=120,required=False)
  

  
    
  

