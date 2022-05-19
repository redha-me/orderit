from django.contrib import admin
from .models import Address,Hour,Wilaya,Commune

# admin.site.register(Day)
admin.site.register(Hour)
admin.site.register( Wilaya)
admin.site.register( Commune)
admin.site.register(Address)
