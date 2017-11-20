import json

import jinja2
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django_comments.forms import CommentSecurityForm
from django_comments_xtd.conf import settings
from django_comments_xtd.templatetags.comments_xtd import (GetCommentBoxPropsNode,
                                                           XtdComment)
from django_jinja import library


@library.global_function
@jinja2.contextfunction
def get_commentbox_props(context, obj):
    '''
    Returns a JSON object with the initial props for the CommentBox component.

    The returned JSON object contains the following attributes::
        {
            comment_count: <int>,  // Count of comments posted to the object.
            allow_comments: <bool>,  // Whether to allow comments to this post.
            current_user: <str as 'user_id:user_name'>,
            is_authenticated: <bool>,  // Whether current_user is authenticated.
            allow_flagging: false,
            allow_feedback: false,
            show_feedback: false,
            can_moderate: <bool>,  // Whether current_user can moderate.
            poll_interval: 2000, // Check for new comments every 2 seconds.
            feedback_url: <api-url-to-send-like/dislike-feedback>,
            delete_url: <api-url-for-moderators-to-remove-comment>,
            login_url: settings.LOGIN_URL,
            reply_url: <api-url-to-reply-comments>,
            flag_url: <api-url-to-suggest-comment-removal>,
            list_url: <api-url-to-list-comments>,
            count_url: <api-url-to-count-comments>,
            send_url: <api-irl-to-send-a-comment>,
            form: {
                content_type: <value>,
                object_pk: <value>,
                timestamp: <value>,
                security_hash: <value>
            },
            login_url: <only_when_user_is_not_authenticated>,
            like_url: <only_when_user_is_not_authenticated>,
            dislike_url: <only_when_user_is_not_authenticated>
        }
    '''
    user = context.get('user', None)
    form = CommentSecurityForm(obj)
    ctype = ContentType.objects.get_for_model(obj)
    queryset = XtdComment.objects.filter(content_type=ctype,
                                         object_pk=obj.pk,
                                         site__pk=settings.SITE_ID,
                                         is_public=True)
    ctype_slug = f'{ctype.app_label}-{ctype.model}'
    d = {
        'commentCount': queryset.count(),
        'allowComments': True,
        'currentUser': '0:Anonymous',
        'isAuthenticated': False,
        'allowFlagging': True,
        'allowFeedback': True,
        'showFeedback': user.has_perm('django_comments.can_moderate'),
        'canModerate': False,
        'pollInterval': 2000,
        'feedbackUrl': reverse('comments-xtd-api-feedback'),
        'deleteUrl': reverse('comments-delete', args=(0,)),
        'replyUrl': reverse('comments-xtd-reply', kwargs={'cid': 0}),
        'flagUrl': reverse('comments-xtd-api-flag'),
        'listUrl': reverse('comments-xtd-api-list',
                           kwargs={
                               'content_type': ctype_slug,
                               'object_pk': obj.id
                           }),
        'countUrl': reverse('comments-xtd-api-count',
                            kwargs={
                                'content_type': ctype_slug,
                                'object_pk': obj.id
                            }),
        'sendUrl': reverse('comments-xtd-api-create'),
        'form': {
            'contentType': form['content_type'].value(),
            'objectPk': form['object_pk'].value(),
            'timestamp': form['timestamp'].value(),
            'securityHash': form['security_hash'].value()
        }
    }
    if user and user.is_authenticated():
        d['currentUser'] = '%d:%s' % (user.pk, settings.COMMENTS_XTD_API_USER_REPR(user))
        d['isAuthenticated'] = True
        d['canModerate'] = user.has_perm('django_comments.can_moderate')
    else:
        d['loginUrl'] = '/admin/login/'
        d['likeUrl'] = reverse('comments-xtd-like', args=(0,))
        d['dislikeUrl'] = reverse('comments-xtd-dislike', args=(0,))
    return json.dumps(d)
