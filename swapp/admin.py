from django.contrib import admin
from .models import *


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'seller',  'price', 'sold', 'checked')


# Register your models here.
admin.site.register(Item, ItemAdmin)
admin.site.register(Event)
admin.site.register(Checkout)
admin.site.register(Announcement)
