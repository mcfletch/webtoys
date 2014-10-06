#from django.utils.translation import ugettext_lazy as _
from django.conf.urls import patterns, url

urlpatterns = patterns('toys.views',
    url(r'^(?:index.html)?$','frontpage',name='frontpage'),
    url(r'^polygons[/]?$','polygons',name='polygons'),
    url(r'^countingby[/]?$','countingby',name='countingby'),
    url(r'^1[/]?$','countingby',kwargs={'per_row':10}, name='multiplefactors',),
    url(r'^powersten[/]?$','powersten',name='powersten'),
)

#from django.utils.translation import ugettext as _
