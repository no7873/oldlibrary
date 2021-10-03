from django.urls import path
from .views import *

app_name = 'rental'

urlpatterns = [
    path('rentbook_all/', rentbook_in_category, name='rentbook_all'),
    path('<category_slug>/', rentbook_in_category, name='rentbook_in_category'),
    path('<int:id>/<product_slug>/', rentbook_detail, name='rentbook_detail'),
    path('reserve/<int:id>/', reserve, name='reserve'),
    path('rental/<int:id>', rental, name='rental'),
]