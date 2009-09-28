from django import forms
from django.forms.models import modelformset_factory
from django.db import models
from django.utils.translation import ugettext as _

from models import Comment,COMMENT_MAX_LENGTH

class CommentForm(forms.ModelForm):
    comment = forms.CharField(
        label = _('Leave a comment'),
        max_length = COMMENT_MAX_LENGTH,
        widget = forms.Textarea
    )
    class Meta:
        model = Comment
        fields = ('user_name', 'user_email', 'user_url', 'comment', 'parent', 'is_notice')
