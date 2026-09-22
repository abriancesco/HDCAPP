from django import template

register = template.Library()

@register.simple_tag
def querystring(**kwargs):
    from django.http import QueryDict
    q = QueryDict(mutable=True)
    q.update(kwargs)
    return q.urlencode()
