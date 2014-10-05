#from django.utils.translation import ugettext_lazy as _
from django.conf.urls import patterns, url

urlpatterns = patterns('toys.views',
    url(r'^(?:index.html)?$','frontpage',name='frontpage'),
    url(r'^countingby[/]?$','countingby',name='countingby'),
)

#from django.utils.translation import ugettext as _
