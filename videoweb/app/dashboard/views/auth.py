# coding:utf8
'''
    @ 本文件用于处理登录界面和主要的管理用户界面
'''
from django.views.generic import View
from app.libs.base_render import render_to_response
from django.shortcuts import render, reverse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.core.paginator import Paginator
from app.dashboard.utils.permission import dashboardAuth, checkLoginByCookies, checkLoginBySession
from django.http import JsonResponse
from app.const.const import COOKIES_NAME, SESSION_NAME
import datetime




"""
    ////////////////////////////////////////////////////////////////////////////////
    登录界面
    
    @ get   ->  判断是否登录，如果登录了则跳转至主页；否则进行登录，并保存发出请求的路径至`to`
    @ post  ->  进行用户名和密码的验证，如果无误则设置用户登录信息
    ////////////////////////////////////////////////////////////////////////////////
"""
class Login(View):
    TEMPLATE = 'dashboard/auth/login.html'

    def get(self, req):
        # id = req.COOKIES.get(COOKIES_NAME)      # cookie版本
        id = req.session.get(SESSION_NAME)      # session版本
        if id:
            return redirect(reverse('dashboard_index'))
        to = req.GET.get('to', '')
        return render_to_response(req, self.TEMPLATE, {'to': to})


    def post(self, req):
        username = req.POST.get('username')
        password = req.POST.get('password')

        # 查看是否存在用户
        exists = User.objects.filter(username=username).exists()
        if not exists:
            return JsonResponse({'status': -1, 'error': '该用户不存在'})

        # 查看用户账号密码是否匹配
        user = authenticate(username=username, password=password)
        if not user:
            return JsonResponse({'status': -1, 'error': "登录失败"})

        user = User.objects.get(username=username)
        if user.is_staff is False:
            return JsonResponse({'status': -1, 'error': "缺少权限，请联系管理员"})

        current_time = datetime.datetime.utcnow()                   # 获取当前时间
        expire_time = current_time + datetime.timedelta(minutes=5)  # 推迟五分钟作为过期时间

        # # 配置cookie
        # response = JsonResponse({'status': 0, 'error': ''})
        # response.set_cookie(COOKIES_NAME, str(user.id), expires=expire_time)

        # 配置session
        req.session[SESSION_NAME] = user.id
        req.session["username"] = user.username
        req.session["is_login"] = "true"
        req.session.set_expiry(300)         # 300s后失效
        response = JsonResponse({'status': 0, 'error': ''})

        return response




"""
    ////////////////////////////////////////////////////////////////////////////////
    注销
    
    @ get   ->  将用户登录信息抹去
    ////////////////////////////////////////////////////////////////////////////////
"""
class Logout(View):
    def get(self, req):
        response = redirect(reverse('dashboard_login'))
        # response.delete_cookie(COOKIES_NAME)  # cookies版本
        req.session.flush() # session版本
        return response



"""
    ////////////////////////////////////////////////////////////////////////////////
    管理员对用户权限等进行操作的视图

    @ get   ->  显示用户信息
    ////////////////////////////////////////////////////////////////////////////////
"""
class AdminManage(View):
    TEMPLATE = 'dashboard/auth/admin.html'

    @checkLoginBySession
    def get(self, req):
        users = User.objects.all()

        # isAdmin = req.user.is_superuser # 当前登录的用户是管理员吗
        isAdmin = (req.session.get('username')=='admin')

        page = req.GET.get('page', 1)   # 获取当前的页
        p = Paginator(users, 5)         # 定义num个数据/页
        total_pages = p.num_pages       # 获取总的页数

        # 限定范围
        if int(page)<=1:
            page = 1
        if int(page)>=int(total_pages):
            page = total_pages

        current_users = p.get_page(int(page)).object_list   # 获取当前页的内容
        data = {'users': current_users, 'total': int(total_pages), 'page': int(page), 'isAdmin': isAdmin}

        return render_to_response(req, self.TEMPLATE, data=data)




"""
    ////////////////////////////////////////////////////////////////////////////////
    更新用户状态

    @ get   ->  更新用户状态
    ////////////////////////////////////////////////////////////////////////////////
"""
class UpdateAdminStatus(View):
    AdminManage = 'dashboard/auth/admin.html'
    def get(self, req):
        status = req.GET.get('status', 'off')
        id = req.GET.get('id', '')

        # 更改状态
        _status = False if status=='on' else True

        # 找到修改的对象
        user = User.objects.get(id=id)
        user.is_staff = _status
        user.save()
        return redirect(reverse('admin_manage'))




"""
    ////////////////////////////////////////////////////////////////////////////////
    用户注册逻辑

    @ get   ->  注册界面
    @ post  ->  检查注册的合法性，如果通过则完成信息更新与用户登录
    ////////////////////////////////////////////////////////////////////////////////
"""
class Register(View):
    TEMPLATE = 'dashboard/auth/register.html'
    def get(self, req):
        id = req.session.get(SESSION_NAME)  # session版本
        if id:
            return redirect(reverse('dashboard_index'))
        return render_to_response(req, self.TEMPLATE)


    def post(self, req):
        username = req.POST.get('username', '')
        password = req.POST.get('password', '')
        check = req.POST.get('check', '')

        if not all([username, password, check]):
            return JsonResponse({'status': -1, 'error': '请填写相应内容'})

        exists = User.objects.filter(username=username).exists()
        if exists:
            return JsonResponse({'status': -1, 'error': '用户已存在'})

        if password and password!=check:
            return JsonResponse({'status': -1, 'error': '注册失败，请确保两次密码输入一致'})

        User.objects.create_user(
            username=username,
            password=password,
            is_staff=True
        )

        user = User.objects.get(username=username)

        # 配置session
        req.session[SESSION_NAME] = user.id
        req.session['user_name'] = user.username
        req.session["is_login"] = "true"
        req.session.set_expiry(300)  # 300s后失效
        response = JsonResponse({'status': 0, 'error': ''})

        return response