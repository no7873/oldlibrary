from django.contrib import admin

# Register your models here.
import csv
import datetime
from django.http import HttpResponse

def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename={}.csv'.format(opts.verbose_name)
    response.write(u'/ufeff'.encode('utf8'))

    writer = csv.writer(response)

    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]

    writer.writerow([field.verbose_name for field in fields])

    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime("%Y-%m-%d")
            data_row.append(value)
        writer.writerow(data_row)
    return response

export_to_csv.short_description = 'Export to CSV'

from django.urls import reverse
from django.utils.safestring import mark_safe

def rent_detail(obj):
    return mark_safe('<a href="{}">Detail</a>'.format(reverse('rentorders:admin_rent_detail', args=[obj.id])))

rent_detail.short_description = 'Detail'

def rent_pdf(obj):
    return mark_safe('<a href="{}">PDF</a>'.format(reverse('rentorders:admin_rent_pdf', args=[obj.id])))

rent_pdf.short_description = 'PDF'

from .models import RentItem, Rent

class RentItemInline(admin.TabularInline):
    model = RentItem
    raw_id_fields = ['product']

class RentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'address', 'detailadd', 'phone', 'paid', rent_detail, rent_pdf, 'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [RentItemInline]
    actions = [export_to_csv]

admin.site.register(Rent, RentAdmin)