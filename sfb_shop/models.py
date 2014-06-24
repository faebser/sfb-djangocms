# -*- coding: utf-8 -*-

from django.db import models
from djangocms_text_ckeditor.fields import HTMLField  # html field
from os import path
from django.db import models
from cms.models.pluginmodel import CMSPlugin  # normal cms-plugin
# Models for the sfb-shop


class Item(CMSPlugin):
    name = models.CharField(max_length=200, verbose_name=u'Name')
    description = HTMLField(verbose_name=u'Beschreibung')
    picture = models.ImageField(verbose_name=u'Bild', upload_to=path.join('shop/products'))
    price = models.FloatField(verbose_name=u'Preis')

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

