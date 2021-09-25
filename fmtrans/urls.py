from django.urls import path
from django.urls.resolvers import URLPattern
from django.conf import settings
from django.conf.urls.static import static
from .import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from .views import ajax_view
from .api import api
from django.contrib import admin


urlpatterns= [
        path('',views.index),
        path('light',views.light),
        path('cloud',views.cloud),
        path('add',views.add),
        path('del',views.borrar),
        path('modify',views.modify),
        path('ajax/', ajax_view, name="ajax"),
        path('config', views.config),
        path('download', views.download_file),
        path('export', views.export),
        path("api/",api.urls),
        ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


