from django.conf.urls import url

from .views import PackDetail, TypeDetail, TypeList

urlpatterns = [
    url(r'^$', TypeList.as_view(), name='types'),
    url(r'^type/(?P<slug>[-\w]+)/$', TypeDetail.as_view(), name='type'),
    url(r'^(?P<pk>[0-9]+)-(?P<slug>[^/]+)/$', PackDetail.as_view(), name='pack'),
]
