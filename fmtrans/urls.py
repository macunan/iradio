from django.urls import path
from django.urls.resolvers import URLPattern
from django.conf import settings
from django.conf.urls.static import static
from .import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from .views import ajax_view


urlpatterns= [
        path('',views.index),
        path('light',views.light),
        path('cloud',views.cloud),
        path('add',views.add),
        path('del',views.borrar),
        path('modify',views.modify),
        path('ajax/', ajax_view, name="ajax"),
        ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



# urlpatterns += staticfiles_urlpatterns()
