from braces.views import AnonymousRequiredMixin
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View
from django.views.generic import DetailView, FormView, UpdateView

from futily.apps.clubs.models import Club

from ..leagues.models import League
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


class UserMixin(View):
    model = User
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        print(self.request.path, self.request.user.get_collection_url(), self.request.path.startswith(self.request.user.get_collection_url()))

        context['side_nav'] = [
            {
                'label': 'Profile',
                'url': self.object.get_absolute_url(),
                'current': str(self.request.path == self.object.get_absolute_url()).lower(),
            },
            {
                'label': 'Squads',
                'url': self.object.get_squads_url(),
                'current': str(self.request.path == self.object.get_squads_url()).lower(),
            },
            {
                'label': 'Packs',
                'url': self.object.get_packs_url(),
                'current': str(self.request.path == self.object.get_packs_url()).lower(),
            },
            {
                'label': 'Collection',
                'url': self.object.get_collection_url(),
                'current': str(self.request.path.startswith(self.object.get_collection_url())).lower(),
            },
        ]

        return context


class UserCollectionView(UserMixin, DetailView):
    template_name = 'users/user_detail_collection.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['leagues'] = League.objects.all()

        return context


class UserCollectionClubView(UserMixin, DetailView):
    template_name = 'users/user_detail_collection_club.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['club'] = Club.objects.prefetch_related('player_set').get(slug=self.kwargs['club_slug'])
        context['league'] = League.objects.get(slug=self.kwargs['league_slug'])
        context['collected_players'] = [
            x for x in self.request.user.cardcollection.players.filter(
                club=context['club'])]
        context['uncollected_players'] = context['club'].player_set(manager='cards').exclude(
            id__in=[x.id for x in context['collected_players']])

        return context


class UserCollectionLeagueView(UserMixin, DetailView):
    template_name = 'users/user_detail_collection_league.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['league'] = League.objects.get(slug=self.kwargs['league_slug'])

        return context


class UserPackView(UserMixin, DetailView):
    template_name = 'users/user_detail_packs.html'


class UserProfileView(UserMixin, DetailView):
    pass


class UserSettingsView(LoginRequiredMixin, UserMixin, UpdateView):
    form_class = UserSettingsForm
    template_name = 'users/user_settings.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user

        return kwargs

    def get_object(self, queryset=None):
        return self.request.user
