from django.urls import path
from . import views

app_name='restaurent'
urlpatterns=[
        path('dashbord/create-dish/',views.DishCreate.as_view(),name='create'),
        path('dashbord/update-dish/<str:pk>',views.DishUpdate,name='update'),
        path('dashbord/delete-dish/<str:pk>',views.DishDelete,name='delete'),
        path('dashbord/account-update',views.AccountUpdate.as_view(),name='account-update'),
        path('dashbord/account',views.Account,name='account'),
        path('dashbord/orders',views.orders,name='orders'),
        path('dashbord/<int:pk>/meals',views.dishs,name='meals'),
        path('<str:pk>',views.DishDetail.as_view(),name='detail'),
        path('signup/',views.SignUpView.as_view(),name='signup'),
        path('signup/commune/', views.load_commune, name='commune'),
        path('dashbord/',views.dashbord,name='home'),
        path('searchByCity/<str:city>',views.search_by_citys,name='searchc'),
        path('orders/notification/<last_request_time>/',views.restaurant_order_notification,name='notification'),

]
