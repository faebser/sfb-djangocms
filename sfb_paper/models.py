from django.db import models
from cms.models.pluginmodel import CMSPlugin  # normal cms-plugin
from djangocms_text_ckeditor.fields import HTMLField  # html field
from unidecode import unidecode
from django_select2.fields import ModelSelect2Field
from os import path
from csv import reader as csv_reader
from time import strftime

# Create your models here.




VERBOSE_NAME = u'Archiv'


class Tag(models.Model):
    name = models.CharField(max_length=256, verbose_name=u'Name')
    url = models.CharField(max_length=512, editable=False)

    class Meta:
        verbose_name = u'Schlagwort'
        verbose_name_plural = u'Schlagworte'

    def save(self, *args, **kwargs):
        self.url = unidecode(self.name.lower().replace(' ', '_'))
        super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return unicode(self.name)


class TagPlaceholder(CMSPlugin):
    tag = models.ForeignKey(to=Tag, verbose_name=u'Schlagwort')

    def __unicode__(self):
        return unicode(self.tag.name)

    def __str__(self):
        return self.tag.name


class Author(models.Model):
    name = models.CharField(max_length=256, verbose_name=u'Name')

    class Meta:
        verbose_name = u'Autor'
        verbose_name_plural = u'Autoren'

    def __str__(self):
        return self.name


class Download(models.Model):
    def get_path(self, filename):
        return path.join('archiv', 'ausgaben', filename)

    pdf = models.FileField(verbose_name=u'Datei', upload_to=get_path)

    class Meta:
        verbose_name = u'PDF-Datei'
        verbose_name_plural = u'PDF-Dateien'

    def __str__(self):
        return self.pdf.name


class Article(models.Model):
    title = models.CharField(max_length=2048, verbose_name=u'Titel', null=True, blank=False)
    subtitle = models.CharField(max_length=2048, verbose_name=u'Untertitel', null=True, blank=False)
    authors = models.ManyToManyField(Author, verbose_name=u'Autoren')
    issue = models.ForeignKey('Issue', verbose_name=u'Ausgabe')
    page = models.IntegerField(verbose_name=u'Seite', default=0, null=True)
    tags = models.ManyToManyField(Tag, verbose_name=u'Schlagworte')

    class Meta:
        verbose_name = u'Artikel'
        verbose_name_plural = u'Artikel'

    def __str__(self):
        return self.title


class ArticleList(CMSPlugin):
    amount = models.IntegerField(verbose_name=u'Anzahl')


class Issue(CMSPlugin):
    name = models.CharField(max_length=256, verbose_name=u'Name')
    year = models.IntegerField(verbose_name=u'Jahr')
    month = models.FloatField(verbose_name=u'Monat')
    download = models.ForeignKey(Download, verbose_name=u'Download')
    date_sort = models.IntegerField(editable=False)

    class Meta:
        ordering = ['-date_sort']
        verbose_name = u'Ausgabe'
        verbose_name_plural = u'Ausgaben'

    def save(self, *args, **kwargs):
        self.date_sort = self.year + (self.month * 0.1)
        super(Issue, self).save(*args, **kwargs)


class ImporterFile(CMSPlugin):
    def generate_path(self, filename):
        if len(filename.split('.')) > 1:
            filename = filename.split('.')[0] + '_' + strftime('%Y_%m_%d_%H_%M_%S') + '.' + filename.split('.')[1]
        return path.join('archiv', 'csv-daten', filename)

    csv_file = models.FileField(verbose_name=u'CSV-Datei', upload_to=generate_path)

    class Meta:
        verbose_name = u'CSV-Datei'
        verbose_name_plural = u'CSV-Dateien'

    def __str__(self):
        return self.csv_file.name

    def save(self, *args, **kwargs):
        # save first to write file to disk
        super(ImporterFile, self).save(*args, **kwargs)
        print self.csv_file.path
        with open(self.csv_file.path) as csv_file:
            csv_to_models_importer(csv_file)
        print 'finished'


def csv_to_models_importer(csv_file):
    reader = csv_reader(csv_file, delimiter=';')
    for row in reader:
        print ','.join(row)
    return