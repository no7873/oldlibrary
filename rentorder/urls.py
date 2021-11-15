from django.urls import path
from .views import *

app_name = 'rentorders'

urlpatterns = [
    path('create/', rent_create, name='rent_create'),
    path('create_ajax/', RentCreateAjaxView.as_view(), name='rent_create_ajax'),
    path('checkout/', RentCheckoutAjaxView.as_view(), name='rent_checkout'),
    path('validation/', RentImpAjaxView.as_view(), name='rent_validation'),
    path('complete/', rent_complete, name='rent_complete'),
    path('admin/rent/<int:order_id>/', admin_rent_detail, name='admin_rent_detail'),
    path('admin/rent/<int:order_id>/pdf/', admin_rent_pdf, name='admin_rent_pdf'),

    # path('point/', point_order, name='point_order'),
]