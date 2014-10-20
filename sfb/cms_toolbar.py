# -*- coding: utf-8 -*-
__author__ = 'faebser'

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool
from cms.toolbar.items import Break, SubMenu
from cms.cms_toolbar import ADMIN_MENU_IDENTIFIER, ADMINISTRATION_BREAK


@toolbar_pool.register
class PriceModelMenu(CMSToolbar):

    menu_key = 'shop'
    verbose_name = 'Shop'

    def populate(self):
        admin_menu = self.toolbar.get_or_create_menu(self.menu_key, self.verbose_name)
        price_models = admin_menu.get_or_create_menu('model', _('Preis-Modelle'))
        price_models.add_modal_item(_(u'Neues Preismodel hinzufügen'), reverse("admin:sfb_shop_pricemodel_add"))
        url = reverse('admin:sfb_shop_pricemodel_changelist')
        price_models.add_sideframe_item(_('Liste der Preismodelle'), url=url)