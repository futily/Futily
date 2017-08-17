from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from .views import (RegisterView, UserCollectionClubView,
                    UserCollectionLeagueView, UserCollectionView,
                    UserFollowView, UserPackView, UserProfileView,
                    UserSettingsView)

urlpatterns = [
    # Login
    url(r'^login/$', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),

    # Password change
    url(r'^password_change/$', auth_views.PasswordChangeView.as_view(), name='password_change'),
    url(r'^password_change/done/$', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    # Password reset
    url(
        r'^password_reset/$',
        auth_views.PasswordResetView.as_view(email_template_name='users/emails/password_reset.html',
                                             template_name='users/password_reset.html',
                                             success_url=reverse_lazy('users:password_reset_done')),
        name='password_reset'),
    url(
        r'^password_reset/done/$',
        auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
        name='password_reset_done'),
    url(
        r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html',
                                                    success_url=reverse_lazy('users:password_reset_complete')),
        name='password_reset_confirm'),
    url(
        r'^reset/done/$',
        auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
        name='password_reset_complete'),

    # Register
    url(r'^register/$', RegisterView.as_view(), name='register'),
    # url(r'^register/done/$', auth_views.PasswordResetDoneView.as_view(
    #     template_name='users/register_done.html'
    # ), name='register-done'),
    # url(r'^register/password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     auth_views.PasswordResetConfirmView.as_view(
    #         template_name='users/initial_confirm.html',
    #         success_url='users:register-complete'
    #     ), name='register-confirm'),
    # url(r'^register/complete/$', auth_views.PasswordResetCompleteView.as_view(
    #     template_name='users/initial_complete.html'
    # ), name='register-complete'),

    # Profile
    url(r'^(?P<username>[0-9A-Za-z_\-]+)/$', UserProfileView.as_view(), name='profile'),
    url(r'^(?P<username>[0-9A-Za-z_\-]+)/collection/$', UserCollectionView.as_view(), name='collection'),
    url(
        r'^(?P<username>[0-9A-Za-z_\-]+)/collection/(?P<league_slug>[-\w]+)/$',
        UserCollectionLeagueView.as_view(),
        name='collection-league'
    ),
    url(
        r'^(?P<username>[0-9A-Za-z_\-]+)/collection/(?P<league_slug>[-\w]+)/(?P<club_slug>[-\w]+)/$',
        UserCollectionClubView.as_view(),
        name='collection-club'
    ),
    url(r'^(?P<username>[0-9A-Za-z_\-]+)/packs/$', UserPackView.as_view(), name='packs'),
    url(r'^(?P<username>[0-9A-Za-z_\-]+)/settings/$', UserSettingsView.as_view(), name='settings'),

    url(r'^(?P<username>[0-9A-Za-z_\-]+)/follow/$', UserFollowView.as_view(), name='follow'),
]
