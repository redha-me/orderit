from django.urls import path,include
from partner_restaurent import views
from . import views as v
app_name='core'
urlpatterns = [
path('',views.HomeView.as_view(),name='home'),
path('search/', views.search, name='search'),
path('get-search/', views.get_search, name='get_search'),
path('commune/',views.load_commune,name='commune'),


]
