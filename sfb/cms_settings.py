# -*- coding: utf-8 -*-
from os import path
__author__ = 'faebser'

gettext = lambda s: s

CMS_LANGUAGES = {
    ## Customize this
    'default': {
        'hide_untranslated': False,
        'redirect_on_fallback': True,
        'public': True,
    },
    1: [
        {
            'redirect_on_fallback': True,
            'code': 'de',
            'hide_untranslated': False,
            'name': gettext('de'),
            'public': True,
        },
        {
            'redirect_on_fallback': True,
            'code': 'en',
            'hide_untranslated': False,
            'name': gettext('en'),
            'public': True,
        },
    ],
}

CMS_TEMPLATES = (
    ## Customize this
    ('fullwidth.html', 'Fullwidth'),
    ('sidebar_left.html', 'Sidebar Left'),
    ('sidebar_right.html', 'Sidebar Right'),
    ('index.html', 'test'),
    (path.join('pages', 'sfb-default.html'), 'SFB Standard'),
    (path.join('pages', 'sfb-event-news.html'), u'SFB News und Event Detailseite'),
    (path.join('pages', 'sfb-teaser.html'), u'SFB News und Event Übersicht'),
)

CMS_PERMISSION = True

CMS_PLACEHOLDER_CONF = {
    'intro': {
        'plugins': ['ArticlePageIntro'],
        'name': u'Intro',
        'limits': {
            'global': 1
        }
    },
    'pdfbox': {
        'plugins': ['PdfBox'],
        'name': u'PDF-Box',
        'limits': {
            'PdfBox': 1
        }
    },
    'linkbox': {
        'plugins': ['LinkBox'],
        'name': u'Link-Box',
        'limits': {
            'LinkBox': 1
        }
    },
    'teaserList': {
        'plugins': ['ArticlePageTeaser'],
        'name': u'Übersicht mit grossen Teaser'
    },
    'teaserListSmall': {
        'name': u'Liste mit kleinen Teaser',
        'plugins': ['ArticlePageTeaserSmall']
    }
}
