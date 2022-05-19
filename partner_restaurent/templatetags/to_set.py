from django import template
register = template.Library()

from ..models import Restaurent

@register.filter(is_safe=True)
def toSet(mylist):
   l=[]
   for r in mylist:
        l.append(r.wilaya)
   l=list(dict.fromkeys(l))#list(set(l))
   return l