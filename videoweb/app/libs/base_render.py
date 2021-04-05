# coding:utf-8
'''
    本文件用于定义mako模板
'''
from mako.lookup import TemplateLookup
from django.template import RequestContext
from django.conf import settings
from django.template.context import Context
from django.http import HttpResponse

def render_to_response(req, template, data=None):
    context_instance = RequestContext(req)
    path = settings.TEMPLATES[0]['DIRS'][0] # 获取config/settings.py中定义的模板路径
    lookup = TemplateLookup(
        directories=path,
        output_encoding='utf-8',
        input_encoding='utf-8'
    )
    mako_template = lookup.get_template(template)
    if not data:
        data = {}

    if context_instance:
        context_instance.update(data)
    else:
        context_instance = Context(data)

    result = {}

    for d in context_instance:
        result.update(d)

    result['csrf_token'] = '<input type="hidden" name="csrfmiddlewaretoken" value={0} />'.format(req.META['CSRF_COOKIE'])

    return HttpResponse(mako_template.render(**result))