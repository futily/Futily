from django.contrib.staticfiles.storage import staticfiles_storage
from django_comments_xtd.api.serializers import ReadCommentSerializer as RCS

from .models import FlyComment


class ReadCommentSerializer(RCS):
    class Meta:
        model = FlyComment
        fields = ['id', 'user_name', 'user_url', 'user_moderator', 'user_avatar', 'permalink', 'comment',
                  'submit_date', 'parent_id', 'level', 'is_removed', 'allow_reply', 'flags', 'score']

    def get_user_avatar(self, obj):
        user = obj.user

        if user:
            if user.favourite_club_id:
                return staticfiles_storage.url(f'ea-images/clubs/{user.favourite_club.ea_id}.png')
            elif user.favourite_player_id:
                return staticfiles_storage.url(f'ea-images/players/{user.favourite_player.ea_id}.png')
            elif user.favourite_nation_id:
                return staticfiles_storage.url(f'ea-images/nations/{user.favourite_nation.ea_id}.png')
            else:
                return None
