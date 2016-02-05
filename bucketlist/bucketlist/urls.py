from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^', include('restapi.urls')),
    url(r'^api-docs/', include('rest_framework_swagger.urls')),
    url(r'^.*$',
        TemplateView.as_view(template_name='restapi/index.html'),
        name='index'),
    url(r'^admin/', admin.site.urls),
]
