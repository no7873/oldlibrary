from django.urls import path
from .views import *

app_name = 'shop'

urlpatterns = [
    path('', buybook_in_category, name='buybook_all'),
    # path('<slug:category_slug>/', product_in_category, name='product_on_category'),
    path('<category_slug>/', buybook_in_category, name='buybook_in_category'),
    path('<int:id>/<product_slug>/', buybook_detail, name='buybook_detail'),
]