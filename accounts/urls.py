from django.urls import path
from django.contrib.auth import views as auth_view
from .views import signup, id_overlap_check
from . import views

urlpatterns=[
    path('login/', auth_view.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_view.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('signup/check/', id_overlap_check, name='id_overlap_check'),
]