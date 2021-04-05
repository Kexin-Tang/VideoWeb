# coding:utf8
from django.views.generic import View
from app.libs.base_render import render_to_response

class Index(View):
    TEMPLATE = 'dashboard/index.html'

    def get(self, req):
        return render_to_response(req, self.TEMPLATE)