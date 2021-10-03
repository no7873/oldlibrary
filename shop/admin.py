from django.contrib import admin
from .models import *

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

class BuyProductAdmin(admin.ModelAdmin):
    list_display=['btitle', 'slug', 'bcategory', 'bpublisher', 'bauthor', 'bcontent', 'condition', 'price', 'btotal', 'bstock',
                  'available_display', 'available_order', 'created', 'updated']
    prepopulated_fields = {'slug': ('btitle',)}
    list_editable =['price', 'condition', 'btotal', 'bstock', 'available_display', 'available_order']

admin.site.register(Buycategory, CategoryAdmin)
admin.site.register(Buybook, BuyProductAdmin)