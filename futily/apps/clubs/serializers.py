from rest_framework import serializers

from futily.apps.clubs.models import Club


class ClubSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Club
        fields = ['url', 'id', 'ea_id', 'name']
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }
