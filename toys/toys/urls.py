from django.utils.translation import ugettext_lazy as _
from django.conf.urls import patterns, include, url

urlpatterns = patterns('toys.views',
    url(r'^(?:index.html)?$','frontpage',name='frontpage'),
)

from django.utils.translation import ugettext as _
