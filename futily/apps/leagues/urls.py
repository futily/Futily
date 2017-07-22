from django.conf.urls import url

from .views import LeagueDetail, LeagueList

urlpatterns = [
    url(r'^$', LeagueList.as_view(), name='leagues'),
    url(r'^(?P<slug>[-\w]+)/$', LeagueDetail.as_view(), name='league')
]
