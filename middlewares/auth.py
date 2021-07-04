from users.models import Users
from django.http import HttpResponseNotAllowed
from django.shortcuts import redirect
from django.contrib.auth import logout

def verify_student(request):
    try:
        current_user = Users.objects.all().get(user=request.user)
        if not current_user.role == 'S':
            return HttpResponseNotAllowed()  
    except:
        return HttpResponseNotAllowed()

def verify_teacher(request):
    try:
        current_user = Users.objects.all().get(user=request.user)
        if current_user.role == 'T':
            return True
        else:
            return False
    except:
        return False

def verify_login(request):
    return request.user.is_authenticated
        

