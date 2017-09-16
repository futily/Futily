from django import forms
from django.contrib.admin import widgets

from .models import Pack, PackType


class PackTypeAdmin(forms.ModelForm):

    class Meta:
        model = PackType
        fields = '__all__'
        widgets = {
            'roll_1_types': widgets.FilteredSelectMultiple('Roll 1 types', False)
        }


class PackCreationForm(forms.ModelForm):

    class Meta:
        model = Pack
        fields = ['page', 'title', 'slug', 'user', 'players', 'type', 'value']
