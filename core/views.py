import os
from django.http import HttpResponse
from django.shortcuts import render
from core import forms
from mapbox import Directions
from django.contrib.auth.decorators import login_required

from partner_restaurent.models import Restaurent


def distance_calc(origin,distination):
    mapbox_api=os.environ.get('MAPBOX_API_KEY')
    resp=Directions(access_token=mapbox_api).directions([origin,distination])
    resp=resp.json()
    resp=resp['routes'][0]['distance']
    resp=resp/1000
    return resp

def load_commune(request):
    form=forms.addressForm(request.GET)
    return HttpResponse(form['commune'])

def handel_404(request,*args, **kwargs):
    return render(request,'404.html')


    
# def geotransformer(address):
#     mapbox_api=os.environ.get('MAPBOX_API_KEY')
#     g = geocoder.mapbox(address, key=mapbox_api)
#     g = g.latlng
#     print()  
#     lat = g[0]
#     long = g[1]
#     return [long,lat]
    
