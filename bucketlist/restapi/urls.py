from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from restapi import views

urlpatterns = [
    url(r'^auth', 'rest_framework_jwt.views.obtain_jwt_token',
        name='login'),
    url(r'^auth_verify/', 'rest_framework_jwt.views.verify_jwt_token'),

    url(r'^bucketlists/$', views.BucketlistView.as_view(),
        name='api.bucketlists'),

    url(r'^bucketlists/(?P<pk>[0-9]+)/$', views.BucketlistDetailView.as_view(),
        name="api.bucketlist"),

    url(r'^bucketlists/(?P<pk>[0-9]+)/items/$',
        views.BucketlistItemCreateView.as_view(),
        name="api.bucketlistitem.create"),

    url(r'^bucketlists/(?P<pk>[0-9]+)/items/(?P<pk_item>[0-9]+)$',
        views.BucketlistItemDetailView.as_view(),
        name="api.bucketlist.item")
]

urlpatterns = format_suffix_patterns(urlpatterns)
