#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Site-specific settings (used by theme)
SITENAME = 'Kevin Yap'
INDEX_DESCRIPTION = 'Website and blog of Kevin Yap, a developer and musician from Vancouver, BC.'
BIO_TEXT = 'Developer and musician from Vancouver, BC.'
FOOTER_TEXT = 'Powered by <a href="http://getpelican.com">Pelican</a> and <a href="http://pages.github.com">GitHub&nbsp;Pages</a>.'

SITE_AUTHOR = 'Kevin Yap'
TWITTER_USERNAME = '@iKevinY'
GOOGLE_PLUS_URL = 'https://plus.google.com/+KevinYapCA'

SOCIAL_ICONS = [
    ('m&#97;&#105;l&#116;o&#58;me&#64;&#107;e&#118;inya&#112;&#46;ca', 'Email', 'fa fa-envelope'),
    ('http://twitter.com/iKevinY', 'Twitter', 'fa fa-twitter'),
    ('http://plus.google.com/+KevinYapCA', 'Google+', 'fa fa-google-plus-square'),
    ('http://github.com/iKevinY', 'GitHub', 'fa fa-github'),
    ('http://soundcloud.com/iKevinY', 'SoundCloud', 'fa fa-soundcloud'),
]

# General Pelican settings
RELATIVE_URLS = True
SITEURL = 'http://localhost'
THEME = 'theme'
TIMEZONE = 'America/Vancouver'

DEFAULT_DATE_FORMAT = '%B %d, %Y'
DEFAULT_PAGINATION = False

ARTICLE_URL = '{date:%Y}/{date:%m}/{slug}/'
ARTICLE_SAVE_AS = ARTICLE_URL + 'index.html'
PAGE_URL = '{slug}/'
PAGE_SAVE_AS = PAGE_URL + 'index.html'
ARCHIVES_SAVE_AS = 'archive/index.html'
YEAR_ARCHIVE_SAVE_AS = '{date:%Y}/index.html'
MONTH_ARCHIVE_SAVE_AS = '{date:%Y}/{date:%m}/index.html'

# Disables authors, categories, and tags pages
AUTHORS_SAVE_AS = ''
CATEGORY_SAVE_AS = ''
CATEGORIES_SAVE_AS = ''
TAGS_SAVE_AS = ''

# Disables Atom feed generation
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

TYPOGRIFY = True
MD_EXTENSIONS = ['admonition', 'codehilite(linenums=True)', 'extra']

DELETE_OUTPUT_DIRECTORY = True
OUTPUT_PATH = 'develop/'
CACHE_CONTENT = False
PATH = 'content/'

TEMPLATE_PAGES = {
	'404.html': '404.html',
}

STATIC_PATHS = ['images', 'uploads', 'extra']

EXTRA_PATH_METADATA = {
    'extra/CNAME': {'path': 'CNAME'},
    'extra/favicon.ico': {'path': 'favicon.ico'},
    'extra/robots.txt': {'path': 'robots.txt'},
}

PLUGIN_PATH = ['plugins']
PLUGINS = ['assets', 'neighbors']
ASSET_CONFIG = (
	('url_expire', False),
	('versions', False),
	('manifest', False),
	('cache', False),
)
