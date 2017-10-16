from rest_framework import serializers

from futily.apps.nations.models import Nation


class NationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Nation
        fields = ['url', 'id', 'ea_id', 'name']
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }
