from django.db import models
from cms.models.pluginmodel import CMSPlugin  # normal cms-plugin
from djangocms_text_ckeditor.fields import HTMLField  # html field
from unidecode import unidecode
from os import path
from csv import reader as csv_reader
from time import strftime
from django.utils.encoding import smart_text
import codecs

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
    firstname = models.CharField(max_length=256, verbose_name=u'Vorname', blank=True, null=True)
    name = models.CharField(max_length=256, verbose_name=u'Name')

    class Meta:
        verbose_name = u'Autor'
        verbose_name_plural = u'Autoren'

    def __unicode__(self):
        if self.firstname is None:
            return unicode(self.name)
        else:
            return u"{} {}".format(self.firstname, self.name)


class Download(models.Model):
    def get_path(self, filename):
        return path.join('archiv', 'ausgaben', filename)

    pdf = models.FileField(verbose_name=u'Datei', upload_to=get_path)

    class Meta:
        verbose_name = u'PDF-Datei'
        verbose_name_plural = u'PDF-Dateien'

    def __unicode__(self):
        return self.pdf.name

    def __str__(self):
        return self.pdf.name


class Article(models.Model):
    title = models.CharField(max_length=2048, verbose_name=u'Titel', null=True, blank=True)
    subtitle = models.CharField(max_length=2048, verbose_name=u'Untertitel', null=True, blank=True)
    authors = models.ManyToManyField(Author, verbose_name=u'Autoren', null=True, blank=True)
    issue = models.ForeignKey('Issue', verbose_name=u'Ausgabe')
    page = models.IntegerField(verbose_name=u'Seite', default=0, null=True)
    tags = models.ManyToManyField(Tag, verbose_name=u'Schlagworte', null=True, blank=True)
    csv_id = models.IntegerField(editable=False, blank=True, null=True)

    class Meta:
        ordering = ['-page']
        verbose_name = u'Artikel'
        verbose_name_plural = u'Artikel'

    def __str__(self):
        return self.title

    def __unicode__(self):
        return unicode(self.title)


class ArticleList(CMSPlugin):
    amount = models.IntegerField(verbose_name=u'Anzahl Jahre zur Darstellung', default=3)


class Issue(CMSPlugin):
    def generate_path(self, filename):
        return path.join('archiv', 'frontseiten', filename)

    name = models.CharField(max_length=256, verbose_name=u'Name', blank=True, null=True, default='')
    year = models.IntegerField(verbose_name=u'Jahr')
    month = models.IntegerField(verbose_name=u'Monat')
    download = models.ForeignKey(Download, verbose_name=u'Download', blank=True, null=True)
    front = models.ImageField(verbose_name=u'Frontseite', upload_to=generate_path, blank=True, null=True)
    date_sort = models.IntegerField(editable=False)

    def __unicode__(self):
        if self.download is None:
            return u"{} {}".format(self.name, u'Kein Download vorhanden')
        else:
            return unicode(self.name)

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
    issues = dict()
    issues_qs = Issue.objects.all()
    articles = dict()
    articles_qs = Article.objects.all()
    authors = dict()
    authors_qs = Author.objects.all()
    tags = dict()
    tags_qs = Tag.objects.all()
    # try to save at the very end, so not to leave the db in a messed up state

    # read row
    # get id
    # check dict for article
    # in not in dict, check db
    # if not in db, create new object
    # put object in dict
    #
    # get month and year
    # check dict for an issue
    # if not in dict, check db
    # if not in db, create a new object
    # put object in dict, link with article
    #
    # get author
    # split string to get all authors
    # parse string go get first and lastname
    # check dict
    # if not in dict, check db
    # if not in db, create new object
    # put into dict, link with article
    #
    # get tag
    # parse tags to get all the tags
    # check dict
    # if not in dict, check db
    # if not in db, create object
    # put object in dict, link with article

    # save all objects
    for row in reader:
        print ','.join(row)
        if 'Artikel-ID' in row[0]:
            continue # header row
        else:
            article = get_or_create_article(row, articles, articles_qs)
            issue = get_or_create_issue(row, issues, issues_qs)
            issue.save()
            article.issue = issue
            article.save()
            article.tags.clear()
            for tag_name in row[8].split('+'):
                tag = get_or_create_tag(tag_name, tags, tags_qs)
                article.tags.add(tag)
            for author_name in row[7].split('/ '):
                if len(author_name) > 0 and ', ' in author_name:
                    # author with lastname and firstname
                    lastname, firstname = author_name.split(', ')
                    author = get_or_create_author_with_lastname(firstname, lastname, authors, authors_qs)
                else:
                    # only name
                    author = get_or_create_author_with_name(author_name, authors, authors_qs)
                article.authors.add(author)
            #if article.authors is None:
            #    print 'no authors'
            #    pass
            # article.save()
    return


def get_or_create_article(row, articles, queryset):
    csv_id, name, year, month, page, title, subtitle, author, tags = row
    if csv_id in articles:
        article = articles[csv_id]
    else:
        if bool(queryset.filter(csv_id=csv_id)):
            article = queryset.filter(csv_id=csv_id).first()
        else:
            article = Article()
        articles[csv_id] = article

    # adding or modyfing values in article
    if article.title is None or article.title != smart_text(title):
        article.title = smart_text(title)
    if article.subtitle is None or article.subtitle != smart_text(subtitle):
        article.subtitle = smart_text(subtitle)
    if article.page is None or article.page != page:
        article.page = page
    if article.csv_id is None:
        article.csv_id = csv_id
    return article


def get_or_create_issue(row, issues, queryset):
    csv_id, name, year, month, page, title, subtitle, author, tags = row
    if name in issues:
        issue = issues[name]
    else:
        if bool(queryset.filter(name=name)):
            issue = queryset.filter(name=name).first()
        else:
            issue = Issue()
        issues[name] = issue
    if issue.name is None or issue.name != name:
        issue.name = smart_text(name)
    if issue.year is None or issue.year != year:
        issue.year = int(year)
    if issue.month is None or issue.month != month:
        issue.month = float(month)
    return issue


def get_or_create_tag(name, tags, queryset):
    if name in tags:
        tag = tags[name]
    else:
        if bool(queryset.filter(name__iexact=name)):
            tag = queryset.filter(name__iexact=name).first()
        else:
            tag = Tag()
        if tag.name is None or tag.name != name:
            tag.name = smart_text(name)
        tags[name] = tag
        tag.save()
    return tag


def get_or_create_author_with_lastname(firstname, lastname, authors, queryset):
    id_string = firstname + "_" + lastname
    if id_string in authors:
        author = authors[id_string]
    else:
        if bool(queryset.filter(name__iexact=lastname, firstname__iexact=firstname)):
            author = queryset.filter(name__iexact=lastname, firstname__iexact=firstname).first()
        else:
            author = Author()
        if author.name is None or author.name != smart_text(lastname):
            author.name = smart_text(lastname)
        if author.firstname is None or author.firstname != smart_text(firstname):
            author.firstname = smart_text(firstname)
        author.save()
        authors[id_string] = author
    return author


def get_or_create_author_with_name(name, authors, queryset):
    if name in authors:
        author = authors[name]
    else:
        if bool(queryset.filter(name__iexact=name)):
            author = queryset.filter(name__iexact=name).first()
        else:
            author = Author()
        if author.name is None or author.name != smart_text(name):
            author.name = smart_text(name)
        author.save()
        authors[name] = author
    return author