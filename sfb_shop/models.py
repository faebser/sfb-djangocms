# -*- coding: utf-8 -*-

from django.db import models
from djangocms_text_ckeditor.fields import HTMLField  # html field
from os import path
from django.db import models
from cms.models.pluginmodel import CMSPlugin  # normal cms-plugin
from django.core import serializers
import json
# Models for the sfb-shop


class PriceModelItem(CMSPlugin):
    amount = models.IntegerField(verbose_name=u'Max. Anzahl')
    price = models.DecimalField(verbose_name=u'Preis', max_digits=5, decimal_places=2)

    class Meta:
        verbose_name = u'Preismodel-Eintrag'

    def __unicode__(self):
        return unicode(self.amount) + u" /  " + unicode(self.price)


class PriceModel(CMSPlugin):
    items = models.ManyToManyField(PriceModelItem, verbose_name=u'Preisstufen', related_name='items')
    name = models.CharField(max_length=512, verbose_name=u'Name')

    class Meta:
        verbose_name = u'Preismodel'

    def __unicode__(self):
        return unicode(self.name)

    @property
    def to_json_data(self):
        print "test"
        print json.dumps(self.items)
        #print serializers.serialize('json', PriceModel.objects.get(pk=self.id), fields='items')
        return serializers.serialize('json', PriceModel.objects.get(pk=self.id), fields='items')


class ItemContainer(CMSPlugin):
    name = models.CharField(max_length=200, verbose_name=u'Name')
    description = HTMLField(verbose_name=u'Beschreibung')
    picture = models.ImageField(verbose_name=u'Bild', upload_to=path.join('shop', 'products'))

    def __unicode__(self):
        return unicode(self.name)


class Item(CMSPlugin):
    name = models.CharField(max_length=200, verbose_name=u'Name')
    description = HTMLField(verbose_name=u'Beschreibung')
    picture = models.ImageField(verbose_name=u'Bild', upload_to=path.join('shop', 'products', 'variants'))
    price = models.ForeignKey(PriceModel)

    def __unicode__(self):
        return unicode(self.name)


class Card(Item):
    def __unicode__(self):
        return u'Karte: ' + unicode(self.name)

    class Meta:
        verbose_name = u'Karte für Shop'


class Merch(Item):
    def __unicode__(self):
        return u'Merchandise: ' + unicode(self.name)

    class Meta:
        verbose_name = u'Merch für Shop'


class Category(CMSPlugin):
    title = models.CharField(max_length=64, verbose_name=u'Name')
    description = HTMLField(verbose_name=u'Beschreibung')
    picture = models.ImageField(verbose_name=u'Bild', upload_to=path.join('shop', 'products', 'categories'))
    price = models.ForeignKey(PriceModel)

    class Meta:
        verbose_name = u'the niew thing'

    def __unicode__(self):
        return unicode(self.title)


class NewItem(CMSPlugin):
    name = models.CharField(max_length=64, verbose_name=u'Name')
    picture = models.ImageField(verbose_name=u'kleines Bild', upload_to=path.join('shop', 'products', 'items'))
    bigPicture = models.ImageField(verbose_name=u'grosses Bild', upload_to=path.join('shop', 'products', 'items-big'))

    class Meta:
        verbose_name = u'the other niews things'

    def __unicode__(self):
        return unicode(self.name)