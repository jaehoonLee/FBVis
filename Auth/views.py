from django.shortcuts import redirect
from django.contrib.auth import logout, login, authenticate
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User


@csrf_exempt
def web_register(request):

    user = User.objects.create_user(username=request.POST['username'], email=request.POST['email'], password=request.POST['password'])
    user.save()

    user = authenticate(username=request.POST['username'], password=request.POST['password'])
    if user is not None:
        login(request, user)

    return redirect('/')

@csrf_exempt
def web_login(request):
    user = authenticate(username=request.POST['username'], password=request.POST['password'])
    if user is not None:
        login(request, user)

    return redirect('/')

@csrf_exempt
def web_logout(request):
    logout(request)
    return redirect('/')
