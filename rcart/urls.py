from django.urls import path
from .views import *

app_name = 'rcart'

urlpatterns=[
    path('', cart_detail, name='rdetail'),
    path('radd/<int:product_id>', add_cart, name='rproduct_add'),
    path('remove/<product_id>', cart_remove, name='rproduct_remove'),
]
