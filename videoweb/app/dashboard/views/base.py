# coding:utf8
from django.views.generic import View
from app.libs.base_render import render_to_response
from app.dashboard.utils.permission import dashboardAuth

class Index(View):
    TEMPLATE = 'dashboard/index.html'
    @dashboardAuth
    def get(self, req):
        return render_to_response(req, self.TEMPLATE)