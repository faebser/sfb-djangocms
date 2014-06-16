# -*- coding: utf-8 -*-
__author__ = 'faebser'

from django.db import models
from cms.models import Page
from cms.models.pluginmodel import CMSPlugin  # normal cms-plugin
from djangocms_text_ckeditor.models import AbstractText  # text plugin
from djangocms_text_ckeditor.fields import HTMLField  # html field
from django.utils.translation import ugettext_lazy as _
from django.utils.text import Truncator
from django.utils.html import strip_tags
import datetime


class SfbDefaultText(AbstractText):
    def __unicode__(self):
        return Truncator(strip_tags(self.body)).words(3, truncate="...")

    class Meta:
        verbose_name = u'Text'


class SfbArticlePageHeader(CMSPlugin):
    title = models.CharField(max_length=256, verbose_name=u"Titel")
    author = models.CharField(max_length=256, verbose_name=u"Autor")
    image = models.ImageField(verbose_name=u"Bild", upload_to=CMSPlugin.get_media_path, blank=True, null=True)
    publicationDate = models.DateTimeField(verbose_name=u"Datum/Zeit", default=datetime.datetime.now())
    body = HTMLField(verbose_name=u"Abriss")

    def __unicode__(self):
        return "Artikel: " + self.title[0:25] + "... von " + self.author + " / " + str(self.publicationDate.strftime("%H:%M:%S %m/%d/%Y"))

    class Meta:
        verbose_name = "Artikel Intro"


class SfbArticleTeaser(CMSPlugin):
    teaserFor = models.ForeignKey(SfbArticlePageHeader, verbose_name=u"Verweis auf")
    titleOverwrite = models.CharField(max_length=256, verbose_name=u"Titel", blank=True, null=True)
    authorOverwrite = models.CharField(max_length=256, verbose_name=u"Autor", blank=True, null=True)
    imageOverwrite = models.ImageField(verbose_name=u"Bild", upload_to=CMSPlugin.get_media_path, blank=True, null=True)
    publicationDateOverwrite = models.DateTimeField(verbose_name=u"Datum/Zeit", default=datetime.datetime.now(), blank=True, null=True)
    bodyOverwrite = HTMLField(verbose_name=u"Abriss", blank=True, null=True)

    class Meta:
        verbose_name = "Verweis auf Artikel"

    def __unicode__(self):
        return "Artikel: " + self.teaserFor.title[0:25] + "... von " + self.teaserFor.author + " / " + str(self.teaserFor.publicationDate.strftime("%H:%M:%S %m/%d/%Y"))


class SfbNewsPageHeader(SfbArticlePageHeader):

    class Meta:
        verbose_name = "News Intro"


class SfbNewsTeaser(SfbArticleTeaser):
    class Meta:
        verbose_name = "Verweis auf eine News"


class SfbPDFBox(CMSPlugin):

    def __unicode__(self):
        return u'PDF-Box'


class SfbLinkBox(CMSPlugin):

    def __unicode__(self):
        return u'Link-Box'


class SfbPDFLink(CMSPlugin):
    href = models.FileField(verbose_name=u"PDF-Datei", upload_to=CMSPlugin.get_media_path)
    name = models.CharField(max_length=256, verbose_name=u"Text für Link")

    def __unicode__(self):
        return self.name


class SfbInternalLink(CMSPlugin):
    name = models.CharField(max_length=256, verbose_name=u"Text für Link")
    href = models.ForeignKey(Page, verbose_name=u"interne Seite")
    target = models.CharField(verbose_name=u'Öffnen in', blank=True, default=("_blank", u"gleichem Fenster"), max_length=100, choices=((
        ("", _("gleichem Fenster")),
        ("_blank", _("neuem Fenster")),
    )))

    def __unicode__(self):
        return self.name


class SfbExternalLink(CMSPlugin):
    name = models.CharField(max_length=256, verbose_name=u"Text für Link")
    href = models.URLField(verbose_name=u"externer Link")
    target = models.CharField(verbose_name=u'Öffnen in', blank=True, default=("_blank", u"gleichem Fenster"), max_length=100, choices=((
        ("", _("gleichem Fenster")),
        ("_blank", _("neuem Fenster")),
    )))

    def __unicode__(self):
        return self.name