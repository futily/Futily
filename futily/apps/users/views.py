from braces.views import AnonymousRequiredMixin
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (PasswordChangeDoneView,
                                       PasswordChangeView)
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, FormView, UpdateView
from django.views.generic.detail import BaseDetailView

from futily.apps.actions.models import Action
from futily.apps.actions.utils import create_action
from futily.apps.clubs.models import Club
from futily.apps.views import BreadcrumbsMixin

from ..leagues.models import League
from .forms import UserRegistrationForm, UserSettingsForm
from .models import User


class RegisterView(AnonymousRequiredMixin, BreadcrumbsMixin, FormView):
    form_class = UserRegistrationForm
    model = User
    template_name = 'users/register.html'

    def set_breadcrumbs(self):
        return [
            {
                'label': 'Register',
                'link': reverse_lazy('users:register'),
            }
        ]

    def form_valid(self, form):
        password = form.cleaned_data.pop('password1')
        del form.cleaned_data['password2']

        obj = User.objects.create(**form.cleaned_data)
        obj.set_password(password)
        obj.save()

        auth_user = authenticate(username=obj.get_username(), password=password)
        login(self.request, auth_user)

        return redirect(auth_user.get_absolute_url())


class UserMixin(BreadcrumbsMixin, View):
    model = User
    slug_field = 'username__iexact'
    slug_url_kwarg = 'username'

    def set_breadcrumbs(self):
        return [
            {
                'label': self.object,
                'link': self.object.get_absolute_url(),
            }
        ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['side_nav'] = [
            {
                'label': 'Profile',
                'url': self.object.get_absolute_url(),
                'here': self.request.path == self.object.get_absolute_url(),
            },
            {
                'label': 'Players',
                'url': self.object.get_favourite_players_url(),
                'here': self.request.path == self.object.get_favourite_players_url(),
            },
            {
                'label': 'Squads',
                'url': self.object.get_squads_url(),
                'here': self.request.path == self.object.get_squads_url(),
            },
            {
                'label': 'Packs',
                'url': self.object.get_packs_url(),
                'here': self.request.path == self.object.get_packs_url(),
            },
            {
                'label': 'Collection',
                'url': self.object.get_collection_url(),
                'here': self.request.path.startswith(self.object.get_collection_url()),
            },
        ]

        return context


class UserFollowView(LoginRequiredMixin, UserMixin):
    def post(self, request, *args, **kwargs):
        user_to_follow = User.objects.get(username=self.kwargs['username'])
        following_user = self.request.user
        is_already_following = following_user.is_following(user_to_follow)

        if is_already_following:
            user_to_follow.remove_follower(following_user)

            create_action(request.user, 'unfollowed', user_to_follow)
        else:
            user_to_follow.add_follower(following_user)

            create_action(request.user, 'followed', user_to_follow)

        return JsonResponse({
            'followed': not is_already_following,
            'followed_user': user_to_follow.id,
            'followed_by': following_user.id,
        })


class UserFavouritePlayers(UserMixin, DetailView):
    template_name = 'users/user_detail_favourite_players.html'

    def set_breadcrumbs(self):
        return super(UserFavouritePlayers, self).set_breadcrumbs() + [
            {
                'label': 'Favourite players',
                'link': reverse_lazy('users:favourite-players', kwargs={'username': self.object.username}),
            }
        ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['players'] = self.object.favouriteplayers.players.all()

        return context


class UserCollectionView(UserMixin, DetailView):
    template_name = 'users/user_detail_collection.html'

    def set_breadcrumbs(self):
        return super(UserCollectionView, self).set_breadcrumbs() + [
            {
                'label': 'Card collection',
                'link': reverse_lazy('users:collection', kwargs={'username': self.object.username}),
            }
        ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['leagues'] = sorted(League.objects.all(), reverse=True, key=lambda x: x.collected_count(self.object))

        return context


class UserCollectionLeagueView(UserMixin, DetailView):
    template_name = 'users/user_detail_collection_league.html'

    def __init__(self):
        super(UserCollectionLeagueView, self).__init__()

        self.league = None

    def set_breadcrumbs(self):
        self.league = self.get_league()

        return super(UserCollectionLeagueView, self).set_breadcrumbs() + [
            {
                'label': 'Card collection',
                'link': reverse_lazy('users:collection', kwargs={'username': self.object.username}),
            },
            {
                'label': self.league.title,
                'link': reverse_lazy('users:collection-league', kwargs={
                    'username': self.object.username,
                    'league_slug': self.league.slug,
                }),
            },
        ]

    def get_league(self):
        return League.objects.get(slug=self.kwargs['league_slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['league'] = self.league
        context['clubs'] = sorted(self.league.club_set.all(), reverse=True,
                                  key=lambda x: x.collected_count(self.object))

        return context


class UserCollectionClubView(UserMixin, DetailView):
    template_name = 'users/user_detail_collection_club.html'

    def __init__(self):
        super(UserCollectionClubView, self).__init__()

        self.league = None
        self.club = None

    def dispatch(self, request, *args, **kwargs):
        self.league = self.get_league()
        self.club = self.get_club()

        return super(UserCollectionClubView, self).dispatch(request)

    def set_breadcrumbs(self):
        return super(UserCollectionClubView, self).set_breadcrumbs() + [
            {
                'label': 'Card collection',
                'link': reverse_lazy('users:collection', kwargs={'username': self.object.username}),
            },
            {
                'label': self.league.title,
                'link': reverse_lazy('users:collection-league', kwargs={
                    'username': self.object.username,
                    'league_slug': self.league.slug,
                }),
            },
            {
                'label': self.club.title,
                'link': reverse_lazy('users:collection-club', kwargs={
                    'username': self.object.username,
                    'league_slug': self.league.slug,
                    'club_slug': self.club.slug,
                }),
            },
        ]

    def get_league(self):
        return League.objects.get(slug=self.kwargs['league_slug'])

    def get_club(self):
        return Club.objects.prefetch_related('player_set').get(slug=self.kwargs['club_slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['club'] = self.club
        context['league'] = self.league
        context['collected_players'] = [
            x for x in self.request.user.cardcollection.players(manager='cards').filter(
                club=self.club)]
        context['uncollected_players'] = self.club.player_set(manager='cards').exclude(
            id__in=[x.id for x in context['collected_players']])

        return context


class UserPasswordChangeView(UserMixin, BaseDetailView, PasswordChangeView):
    template_name = 'users/user_password_change.html'

    def set_breadcrumbs(self):
        return super(UserPasswordChangeView, self).set_breadcrumbs() + [
            {
                'label': 'Change Password',
                'link': reverse_lazy('users:packs', kwargs={'username': self.object.username}),
            }
        ]

    def get_success_url(self):
        return reverse_lazy('users:password_change_done', kwargs={'username': self.request.user.username})


class UserPasswordChangeDoneView(UserMixin, BaseDetailView, PasswordChangeDoneView):
    template_name = 'users/user_password_change_done.html'

    def set_breadcrumbs(self):
        return super(UserPasswordChangeDoneView, self).set_breadcrumbs() + [
            {
                'label': 'Password change complete',
                'link': reverse_lazy('users:packs', kwargs={'username': self.object.username}),
            }
        ]


class UserSquadsView(UserMixin, DetailView):
    template_name = 'users/user_detail_squads.html'

    def set_breadcrumbs(self):
        return super(UserSquadsView, self).set_breadcrumbs() + [
            {
                'label': 'Squads',
                'link': reverse_lazy('users:squads', kwargs={'username': self.object.username}),
            }
        ]


class UserPacksView(UserMixin, DetailView):
    template_name = 'users/user_detail_packs.html'

    def set_breadcrumbs(self):
        return super(UserPacksView, self).set_breadcrumbs() + [
            {
                'label': 'Packs',
                'link': reverse_lazy('users:packs', kwargs={'username': self.object.username}),
            }
        ]


class UserProfileView(UserMixin, DetailView):
    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data()

        context['actions'] = Action.objects.filter(user=self.object)[:30] \
            .select_related('user') \
            .prefetch_related('target')

        return context


class UserFollowers(UserMixin, DetailView):
    template_name = 'users/user_followers.html'

    def set_breadcrumbs(self):
        return super(UserFollowers, self).set_breadcrumbs() + [
            {
                'label': 'Followers',
                'link': reverse_lazy('users:followers', kwargs={'username': self.object.username}),
            }
        ]


class UserFollowing(UserMixin, DetailView):
    template_name = 'users/user_following.html'

    def set_breadcrumbs(self):
        return super(UserFollowing, self).set_breadcrumbs() + [
            {
                'label': 'Following',
                'link': reverse_lazy('users:following', kwargs={'username': self.object.username}),
            }
        ]


class UserSettingsView(LoginRequiredMixin, UserMixin, UpdateView):
    form_class = UserSettingsForm
    template_name = 'users/user_settings.html'

    def set_breadcrumbs(self):
        return super(UserSettingsView, self).set_breadcrumbs() + [
            {
                'label': 'Settings',
                'link': reverse_lazy('users:packs', kwargs={'username': self.object.username}),
            }
        ]

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user

        return kwargs

    def get_object(self, queryset=None):
        return self.request.user
