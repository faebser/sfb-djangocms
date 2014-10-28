from django.db import models
from cms.models.pluginmodel import CMSPlugin  # normal cms-plugin
from djangocms_text_ckeditor.fields import HTMLField  # html field

# Create your models here.


def get_path(self, filename):
        return 'bla'


class Tag(models.Model):
    name = models.CharField(max_length=256, verbose_name=u'Name')


class Author(models.Model):
    name = models.CharField(max_length=256, verbose_name=u'Name')


class Download(models.Model):
    pdf = models.FileField(verbose_name=u'Datei', upload_to=get_path)


class Article(models.Model):
    authors = models.ManyToManyField(Author, verbose_name=u'Autoren')
    issue = models.ForeignKey('Issue', verbose_name=u'Ausgabe')
    download = models.ForeignKey(Download, verbose_name=u'Download')
    tags = models.ManyToManyField(Tag, verbose_name=u'Schlagworte')


class Issue(CMSPlugin):
    name = models.CharField(max_length=256, verbose_name=u'Name')
    year = models.IntegerField(verbose_name=u'Jahr')
    month = models.IntegerField(verbose_name=u'Monat')
    download = models.ForeignKey(Download, verbose_name=u'Download')

