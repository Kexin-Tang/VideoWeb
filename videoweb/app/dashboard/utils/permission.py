import functools
from django.shortcuts import render, redirect, reverse

def dashboardAuth(func):
    @functools.wraps(func)
    def wrapper(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return redirect('{}?to={}'.format(reverse('dashboard_login'), request.path))
        return func(self, request, *args, **kwargs)
    return wrapper