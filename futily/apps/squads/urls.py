from django.conf.urls import url

from .views import Builder, BuilderAjax, BuilderImport, SquadDetail, SquadList

urlpatterns = [
    url(r'^$', SquadList.as_view(), name='squads'),
    url(r'^builder/$', Builder.as_view(), name='builder'),
    url(r'^builder/save/$', BuilderAjax.as_view(), name='builder_ajax'),
    url(r'^builder/import/(?P<id>[A-Za-z0-9]+)$', BuilderImport.as_view(), name='builder_import'),
    url(r'^(?P<pk>[0-9]+)-(?P<slug>[^/]+)/$', SquadDetail.as_view(), name='squad'),
]
