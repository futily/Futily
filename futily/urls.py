from cms.forms import CMSPasswordChangeForm
from cms.sitemaps import registered_sitemaps
from cms.views import TextTemplateView
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.contenttypes import views as contenttypes_views
from django.contrib.sitemaps import views as sitemaps_views
from django.views import generic
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from futily.apps.clubs.views import ClubViewSet
from futily.apps.nations.views import NationViewSet
from futily.apps.players.views.api import PlayerViewSet

from .apps.sections.models import sections_js
from .utils.views import FrontendView

admin.autodiscover()

router = DefaultRouter()
router.register(r'clubs', ClubViewSet)
router.register(r'nations', NationViewSet)
router.register(r'players', PlayerViewSet)

urlpatterns = [
    url(r'^admin/password_change/$', auth_views.password_change,
        {'password_change_form': CMSPasswordChangeForm}, name='password_change'),
    url(r'^admin/password_change/done/$', auth_views.password_change_done, name='password_change_done'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/pages/page/sections.js$', sections_js, name='admin_sections_js'),

    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'social/', include('social_django.urls', namespace='social')),

    # Special cases
    url(r'chemistry-styles/', TemplateView.as_view(template_name='misc/chemistry-styles.html'), name='chemistry-styles'),
    url(r'users/', include('futily.apps.users.urls', namespace='users')),
    url(r'^comments/', include('futily.apps.comments.urls')),

    # Permalink redirection service.
    url(r'^r/(?P<content_type_id>\d+)-(?P<object_id>[^/]+)/$', contenttypes_views.shortcut, name='permalink_redirect'),

    # Google sitemap service.
    url(r'^sitemap.xml$', sitemaps_views.index, {'sitemaps': registered_sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
    url(r'^sitemap-(?P<section>.+)\.xml$', sitemaps_views.sitemap, {'sitemaps': registered_sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),

    # Basic robots.txt.
    url(r'^robots.txt$', TextTemplateView.as_view(template_name='robots.txt')),

    # There's no favicon here!
    url(r'^favicon.ico$', generic.RedirectView.as_view(permanent=True)),
] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)

if settings.DEBUG:
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns

    urlpatterns += [
        url(r'^silk/', include('silk.urls', namespace='silk')),
        url(r'^404/$', generic.TemplateView.as_view(template_name='404.html')),
        url(r'^500/$', generic.TemplateView.as_view(template_name='500.html')),
        url(r'^frontend/$', FrontendView.as_view()),
        url(r'^frontend/(?P<slug>[\w-]+)/$', FrontendView.as_view())
    ]

handler500 = 'cms.views.handler500'
