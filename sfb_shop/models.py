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
        return str(self.amount) + u" /  " + str(self.price)


class PriceModel(CMSPlugin):
    items = models.ManyToManyField(PriceModelItem, verbose_name=u'Preisstufen', related_name='items')
    name = models.CharField(max_length=512, verbose_name=u'Name')

    class Meta:
        verbose_name = u'Preismodel'

    def __unicode__(self):
        return self.name

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
        return self.name


class Item(CMSPlugin):
    name = models.CharField(max_length=200, verbose_name=u'Name')
    description = HTMLField(verbose_name=u'Beschreibung')
    picture = models.ImageField(verbose_name=u'Bild', upload_to=path.join('shop', 'products', 'variants'))
    price = models.ForeignKey(PriceModel)

    def __unicode__(self):
        return self.name


class Card(Item):
    def __unicode__(self):
        return u'Karte: ' + str(self.name)

    class Meta:
        verbose_name = u'Karte für Shop'


class Merch(Item):
    def __unicode__(self):
        return u'Merchandise: ' + str(self.name)

    class Meta:
        verbose_name = u'Merch für Shop'