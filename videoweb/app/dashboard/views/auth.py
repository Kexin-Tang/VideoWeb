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
from app.dashboard.utils.permission import dashboardAuth

class Login(View):
    TEMPLATE = 'dashboard/auth/login.html'
    def get(self, req):
        if req.user.is_authenticated:
            return redirect(reverse('dashboard_index'))

        to = req.GET.get('to', '')
        return render_to_response(req, self.TEMPLATE, {'error': '', 'to': to})

    def post(self, req):
        username = req.POST.get('username')
        password = req.POST.get('password')
        to = req.GET.get('to', '')          # 用于存储下一次跳转的位置

        # 查看是否存在用户
        exists = User.objects.filter(username=username).exists()
        if not exists:
            return render_to_response(req, self.TEMPLATE, {'error': "未找到该用户"})

        # 查看用户账号密码是否匹配
        user = authenticate(username=username, password=password)
        if not user:
            return render_to_response(req, self.TEMPLATE, {'error': "登录失败"})

        user = User.objects.get(username=username)
        if user.is_staff is False:
            return render_to_response(req, self.TEMPLATE, {'error': "缺少权限，请联系管理员"})

        login(req, user)

        # 如果有跳转，则跳转
        if to:
            return redirect(to)

        return redirect(reverse('dashboard_index'))


class Logout(View):
    def get(self, req):
        logout(req)
        return redirect(reverse('dashboard_login'))


class AdminManage(View):
    TEMPLATE = 'dashboard/auth/admin.html'

    @dashboardAuth
    def get(self, req):
        users = User.objects.all()

        isAdmin = req.user.is_superuser # 当前登录的用户是管理员吗

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


class Register(View):
    TEMPLATE = 'dashboard/auth/register.html'
    def get(self, req):
        data = {}
        error = req.GET.get('error', '')
        data['error'] = error

        return render_to_response(req, self.TEMPLATE, data=data)

    def post(self, req):
        username = req.POST.get('username', '')
        password = req.POST.get('password', '')
        check = req.POST.get('check', '')

        if not all([username, password, check]):
            return redirect('{}?error={}'.format(reverse('dashboard_register'), '请确保所有内容均被正确填写'))

        exists = User.objects.filter(username=username).exists()
        if exists:
            return redirect('{}?error={}'.format(reverse('dashboard_register'), '用户名已存在'))

        if password and password!=check:
            return redirect('{}?error={}'.format(reverse('dashboard_register'), '注册失败'))

        User.objects.create_user(
            username=username,
            password=password,
            is_staff=True
        )

        user = User.objects.get(username=username)
        login(req, user)

        return redirect(reverse('dashboard_index'))