__author__ = 'faebser'

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _
from djangocms_text_ckeditor.cms_plugins import TextPlugin
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
    render_template = path.join(ps.templatePath, "default_plugin.html")


class ArticlePageIntro(TextPlugin):
    name = u'Artikel Intro'
    module = ps.module
    model = SfbArticlePageHeader
    render_template = path.join(ps.templatePath, "default_plugin.html")


plugin_pool.register_plugin(DefaultPlugin)