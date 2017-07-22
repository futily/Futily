from django.conf.urls import url

from .views import PlayerDetail, PlayerList

urlpatterns = [
    url(r'^$', PlayerList.as_view(), name='players'),
    url(r'^(?P<pk>[0-9]+)-(?P<slug>[^/]+)/$', PlayerDetail.as_view(), name='player'),
]
