from django import forms

from .models import Pack


class PackCreationForm(forms.ModelForm):

    class Meta:
        model = Pack
        fields = ['page', 'title', 'slug', 'user', 'players', 'type', 'value']
