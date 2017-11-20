from django import forms
from django_comments_xtd.forms import XtdCommentForm


class FlyCommentForm(XtdCommentForm):
    score = forms.IntegerField(required=False)

    def get_comment_create_data(self, site_id=None):
        data = super(FlyCommentForm, self).get_comment_create_data(site_id)
        data.update({'score': self.cleaned_data['score']})

        return data
