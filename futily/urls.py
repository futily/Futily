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

from .apps.sections.models import sections_js
from .utils.views import FrontendView

admin.autodiscover()

urlpatterns = [
    url(r'^admin/password_change/$', auth_views.password_change,
        {'password_change_form': CMSPasswordChangeForm}, name='password_change'),
    url(r'^admin/password_change/done/$', auth_views.password_change_done, name='password_change_done'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/pages/page/sections.js$', sections_js, name='admin_sections_js'),

    url(r'social/', include('social_django.urls', namespace='social')),

    # Special cases
    url(r'users/', include('futily.apps.users.urls', namespace='users')),

    # Permalink redirection service.
    url(r'^r/(?P<content_type_id>\d+)-(?P<object_id>[^/]+)/$', contenttypes_views.shortcut, name='permalink_redirect'),

    # Google sitemap service.
    url(r'^sitemap.xml$', sitemaps_views.index, {'sitemaps': registered_sitemaps}),
    url(r'^sitemap-(?P<section>.+)\.xml$', sitemaps_views.sitemap, {'sitemaps': registered_sitemaps}),

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
        url(r'^404/$', generic.TemplateView.as_view(template_name='404.html')),
        url(r'^500/$', generic.TemplateView.as_view(template_name='500.html')),
        url(r'^frontend/$', FrontendView.as_view()),
        url(r'^frontend/(?P<slug>[\w-]+)/$', FrontendView.as_view())
    ]

handler500 = 'cms.views.handler500'
