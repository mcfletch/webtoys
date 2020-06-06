#from django.utils.translation import ugettext_lazy as _
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?:index.html)?$',views.frontpage,name='frontpage'),
    url(r'^polygons[/]?$',views.polygons,name='polygons'),
    url(r'^countingby[/]?$',views.countingby,name='countingby'),
    url(r'^multiplefactors[/]?$',views.countingby,kwargs={'per_row':10}, name='multiplefactors',),
    url(r'^powersten[/]?$',views.powersten,name='powersten'),
    url(r'^1[/]?$',views.countingby,kwargs={'per_row':10}, name='multiplefactors_old',),
    
    url(r'^saywhat[/]?$', views.saywhat, name='saywhat'), 
    url(r'^wordlist[/]?$', views.wordlist,  name='wordlist'), 
    url(r'^(wordlist[/])?clickfast([.]html|[/])?$', views.clickfast, name='clickfast'), 
    url(r'^(wordlist[/])?subwords([.]html|[/])?$', views.subwords, name='subwords'), 
    url(r'^(wordlist[/])?innerwords([.]html|[/])?$', views.innerwords, name='innerwords'), 
]

#from django.utils.translation import ugettext as _
