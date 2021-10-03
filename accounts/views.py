from django.shortcuts import render
from .models import User
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

# Create your views here.
def signup(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['password2']:
            user = User.objects.create_user(
                username=request.POST['username'],
                password=request.POST['password'],
                email=request.POST['email'],
                nickname=request.POST['nickname'],
                address=request.POST['address'],
                detailadd=request.POST['detailadd'],
                phone=request.POST['phone'],
            )
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('/')
        return render(request, 'registration/signup.html')
    else:
        form = UserCreationForm
        return render(request, 'registration/signup.html', {'form': form})