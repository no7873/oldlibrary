from django.contrib import admin
from .models import *

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

class ProductAdmin(admin.ModelAdmin):
    list_display=['btitle', 'bpublisher', 'bauthor', 'slug', 'bcategory', 'bcon', 'bstock', 'available_display', 'available_order', 'created', 'updated']
    prepopulated_fields = {'slug': ('btitle',)}
    list_editable =['bcon', 'bstock', 'available_display', 'available_order']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)