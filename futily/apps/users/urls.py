from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from . import views

urlpatterns = [
    # Login
    url(r'^login/$', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),

    # Password reset
    url(
        r'^password-reset/$',
        auth_views.PasswordResetView.as_view(email_template_name='users/emails/password_reset.html',
                                             template_name='users/password_reset.html',
                                             success_url=reverse_lazy('users:password_reset_done')),
        name='password_reset'),
    url(
        r'^password-reset/done/$',
        auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
        name='password_reset_done'),
    url(
        r'^password-reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html',
                                                    success_url=reverse_lazy('users:password_reset_complete')),
        name='password_reset_confirm'),
    url(
        r'^password-reset/complete/$',
        auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
        name='password_reset_complete'),

    # Register
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
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
    url(r'^(?P<username>[\w_\-]+)/$', views.UserProfileView.as_view(), name='profile'),
    url(r'^(?P<username>[0-9A-Za-z_\-]+)/followers/$', views.UserFollowers.as_view(), name='followers'),
    url(r'^(?P<username>[0-9A-Za-z_\-]+)/following/$', views.UserFollowing.as_view(), name='following'),
    url(r'^(?P<username>[0-9A-Za-z_\-]+)/players/$', views.UserFavouritePlayers.as_view(), name='favourite-players'),
    url(r'^(?P<username>[0-9A-Za-z_\-]+)/squads/$', views.UserSquadsView.as_view(), name='squads'),
    url(r'^(?P<username>[0-9A-Za-z_\-]+)/packs/$', views.UserPacksView.as_view(), name='packs'),
    url(r'^(?P<username>[0-9A-Za-z_\-]+)/collection/$', views.UserCollectionView.as_view(), name='collection'),
    url(
        r'^(?P<username>[0-9A-Za-z_\-]+)/collection/(?P<league_slug>[-\w]+)/$',
        views.UserCollectionLeagueView.as_view(),
        name='collection-league'
    ),
    url(
        r'^(?P<username>[0-9A-Za-z_\-]+)/collection/(?P<league_slug>[-\w]+)/(?P<club_slug>[-\w]+)/$',
        views.UserCollectionClubView.as_view(),
        name='collection-club'
    ),

    # Settings
    url(r'^(?P<username>[0-9A-Za-z_\-]+)/settings/$', views.UserSettingsView.as_view(), name='settings'),
    url(
        r'^(?P<username>[0-9A-Za-z_\-]+)/settings/password_change/$',
        views.UserPasswordChangeView.as_view(),
        name='password_change'),
    url(
        r'^(?P<username>[0-9A-Za-z_\-]+)/settings/password_change/done/$',
        views.UserPasswordChangeDoneView.as_view(),
        name='password_change_done'),

    # AJAX
    url(r'^(?P<username>[0-9A-Za-z_\-]+)/follow/$', views.UserFollowView.as_view(), name='follow'),
]
