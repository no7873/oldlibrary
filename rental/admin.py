from django.contrib import admin
from .models import *

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

class RentProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'rtitle', 'slug', 'rcategory', 'rpublisher', 'rauthor', 'rtotal', 'rstock', 'available_display', 'available_order',
                    'created', 'updated']
    prepopulated_fields = {'slug': ('rtitle',)}
    list_editable = ['rtotal', 'rstock', 'available_display', 'available_order']

class RentalAdmin(admin.ModelAdmin):
    list_display = ['cust_num', 'phone', 'address', 'rbook_id', 'rent_date', 'due', 'rental_state', 'overdue', 'created']
    list_editable = ['rent_date', 'due']

class ReserveAdimn(admin.ModelAdmin):
    list_display = ['cust_num', 'rbook_id', 'apply', 'exp']

admin.site.register(Rentbook, RentProductAdmin)
admin.site.register(Rentcategory, CategoryAdmin)
admin.site.register(Rental, RentalAdmin)
admin.site.register(Reservation, ReserveAdimn)