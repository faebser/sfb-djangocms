# -*- coding: utf-8 -*-
__author__ = 'faebser'

from django.db import models
from cms.models import Page
from cms.models.pluginmodel import CMSPlugin  # normal cms-plugin
from djangocms_text_ckeditor.models import AbstractText  # text plugin
from djangocms_text_ckeditor.fields import HTMLField  # html field
from django.utils.translation import ugettext_lazy as _
import datetime


class SfbDefaultText(AbstractText):
    title = models.CharField(max_length=256)


class SfbArticlePageHeader(CMSPlugin):
    title = models.CharField(max_length=256, verbose_name=u"Titel")
    author = models.CharField(max_length=256, verbose_name=u"Autor")
    image = models.ImageField(verbose_name=u"Bild", upload_to=CMSPlugin.get_media_path, default="<empty>")
    publicationDate = models.DateTimeField(verbose_name=u"Datum/Zeit", default=datetime.datetime.now())
    body = HTMLField(verbose_name=u"Abriss")

    def __unicode__(self):
        return "Artikel: " + self.title[0:20] + "... von " + self.author + " / " + str(self.publicationDate.strftime("%H:%M:%S %m/%d/%Y"))

    class Meta:
        verbose_name = "Artikel Intro"


class SfbArticleTeaser(CMSPlugin):
    teaserFor = models.ForeignKey(SfbArticlePageHeader, verbose_name=u"Verweis auf")
    titleOverwrite = models.CharField(max_length=256, verbose_name=u"Titel")
    authorOverwrite = models.CharField(max_length=256, verbose_name=u"Autor")
    imageOverwrite = models.ImageField(verbose_name=u"Bild", upload_to=CMSPlugin.get_media_path, default="<empty>")
    publicationDateOverwrite = models.DateTimeField(verbose_name=u"Datum/Zeit", default=datetime.datetime.now())
    bodyOverwrite = models.TextField(verbose_name=u"Abriss")

    class Meta:
        verbose_name = "Verweis auf Artikel"


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
    pdfFile = models.FileField(verbose_name=u"PDF-Datei", upload_to=CMSPlugin.get_media_path, default="<empty>")
    text = models.CharField(max_length=256, verbose_name=u"Text für Link")

    def __unicode__(self):
        return self.text


class SfbInternalLink(CMSPlugin):
    name = models.CharField(max_length=256, verbose_name=u"Text für Link")
    internalHref = models.ForeignKey(Page, verbose_name=u"interne Seite")
    target = models.CharField(verbose_name=u'Öffnen in', blank=True, default=("_blank", u"gleichem Fenster"), max_length=100, choices=((
        ("", _("gleichem Fenster")),
        ("_blank", _("neuem Fenster")),
    )))

    def __unicode__(self):
        return self.name


class SfbExternalLink(CMSPlugin):
    name = models.CharField(max_length=256, verbose_name=u"Text für Link")
    externalHref = models.URLField(verbose_name=u"externer Link")
    target = models.CharField(verbose_name=u'Öffnen in', blank=True, default=("_blank", u"gleichem Fenster"), max_length=100, choices=((
        ("", _("gleichem Fenster")),
        ("_blank", _("neuem Fenster")),
    )))

    def __unicode__(self):
        return self.name