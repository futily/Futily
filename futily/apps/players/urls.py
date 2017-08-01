from django.conf.urls import url

from .views import PlayerDetail, PlayerDetailSimilar, PlayerList

urlpatterns = [
    url(r'^$', PlayerList.as_view(), name='players'),
    url(r'^(?P<pk>[0-9]+)-(?P<slug>[^/]+)/$', PlayerDetail.as_view(), name='player'),
    url(r'^(?P<pk>[0-9]+)-(?P<slug>[^/]+)/similar/$', PlayerDetailSimilar.as_view(), name='player_similar'),
]
