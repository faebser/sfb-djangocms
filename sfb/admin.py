__author__ = 'faebser'

from django.contrib import admin
from sfb_shop import models
from sfb_paper import models as paper

admin.site.register(models.PriceModelItem)
admin.site.register(models.PriceModel)

admin.site.register(paper.Tag)
admin.site.register(paper.Author)
admin.site.register(paper.Article)
admin.site.register(paper.Download)
admin.site.register(paper.Issue)
