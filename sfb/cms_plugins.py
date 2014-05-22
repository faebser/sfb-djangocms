__author__ = 'faebser'

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _
from djangocms_text_ckeditor.cms_plugins import TextPlugin
from models import SfbDefaultText
from os import path


pluginSettings = {
    'path': path.join("plugins", "sfb")
}


class DefaultPlugin(TextPlugin):
    name = _(u"Text")
    module = _(u"SFB")
    model = SfbDefaultText
    render_template = path.join(pluginSettings['path'], "default_plugin.html")

plugin_pool.register_plugin(DefaultPlugin)