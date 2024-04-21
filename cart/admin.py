from django.contrib import admin
from .models import Delivery


class DeliveryAdmin(admin.ModelAdmin):
    list_display = ['name', 'cost', 'free_shipping', 'free_shipping_amount']


admin.site.register(Delivery, DeliveryAdmin)
