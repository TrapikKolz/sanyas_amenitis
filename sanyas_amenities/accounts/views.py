from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.shortcuts import render
from django.http import HttpResponse
from accounts.models import User

@receiver(user_logged_in)
def got_online(sender, user, request, **kwargs):
    request.user.is_active = True
    request.user.save()

@receiver(user_logged_out)
def got_offline(sender, user, request, **kwargs):
    request.user.is_active = False
    request.user.save()

def index(request):
    user = User.objects.filter(pk=1)
    is_active = user[0].is_active
    return HttpResponse(is_active)



