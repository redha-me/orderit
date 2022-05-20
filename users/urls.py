from django.urls import path
from . import views

app_name='users'
urlpatterns=[
    path('signup/', views.SignUpView.as_view(),name='signup'),
    path('login/', views.LoginView.as_view(),name='login'),
    path('logout/',views.log_out,name="logout"),
    path('verify/<str:key>', views.complete_verification,name='complete-verification'),
    path('order/add_order/',views.add_order,name='add'),
    path('deliverys/',views.deliverys,name='deliverys'),
    path('update_delivery_menu/',views.update_delivery_menu,name="update"),
    path('account/<int:pk>/',views.Account.as_view(),name="account"),
    path('accountupdate/',views.AccountUpdate.as_view(),name="accountupdate"),
    path('UpdatePassword/',views.UpdatePassword.as_view(),name='updatepassword'),
    path('driverPosition/',views.update_driver_postision,name='updatedv'),
    # path('order/latest_status/', views.get_latest_order_status),
]
