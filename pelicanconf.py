#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

SITENAME = 'Kevin Yap'

# Custom text for index page meta description, biography, and footer
INDEX_DESCRIPTION = 'Website and blog of Kevin Yap, a developer and musician from Vancouver, BC.'
BIO_TEXT = 'Developer and musician from Vancouver, BC.'
FOOTER_TEXT = 'Powered by <a href="http://getpelican.com">Pelican</a> and <a href="http://pages.github.com">GitHub&nbsp;Pages</a>.'

RELATIVE_URLS = True

THEME = 'theme'
TYPOGRIFY = True
TIMEZONE = 'America/Vancouver'
DEFAULT_DATE_FORMAT = '%B %d, %Y'
DEFAULT_PAGINATION = False
SUMMARY_MAX_LENGTH = 30

SITE_AUTHOR = 'Kevin Yap'
TWITTER_USERNAME = '@iKevinY'
GOOGLE_PLUS_URL = 'https://plus.google.com/+KevinYapCA'

ARTICLE_URL = '{date:%Y}/{date:%m}/{slug}/'
ARTICLE_SAVE_AS = ARTICLE_URL + 'index.html'

PAGE_URL = '{slug}/'
PAGE_SAVE_AS = PAGE_URL + 'index.html'

ARCHIVES_SAVE_AS = 'archive/index.html'

YEAR_ARCHIVE_SAVE_AS = '{date:%Y}/index.html'
MONTH_ARCHIVE_SAVE_AS = '{date:%Y}/{date:%m}/index.html'

# Disables authors, categories, and tags pages
AUTHORS_SAVE_AS = False
CATEGORIES_SAVE_AS = False
TAGS_SAVE_AS = ''

# Disables Atom feed generation
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

MD_EXTENSIONS = ['admonition', 'codehilite(linenums=True)', 'extra']

DELETE_OUTPUT_DIRECTORY = True
OUTPUT_PATH = 'develop/'
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

# Creates icons for social links using the format ('link', 'hover text', 'icon')
SOCIAL = [
    ('m&#97;&#105;l&#116;o&#58;me&#64;&#107;e&#118;inya%7&#48;&#46;ca', 'Email', 'fa fa-envelope-o'),
    ('http://twitter.com/iKevinY', 'Twitter', 'fa fa-twitter'),
    ('http://plus.google.com/+KevinYapCA', 'Google+', 'fa fa-google-plus-square'),
    ('http://github.com/iKevinY', 'GitHub', 'fa fa-github'),
    ('http://soundcloud.com/iKevinY', 'SoundCloud', 'fa fa-soundcloud'),
]

PLUGIN_PATH = 'plugins'
PLUGINS = ['assets', 'neighbors', 'render_math']
MATH = {'auto_insert': False}

# Configuration for the Assets plugin
ASSET_CONFIG = (
	('url_expire', False),
	('versions', False),
	('manifest', False),
	('cache', False),
)
