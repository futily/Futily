from django.db import models
from django.db.models import F, Max, Min
from django_comments_xtd.models import XtdComment

from futily.apps.users.models import User


class FlyComment(XtdComment):
    score = models.IntegerField(default=0, blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.user_id and not self.user_url:
            self.user_url = User.objects.get(pk=self.user_id).get_absolute_url()
            self.score = 0

            self.save()

    def _calculate_thread_data(self):
        # Implements the following approach:
        #  http://www.sqlteam.com/article/sql-for-threaded-discussion-forums
        parent = XtdComment.objects.get(pk=self.parent_id)

        self.thread_id = parent.thread_id
        self.level = parent.level + 1
        qc_eq_thread = XtdComment.objects.filter(thread_id=parent.thread_id)
        qc_ge_level = qc_eq_thread.filter(level__lte=parent.level,
                                          order__gt=parent.order)
        if qc_ge_level.count():
            min_order = qc_ge_level.aggregate(Min('order'))['order__min']
            XtdComment.objects\
                .filter(thread_id=parent.thread_id, order__gte=min_order)\
                .update(order=F('order') + 1)
            self.order = min_order
        else:
            max_order = qc_eq_thread.aggregate(Max('order'))['order__max']
            self.order = max_order + 1
