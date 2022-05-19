from django.contrib import admin
from . import models


admin.site.register(models.MenuItem)
admin.site.register(models.Order)
admin.site.register(models.OrderDetails)
# admin.site.register(models.Restaurent)
admin.site.register(models.Restaurent_owner)
admin.site.register(models.Type_cuisine)
admin.site.register(models.Type_Resturent)


@admin.register(models.Restaurent)
class RoomAdmin(admin.ModelAdmin):
    list_filter = (
       'user',
    )
    search_fields = ("^user","^restaurent_owner")