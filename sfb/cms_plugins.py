# -*- coding: utf-8 -*-
__author__ = 'faebser'

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _
from djangocms_text_ckeditor.cms_plugins import TextPlugin
from django.core.urlresolvers import reverse
from models import *
from os import path

class PluginSettings():
    templatePath = path.join("plugins", "sfb")
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

