from django.conf.urls import url
import resapi.views as views

urlpatterns = [
    url(r'^bucketlists/$',
        views.BucketlistView.as_view(),
        name='api.bucketlists'),

    url(r'^bucketlists/(?P<pk>[0-9]+)/$',
        views.BucketlistDetailView.as_view(),
        name="api.bucketlist"),

    url(r'^bucketlists/(?P<pk>[0-9]+)/items/$',
        views.BucketlistItemCreateView.as_view(),
        name="api.bucketlistitem.create"),

    url(r'^bucketlists/(?P<pk>[0-9]+)/items/(?P<pk>[0-9]+)$',
        views.BucketlistItemDetailView.as_view(),
        name="api.bucketlist.item")

]
