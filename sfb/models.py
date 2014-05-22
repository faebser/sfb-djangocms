__author__ = 'faebser'

from django.db import models
from cms.models import Page
from cms.models.pluginmodel import CMSPlugin  # normal cms-plugin
from djangocms_text_ckeditor.models import AbstractText  # text plugin
from django.utils.translation import ugettext_lazy as _
import datetime


class SfbDefaultText(AbstractText):
    title = models.CharField(max_length=256)


class SfbArticlePageHeader(AbstractText):
    title = models.CharField(max_length=256, verbose_name=u"Titel")
    author = models.CharField(max_length=256, verbose_name=u"Autor")
    image = models.ImageField(verbose_name=u"Bild", upload_to=CMSPlugin.get_media_path, default="<empty>")
    publicationDate = models.DateTimeField(verbose_name=u"Datum/Zeit", default=datetime.now)
    body = models.TextField(_("body"), verbose_name=u"Abriss")

    def __unicode__(self):
        return "Artikel: " + self.title[0:20] + "... von " + self.author + " / " + str(self.publicationDate.strftime("%Y%m%d%H%M%S"))

    class Meta:
        verbose_name = "Artikel Intro"


class SfbArticleTeaser(AbstractText):
    teaserFor = models.ForeignKey(SfbArticlePageHeader, verbose_name=u"Verweis auf")
    titleOverwrite = models.CharField(max_length=256, verbose_name=u"Titel")
    authorOverwrite = models.CharField(max_length=256, verbose_name=u"Autor")
    imageOverwrite = models.ImageField(verbose_name=u"Bild", upload_to=CMSPlugin.get_media_path, default="<empty>")
    publicationDateOverwrite = models.DateTimeField(verbose_name=u"Datum/Zeit", default=datetime.now)
    bodyOverwrite = models.TextField(_("body"), verbose_name=u"Abriss")

    class Meta:
        verbose_name = "Verweis auf Artikel"


class SfbNewsPageHeader(SfbArticlePageHeader):

    class Meta:
        verbose_name = "News Intro"


class SfbNewsTeaser(SfbArticleTeaser):

    class Meta:
        verbose_name = "Verweis auf eine News"


class SfbPDFLink(CMSPlugin):
    file = models.FileField(verbose_name=u"PDF-Datei", upload_to=CMSPlugin.get_media_path, default="<empty>")
    text = models.CharField(max_length=256, verbose_name=u"Text für Link")

    def __unicode__(self):
        return self.text


class SfbInternalLink(CMSPlugin):
    name = models.CharField(max_length=256, verbose_name=u"Text für Link")
    link = models.ForeignKey(Page, verbose_name=u"interne Seite")

    def __unicode__(self):
        return self.name


class SfbExternalLink(CMSPlugin):
    name = models.CharField(max_length=256, verbose_name=u"Text für Link")
    link = models.URLField(verbose_name=u"externer Link")

    def __unicode__(self):
        return self.name