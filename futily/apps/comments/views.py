from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.db.models import F
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_protect
from django_comments.models import CommentFlag
from django_comments.views.utils import next_redirect
from django_comments_xtd import get_model as get_comment_model
from django_comments_xtd.api import ToggleFeedbackFlag
from django_comments_xtd.models import (DISLIKEDIT_FLAG, LIKEDIT_FLAG,
                                        XtdComment)
from django_comments_xtd.utils import has_app_model_option
from rest_framework import generics

from .models import FlyComment
from .serializers import ReadCommentSerializer


class CommentList(generics.ListAPIView):
    """List all comments for a given ContentType and object ID."""
    serializer_class = ReadCommentSerializer

    def get_queryset(self):
        content_type_arg = self.kwargs.get('content_type', None)
        object_pk_arg = self.kwargs.get('object_pk', None)
        app_label, model = content_type_arg.split("-")
        try:
            content_type = ContentType.objects.get_by_natural_key(app_label, model)
        except ContentType.DoesNotExist:
            qs = XtdComment.objects.none()
        else:
            qs = XtdComment.objects.filter(content_type=content_type, object_pk=int(object_pk_arg),
                                           site__pk=settings.SITE_ID, is_public=True)

        return qs


class CommentFeedback(ToggleFeedbackFlag):
    def perform_create(self, serializer):
        f = perform_like if self.request.data["flag"] == 'like' else perform_dislike
        self.created = f(self.request, serializer.validated_data['comment'])


@csrf_protect
@login_required
def like(request, comment_id, next=None):
    """
    Like a comment. Confirmation on GET, action on POST.

    Templates: :template:`django_comments_xtd/like.html`,
    Context:
        comment
            the flagged `comments.comment` object
    """
    comment = get_object_or_404(get_comment_model(), pk=comment_id,
                                site__pk=settings.SITE_ID)
    if not has_app_model_option(comment)['allow_feedback']:
        ctype = ContentType.objects.get_for_model(comment.content_object)
        raise Http404("Comments posted to instances of '%s.%s' are not "
                      "explicitly allowed to receive 'liked it' flags. "
                      "Check the COMMENTS_XTD_APP_MODEL_OPTIONS "
                      "setting." % (ctype.app_label, ctype.model))
    # Flag on POST
    if request.method == 'POST':
        perform_like(request, comment)
        return next_redirect(request,
                             fallback=next or 'comments-xtd-like-done',
                             c=comment.pk)
    # Render a form on GET
    else:
        liked_it = request.user in comment.users_flagging(LIKEDIT_FLAG)
        return render(request, 'django_comments_xtd/like.html',
                      {
                          'comment': comment,
                          'already_liked_it': liked_it,
                          'next': next
                      })


@csrf_protect
@login_required
def dislike(request, comment_id, next=None):
    """
    Dislike a comment. Confirmation on GET, action on POST.

    Templates: :template:`django_comments_xtd/dislike.html`,
    Context:
        comment
            the flagged `comments.comment` object
    """
    comment = get_object_or_404(get_comment_model(), pk=comment_id,
                                site__pk=settings.SITE_ID)
    if not has_app_model_option(comment)['allow_feedback']:
        ctype = ContentType.objects.get_for_model(comment.content_object)
        raise Http404("Comments posted to instances of '%s.%s' are not "
                      "explicitly allowed to receive 'disliked it' flags. "
                      "Check the COMMENTS_XTD_APP_MODEL_OPTIONS "
                      "setting." % (ctype.app_label, ctype.model))
    # Flag on POST
    if request.method == 'POST':
        perform_dislike(request, comment)
        return next_redirect(request,
                             fallback=(next or 'comments-xtd-dislike-done'),
                             c=comment.pk)
    # Render a form on GET
    else:
        disliked_it = request.user in comment.users_flagging(DISLIKEDIT_FLAG)
        return render(request, 'django_comments_xtd/dislike.html',
                      {
                          'comment': comment,
                          'already_disliked_it': disliked_it,
                          'next': next
                      })


def perform_like(request, comment):
    """Actually set the 'Likedit' flag on a comment from a request."""
    flag, created = CommentFlag.objects.get_or_create(comment=comment,
                                                      user=request.user,
                                                      flag=LIKEDIT_FLAG)
    fly_comment = FlyComment.objects.get(id=comment.id)
    if created:
        already_voted = CommentFlag.objects.filter(comment=comment, user=request.user, flag=DISLIKEDIT_FLAG)

        print(already_voted)
        if already_voted:
            fly_comment.score += 2
            already_voted.delete()
        else:
            fly_comment.score += 1
    else:
        fly_comment.score += 1
        flag.delete()

    fly_comment.save(update_fields=['score'])

    return created


def perform_dislike(request, comment):
    """Actually set the 'Dislikedit' flag on a comment from a request."""
    flag, created = CommentFlag.objects.get_or_create(comment=comment,
                                                      user=request.user,
                                                      flag=DISLIKEDIT_FLAG)
    fly_comment = FlyComment.objects.get(id=comment.id)
    if created:
        already_voted = CommentFlag.objects.filter(comment=comment, user=request.user, flag=LIKEDIT_FLAG)

        if already_voted:
            fly_comment.score -= 2
            already_voted.delete()
        else:
            fly_comment.score -= 1
    else:
        fly_comment.score -= 1
        flag.delete()

    fly_comment.save(update_fields=['score'])

    return created
