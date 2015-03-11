# -*- coding: utf-8 -*-
__author__ = 'faebser'

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _
from djangocms_text_ckeditor.cms_plugins import TextPlugin
from django.core.urlresolvers import reverse
import json
from models import *
from os import path
from sfb_shop import models as shop
from sfb_paper import models as paper
from collections import OrderedDict
from django.db.models import Count
from datetime import datetime


class PluginSettings():
    templatePath = path.join("plugins", "sfb")
    templatePathShop = path.join('plugins', 'shop')
    templatePathPaper = path.join('plugins', 'paper')
    module = u'SFB'

ps = PluginSettings()


class DefaultPlugin(TextPlugin):
    name = _(u"Text")
    module = ps.module
    model = SfbDefaultText
    render_template = path.join(ps.templatePath, "text.html")

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        return context


class ArticlePageIntro(CMSPluginBase):
    name = u'Artikel Intro'
    module = ps.module
    model = SfbArticlePageHeader
    render_template = path.join(ps.templatePath, "intro.html")


class ArticlePageTeaser(CMSPluginBase):
    name = u"Artikel Teaser gross"
    module = ps.module
    model = SfbArticleTeaser
    render_template = path.join(ps.templatePath, "teaser.html")

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        context['teaser'] = instance.teaserFor
        context['url'] = instance.teaserFor.page.get_absolute_url()
        return context


class ArticlePageTeaserSmall(ArticlePageTeaser):
    name = u"Artikel Teaser klein"
    render_template = path.join(ps.templatePath, "teaser_small.html")

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        context['teaser'] = instance.teaserFor
        context['url'] = instance.teaserFor.page.get_absolute_url()
        if not instance.imageOverwrite and not instance.teaserFor.image:
            context['noImageCssClass'] = True
        return context


class NewsPageIntro(CMSPluginBase):
    name = u"News Intro"
    module = ps.module
    model = SfbNewsPageHeader
    render_template = path.join(ps.templatePath, "intro.html")


class NewsPageTeaser(CMSPluginBase):
    name = u'News Teaser'
    module = ps.module
    model = SfbNewsTeaser
    render_template = path.join(ps.templatePath, "default_plugin.html")


class PdfBox(CMSPluginBase):
    name = u'PDF-Box'
    module = ps.module
    model = SfbPDFBox
    render_template = path.join(ps.templatePath, "link-box.html")
    allow_children = True
    child_classes = ["PdfLink"]

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        context['cssClass'] = "box pdf"
        context['title'] = u"Downloads"
        return context


class PdfLink(CMSPluginBase):
    name = u'PDF'
    module = ps.module
    model = SfbPDFLink
    render_template = path.join(ps.templatePath, "link.html")

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        context['cssClass'] = "pdf"
        context['url'] = instance.href.url
        return context


class LinkBox(CMSPluginBase):
    name = u'Link-Box'
    module = ps.module
    model = SfbLinkBox
    render_template = path.join(ps.templatePath, "link-box.html")
    allow_children = True
    child_classes = ["InternalLink", "ExternalLink"]

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        context['cssClass'] = "box linklist"
        context['title'] = u"Links"
        return context


class InternalLink(CMSPluginBase):
    name = u'Interner Link'
    module = ps.module
    model = SfbInternalLink
    render_template = path.join(ps.templatePath, "link.html")

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        context['cssClass'] = "internal"
        context['url'] = instance.href.get_absolute_url()
        return context


class ExternalLink(CMSPluginBase):
    name = u'Externer Link'
    module = ps.module
    model = SfbExternalLink
    render_template = path.join(ps.templatePath, "link.html")

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        context['cssClass'] = "external"
        context['url'] = instance.href
        return context


class ShopContainer(CMSPluginBase):
    name = u'Artikel'
    model = shop.ItemContainer
    module = ps.module + ' Shop'
    allow_children = True
    child_classes = ["ShopCard", "ShopMerch"]
    render_template = path.join(ps.templatePathShop, 'container.html')


class ShopCategory(CMSPluginBase):
    name = u'Artikel-Kategorie'
    model = shop.Category
    module = ps.module + ' Shop'
    allow_children = True
    child_classes = ['ShopNewItem']
    render_template = path.join(ps.templatePathShop, 'category.html')

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        dump = list()
        for item in instance.price.items.all():
            dump.append({
                'amount': str(item.amount),
                'price': float(item.price)
            })
        context['priceData'] = json.dumps(dump)
        return context


class ShopNewItem(CMSPluginBase):
    name = u'Neuer Artikel'
    model = shop.NewItem
    module = ps.module + ' Shop'
    render_template = path.join(ps.templatePathShop, 'newItem.html')


class ShopCard(CMSPluginBase):
    name = u'Karte'
    model = shop.Card
    module = ps.module + ' Shop'
    render_template = path.join(ps.templatePathShop, 'item.html')

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        context['type'] = 'card'
        if instance.picture.height >= instance.picture.width:
            context['cssClass'] = 'high'
        else:
            context['cssClass'] = 'wide'
        dump = dict()
        for item in instance.price.items.all():
            dump[str(item.amount)] = float(item.price)
        context['priceData'] = json.dumps(dump)
        return context


class ShopMerch(CMSPluginBase):
    name = u'Artikel'
    model = shop.Merch
    module = ps.module + ' Shop'
    render_template = path.join(ps.templatePathShop, 'item.html')

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        context['type'] = 'merch'
        return context


class TagContainer(CMSPluginBase):
    name = u'Schlagworte Schwerpunkte'
    module = ps.module + ' Archiv'
    render_template = path.join(ps.templatePathPaper, 'tag-container.html')
    allow_children = True


class PaperTag(CMSPluginBase):
    name = u'Schlagwort'
    module = ps.module + ' Archiv'
    model = paper.TagPlaceholder
    render_template = path.join(ps.templatePathPaper, 'tag.html')


class ArticleList(CMSPluginBase):
    name = u'Chronologische Übersicht'
    module = ps.module + ' Archiv'
    model = paper.ArticleList
    cache = False
    render_template = path.join(ps.templatePathPaper, 'issues.html')

    def render(self, context, instance, placeholder):
        start_year = context['request'].GET.get('pagination', None) or datetime.now().year
        start_year = int(start_year)
        end_year = start_year - instance.amount + 1
        context['instance'] = instance
        years = OrderedDict()
        for issue in paper.Issue.objects.all().filter(year__lte=start_year).order_by('-date_sort'):
            year_as_string = str(issue.year)
            if issue.year < end_year:
                break
            if year_as_string not in years:
                years[year_as_string] = [issue]
            else:
                years[year_as_string].append(issue)

        num_paginaton = paper.Issue.objects.all().filter(year__lte=end_year-1).count()

        context.update({
            'years': years,
            'pagination': end_year - 1,
            'num_pagination': num_paginaton
        })

        return context


class SearchPlugin(CMSPluginBase):
    name = u'Suche'
    module = ps.module + ' Archiv'
    render_template = path.join(ps.templatePathPaper, 'search.html')


class MostUsedTagsPlugin(CMSPluginBase):
    name = u'Beliebte Schlagworte'
    module = ps.module + ' Archiv'
    render_template = path.join(ps.templatePathPaper, 'mostusedtags.html')

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        context['tags'] = paper.Tag.objects.annotate(num_articles=Count('article')).order_by('-num_articles')
        return context


plugin_pool.register_plugin(DefaultPlugin)
plugin_pool.register_plugin(ArticlePageIntro)
plugin_pool.register_plugin(ArticlePageTeaser)
plugin_pool.register_plugin(ArticlePageTeaserSmall)
plugin_pool.register_plugin(NewsPageIntro)
plugin_pool.register_plugin(NewsPageTeaser)
plugin_pool.register_plugin(PdfBox)
plugin_pool.register_plugin(LinkBox)
plugin_pool.register_plugin(PdfLink)
plugin_pool.register_plugin(InternalLink)
plugin_pool.register_plugin(ExternalLink)

#shop
plugin_pool.register_plugin(ShopContainer)
plugin_pool.register_plugin(ShopCard)
plugin_pool.register_plugin(ShopMerch)
plugin_pool.register_plugin(ShopCategory)
plugin_pool.register_plugin(ShopNewItem)


#paper
plugin_pool.register_plugin(TagContainer)
plugin_pool.register_plugin(PaperTag)
plugin_pool.register_plugin(ArticleList)
plugin_pool.register_plugin(SearchPlugin)
plugin_pool.register_plugin(MostUsedTagsPlugin)
