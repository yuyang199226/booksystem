from django import template
register=template.Library()
@register.filter
def traversal(value):
    ls=[]

    for i in value.all():
        ls.append(str(i))
    return '、'.join(ls)