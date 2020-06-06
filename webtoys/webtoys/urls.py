from django.conf.urls import include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^a/', admin.site.urls),
    url(r'',include('toys.urls')),
]
