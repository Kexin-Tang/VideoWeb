# coding:utf8
from django.views.generic import View
from app.libs.base_render import render_to_response
from django.shortcuts import render, reverse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.core.paginator import Paginator

class Login(View):
    TEMPLATE = 'dashboard/auth/login.html'
    def get(self, req):

        if req.user.is_authenticated:
            return redirect(reverse('dashboard_index'))

        return render_to_response(req, self.TEMPLATE, {'error': ''})

    def post(self, req):
        username = req.POST.get('username')
        password = req.POST.get('password')
        exists = User.objects.filter(username=username).exists()
        if not exists:
            return render_to_response(req, self.TEMPLATE, {'error': "User not found"})

        user = authenticate(username=username, password=password)
        if not user:
            return render_to_response(req, self.TEMPLATE, {'error': "Login failed"})

        login(req, user)

        return redirect(reverse('dashboard_index'))

class Logout(View):
    def get(self, req):
        logout(req)
        return redirect(reverse('dashboard_login'))


class AdminManage(View):
    TEMPLATE = 'dashboard/auth/admin.html'

    def get(self, req):
        users = User.objects.all()

        page = req.GET.get('page', 1)   # 获取当前的页
        p = Paginator(users, 5)         # 定义num个数据/页
        total_pages = p.num_pages       # 获取总的页数

        # 限定范围
        if int(page)<=1:
            page = 1
        if int(page)>=int(total_pages):
            page = total_pages

        current_users = p.get_page(int(page)).object_list   # 获取当前页的内容
        data = {'users': current_users, 'total': int(total_pages), 'page': int(page)}

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
        user.is_superuser = _status
        user.save()
        return redirect(reverse('admin_manage'))