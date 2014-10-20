__author__ = 'faebser'

from django.contrib import admin
from sfb_shop import models

admin.site.register(models.PriceModelItem)
admin.site.register(models.PriceModel)
