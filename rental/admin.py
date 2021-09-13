from django.contrib import admin
from .models import *

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

class RentProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'publisher', 'author', 'total', 'stock', 'available_display', 'available_order',
                    'created', 'updated']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['total', 'stock', 'available_display', 'available_order']

class RentalAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'address', 'bookid', 'title', 'publisher', 'author', 'rentdate', 'expdate', 'created']
    list_editable = ['rentdate', 'expdate']

class ReserveAdimn(admin.ModelAdmin):
    list_display = ['custnum', 'bookid', 'applydate', 'exrent']

admin.site.register(Rentbook, RentProductAdmin)
admin.site.register(Rentcategory, CategoryAdmin)
admin.site.register(Rental, RentalAdmin)
admin.site.register(Reservation, ReserveAdimn)