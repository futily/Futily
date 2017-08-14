from django.conf.urls import url
from django.contrib.auth import views as auth_views

from .views import ProfileView, RegisterView, SettingsView

urlpatterns = [
    # Login
    url(r'^login/$', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),

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
    url(r'^(?P<username>[0-9A-Za-z_\-]+)/$', ProfileView.as_view(), name='profile'),
    url(r'^(?P<username>[0-9A-Za-z_\-]+)/settings/$', SettingsView.as_view(), name='settings'),
]
