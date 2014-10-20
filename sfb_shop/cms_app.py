# -*- coding: utf-8 -*-
__author__ = 'faebser'

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool


class ShopApphook(CMSApp):
    name = u'Shop-Seite'
    urls = ["sfb_shop.urls"]


print "bla"
apphook_pool.register(ShopApphook)
