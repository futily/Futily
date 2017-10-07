from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.SquadList.as_view(), name='squads'),
    url(r'^builder/$', views.Builder.as_view(), name='builder'),
    url(r'^builder/save/$', views.BuilderAjax.as_view(), name='builder_ajax'),
    url(r'^builder/import/(?P<id>[A-Za-z0-9]+)$', views.BuilderImport.as_view(), name='builder_import'),
    url(r'^(?P<pk>[0-9]+)/$', views.SquadDetail.as_view(), name='squad'),
    url(r'^(?P<pk>[0-9]+)/update/$', views.SquadUpdate.as_view(), name='squad-update'),
]
