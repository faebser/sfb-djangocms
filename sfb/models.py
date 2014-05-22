__author__ = 'faebser'


from django.db import models
from djangocms_text_ckeditor.models import AbstractText


class SfbDefaultText(AbstractText):
    title = models.CharField(max_length=100)