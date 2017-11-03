from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.SquadBuilderChallengeSetList.as_view(), name='sets'),
    url(r'^(?P<category>[-\w]+)/$', views.SquadBuilderChallengeCategoryView.as_view(), name='set'),
    url(r'^set/(?P<slug>[-\w]+)/$', views.SquadBuilderChallengeSetDetail.as_view(), name='set'),
    url(r'^set/(?P<set_slug>[-\w]+)/(?P<slug>[-\w]+)/$', views.SquadBuilderChallengeDetail.as_view(), name='challenge'),
    url(r'^set/(?P<set_slug>[-\w]+)/(?P<slug>[-\w]+)/builder/$', views.SquadBuilderChallengeBuilder.as_view(), name='challenge_builder'),
]
