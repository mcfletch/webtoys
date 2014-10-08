#from django.utils.translation import ugettext_lazy as _
from django.conf.urls import patterns, url

urlpatterns = patterns('toys.views',
    url(r'^(?:index.html)?$','frontpage',name='frontpage'),
    url(r'^polygons[/]?$','polygons',name='polygons'),
    url(r'^countingby[/]?$','countingby',name='countingby'),
    url(r'^multiplefactors[/]?$','countingby',kwargs={'per_row':10}, name='multiplefactors',),
    url(r'^powersten[/]?$','powersten',name='powersten'),
    url(r'^1[/]?$','countingby',kwargs={'per_row':10}, name='multiplefactors_old',),
    
    url(r'^saywhat[/]?$', 'saywhat', name='saywhat'), 
    url(r'^wordlist[/]?$', 'wordlist',  name='wordlist'), 
    url(r'^(?:wordlist[/])?clickfast(?:[.]html|[/])?$', 'clickfast', name='clickfast')
)

#from django.utils.translation import ugettext as _
