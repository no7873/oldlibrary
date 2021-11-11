from django.http import JsonResponse
from django.shortcuts import render

from .forms import RegisterForm
from .models import User
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

# Create your views here.
def signup(request):
    register_form = RegisterForm(request.POST)
    context = {'form':register_form}
    if request.method == 'POST':
        if register_form.is_valid():
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
        return render(request, 'registration/signup.html', context)
    else:
        context['form'] = register_form
        return render(request, 'registration/signup.html', context)

def id_overlap_check(request):
    username = request.GET.get('username')
    try:
        user=User.objects.get(username=username)
    except:
        user = None
    if user is None:
        overlap = 'pass'
    else:
        overlap = "fail"
    context = {'overlap':overlap}
    return JsonResponse(context)