from django.conf import settings
from django.conf.urls import url

from futily.apps.players.views.detail import (PlayerDetail,
                                              PlayerDetailChemistry,
                                              PlayerDetailChemistryType,
                                              PlayerDetailCompare,
                                              PlayerDetailSimilar,
                                              PlayerFavourite, PlayerRate)
from futily.apps.players.views.list import (PlayerCardColorTest, PlayerList,
                                            PlayerListLatest,
                                            PlayerPerfectChemistry)

urlpatterns = [
    url(r'^$', PlayerList.as_view(), name='players'),
    url(r'^latest/$', PlayerListLatest.as_view(), name='latest_players'),
    url(r'^perfect-chemistry/$', PlayerPerfectChemistry.as_view(), name='perfect_chemistry'),
    url(r'^(?P<pk>[0-9]+)-(?P<slug>[^/]+)/$', PlayerDetail.as_view(), name='player'),
    url(r'^(?P<pk>[0-9]+)-(?P<slug>[^/]+)/rate/$', PlayerRate.as_view(), name='player_rate'),
    url(r'^(?P<pk>[0-9]+)-(?P<slug>[^/]+)/favourite/$', PlayerFavourite.as_view(), name='player_favourite'),
    url(r'^(?P<pk>[0-9]+)-(?P<slug>[^/]+)/similar/$', PlayerDetailSimilar.as_view(), name='player_similar'),
    url(r'^(?P<pk>[0-9]+)-(?P<slug>[^/]+)/chemistry/$', PlayerDetailChemistry.as_view(), name='player_chemistry'),
    url(r'^(?P<pk>[0-9]+)-(?P<slug>[^/]+)/chemistry/(?P<chem_type>perfect|strong|weak)/$',
        PlayerDetailChemistryType.as_view(), name='player_chemistry_type'),
    url(r'^(?P<pk>[0-9]+)-(?P<slug>[^/]+)/compare/$',
        PlayerDetailCompare.as_view(), name='player_compare'),
    url(r'^(?P<pk>[0-9]+)-(?P<slug>[^/]+)/compare/(?P<other_pk>[0-9]+)/$',
        PlayerDetailCompare.as_view(), name='player_compare'),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^card-color-test/$', PlayerCardColorTest.as_view(), name='card_test'),
    ]
