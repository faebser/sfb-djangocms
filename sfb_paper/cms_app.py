# -*- coding: utf-8 -*-
__author__ = 'faebser'

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool


class ArchiveApphook(CMSApp):
    name = u'Archiv'
    urls = ["sfb_paper.urls"]


apphook_pool.register(ArchiveApphook)
