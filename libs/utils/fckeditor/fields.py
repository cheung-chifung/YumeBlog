from django.db import models
from django import forms

from django.conf import settings

class RichTextWidget(forms.Textarea):
    def __init__(self, attrs=None):
        final_attrs = {'class': 'vRichTextField' ,'dir':settings.FCKEDITOR_MEDIA_URL}
        if attrs is not None:
            final_attrs.update(attrs)
        super(RichTextWidget, self).__init__(attrs=final_attrs)

    class Media:
        js = (settings.FCKEDITOR_MEDIA_URL+'/fckeditor/fckeditor.js',\
              settings.FCKEDITOR_MEDIA_URL + '/fckeditor/fckeditor_init.js')

class RichTextField(models.TextField):
    def __init(self, *args, **kwargs ):
        super(RichTextField, self).__init__(*args, **kwargs)
        
    def get_internal_type(self):
        return "TextField"

    def formfield(self, **kwargs):
        kwargs['widget'] = RichTextWidget
        return super(RichTextField, self).formfield(**kwargs)
