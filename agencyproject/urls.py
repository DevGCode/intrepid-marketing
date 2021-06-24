from django.urls import include, path
from django.contrib import admin
from django.contrib.auth import views as auth_views

from website.views import *

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # Your URLs go here
    path('', IndexView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('', include('userarea.urls')),
    path('', include('website.urls')),
    path('', include('adminarea.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
