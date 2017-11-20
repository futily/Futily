from django.contrib import admin
from django_comments.models import CommentFlag
from django_comments_xtd.admin import XtdCommentsAdmin
from django_comments_xtd.models import XtdComment

from .models import FlyComment


@admin.register(FlyComment)
class FlyCommentAdmin(XtdCommentsAdmin):
    pass


admin.site.register(XtdComment, XtdCommentsAdmin)
admin.site.register(CommentFlag)
