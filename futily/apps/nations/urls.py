from django.conf.urls import url

from .views import NationDetail, NationList

urlpatterns = [
    url(r'^$', NationList.as_view(), name='nations'),
    url(r'^(?P<slug>[-\w]+)/$', NationDetail.as_view(), name='nation')
]
