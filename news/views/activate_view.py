from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode

from news.models import User
from news.views.tokens import account_activation_token


def account_activation_sent(request):
    return render(request, 'news/account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'news/account_activation_invalid.html')
