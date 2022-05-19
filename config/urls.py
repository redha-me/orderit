from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls import handler404
from core import views as core_views


urlpatterns =[
    path('i18n/', include('django.conf.urls.i18n')),

]
urlpatterns +=i18n_patterns( 
    path('admin/', admin.site.urls),
    path('',include('core.urls',namespace='core')),
    path('users/',include('users.urls',namespace='users')),
    path('delivery_man/',include('delivery_man.urls',namespace='delivery_man')),
    path('restaurent/',include('partner_restaurent.urls',namespace='restraurent')),
    path('cart/',include('cart.urls',namespace='cart')),

)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

handler404=core_views.handel_404