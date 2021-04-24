import functools
from django.shortcuts import render, redirect, reverse
from app.const.const import COOKIES_NAME, SESSION_NAME
from django.contrib.auth.models import User

'''
    判断用户是否已经登录，封装为装饰器
'''
def dashboardAuth(func):
    @functools.wraps(func)
    def wrapper(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return redirect('{}?to={}'.format(reverse('dashboard_login'), request.path))
        return func(self, request, *args, **kwargs)
    return wrapper


'''
    使用COOKIE判断用户是否已经登录
'''
def checkLoginByCookies(func):
    @functools.wraps(func)
    def wrapper(self, request, *args, **kwargs):
        id = request.COOKIES.get(COOKIES_NAME)
        if not id:
            return redirect('{}?to={}'.format(reverse('dashboard_login'), request.path))

        user = User.objects.filter(pk=id).exists()
        if user:
            return func(self, request, *args, **kwargs)
        else:
            return redirect('{}?to={}'.format(reverse('dashboard_login'), request.path))
    return wrapper


'''
    使用SESSION判断用户是否登录
'''
def checkLoginBySession(func):
    @functools.wraps(func)
    def wrapper(self, request, *args, **kwargs):
        status = request.session.get('is_login')
        id = request.session.get(SESSION_NAME)

        if status != 'true':
            return redirect('{}?to={}'.format(reverse('dashboard_login'), request.path))

        user = User.objects.filter(pk=id).exists()
        if user:
            return func(self, request, *args, **kwargs)
        else:
            return redirect('{}?to={}'.format(reverse('dashboard_login'), request.path))

    return wrapper

