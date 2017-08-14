from braces.views import AnonymousRequiredMixin
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import DetailView, FormView, UpdateView

from .forms import UserRegistrationForm, UserSettingsForm
from .models import User


class RegisterView(AnonymousRequiredMixin, FormView):
    form_class = UserRegistrationForm
    model = User
    template_name = 'users/register.html'

    def form_valid(self, form):
        password = form.cleaned_data.pop('password1')
        del form.cleaned_data['password2']

        obj = User.objects.create(**form.cleaned_data)
        obj.set_password(password)
        obj.save()

        auth_user = authenticate(username=obj.get_username(), password=password)
        login(self.request, auth_user)

        return redirect(auth_user.get_absolute_url())


class ProfileView(DetailView):
    model = User
    slug_field = 'username'
    slug_url_kwarg = 'username'


class SettingsView(LoginRequiredMixin, UpdateView):
    form_class = UserSettingsForm
    model = User
    slug_field = 'username'
    slug_url_kwarg = 'username'
    template_name_suffix = '_update_form'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user

        return kwargs

    def get_object(self, queryset=None):
        return self.request.user
