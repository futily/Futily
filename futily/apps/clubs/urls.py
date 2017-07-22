from django.conf.urls import url

from .views import ClubDetail, ClubList

urlpatterns = [
    url(r'^$', ClubList.as_view(), name='clubs'),
    url(r'^(?P<slug>[-\w]+)/$', ClubDetail.as_view(), name='club')
]
