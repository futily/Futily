from django import forms
from django.contrib.auth.forms import UserCreationForm

from ..forms import FormMixin
from .models import User


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'preferred_platform']


class UserSettingsForm(FormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ['about_me', 'preferred_platform', 'psn', 'xbox', 'origin', 'twitter', 'youtube', 'twitch', 'facebook',
                  'favourite_player', 'favourite_club', 'favourite_nation']

    def __init__(self, user=None, *args, **kwargs):
        self.user = user

        super().__init__(*args, **kwargs)

        self.fields['twitter'].widget.attrs['placeholder'] = 'Your Twitter username'
        self.fields['youtube'].widget.attrs['placeholder'] = 'Your YouTube username'
        self.fields['twitch'].widget.attrs['placeholder'] = 'Your Twitch username'
        self.fields['facebook'].widget.attrs['placeholder'] = 'Your Facebook username'

        self.fields['psn'].widget.attrs['placeholder'] = 'Your PSN username'
        self.fields['xbox'].widget.attrs['placeholder'] = 'Your Xbox live username'
        self.fields['origin'].widget.attrs['placeholder'] = 'Your Origin username'

    @property
    def groups(self):
        return [
            {
                'legend': 'Profile',
                'help_text': '',
                'fields': self.get_fields(['about_me', 'preferred_platform']),
            },
            {
                'legend': 'Platforms',
                'help_text': 'Fill these if you would like to show them on your profile',
                'fields': self.get_fields(['psn', 'xbox', 'origin']),
            },
            {
                'legend': 'Social accounts',
                'help_text': 'Fill these if you would like to show them on your profile',
                'fields': self.get_fields(['twitter', 'youtube', 'twitch', 'facebook']),
            },
            {
                'legend': 'Favourites',
                'help_text': '',
                'fields': self.get_fields(['favourite_player', 'favourite_club', 'favourite_nation']),
            },
        ]
