from django.urls import path
from . import views
app_name='delivery_man'
urlpatterns = [
    path('signup/',views.SignUpView.as_view(),name='signup'),
    path('signup/commune/', views.load_commune, name='commune'),
    path('dashbord/',views.dashbord,name='home'),
    path('order/ready/', views.get_ready_orders,name='readyOrder'),
    path('order/pick/<int:order_id>', views.pick_order,name='orderPick'),
    path('order/deliverys/',views.deliverys,name='deliverys'),
    # path('order/latest/', views.get_latest_order),
    path('order/complete/<int:pk>', views.complete_order,name='complete'),
    # path('revenue/', views.get_revenue),
    # path('location/update/', views.update_location,name='updateLocation'),
    path('profile/', views.driver_get_profile,name='account'),#to know info about the driver and his delivery_mean
    path('profile/update/', views.driver_update_profile.as_view(),name='account-update')
    
]
