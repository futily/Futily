from rest_framework import serializers

from .models import Player


class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    # absolute_url = serializers.SerializerMethodField()
    stats = serializers.SerializerMethodField()
    club = serializers.SerializerMethodField()
    league = serializers.SerializerMethodField()
    nation = serializers.SerializerMethodField()

    class Meta:
        model = Player
        fields = ['id', 'stats', 'club', 'league', 'nation', 'ea_id', 'ea_id_base', 'color', 'rating', 'position',
                  'name', 'card_att_1', 'card_att_2', 'card_att_3', 'card_att_4', 'card_att_5', 'card_att_6']
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_field_names(self, declared_fields, info):
        is_search = self.context['request'].query_params.get('is_search')

        if is_search:
            return ['name', 'rating', 'absolute_url']

        return super().get_field_names(declared_fields, info)

    @staticmethod
    def get_absolute_url(obj):
        return obj.get_absolute_url()

    @staticmethod
    def get_stats(obj):
        return obj.card_stats

    @staticmethod
    def get_club(obj):
        return {
            'title': obj.club.title,
            'ea_id': obj.club.ea_id
        }

    @staticmethod
    def get_league(obj):
        return {
            'title': obj.league.title,
            'ea_id': obj.league.ea_id
        }

    @staticmethod
    def get_nation(obj):
        return {
            'title': obj.nation.title,
            'ea_id': obj.nation.ea_id
        }
