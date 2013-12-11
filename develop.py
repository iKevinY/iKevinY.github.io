#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

SITENAME = 'Kevin Yap'
SITEURL = ''

# Custom text for index page meta description, biography, and footer
INDEX_DESCRIPTION = 'Website and blog of Kevin Yap, a developer and musician from Vancouver, BC.'
BIO_TEXT = 'Developer and musician from Vancouver, BC.'
FOOTER_TEXT = 'Powered by <a href="http://getpelican.com">Pelican</a> and <a href="http://pages.github.com">GitHub&nbsp;Pages</a>.'

RELATIVE_URLS = True

THEME = 'simply'
TYPOGRIFY = True
TIMEZONE = 'America/Vancouver'
DEFAULT_DATE_FORMAT = '%B %d, %Y'

ARTICLE_URL = '{date:%Y}/{date:%m}/{slug}/'
ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{slug}/index.html'

PAGE_URL = '{slug}.html'
PAGE_SAVE_AS = '{slug}.html'

YEAR_ARCHIVE_SAVE_AS = '{date:%Y}/index.html'
MONTH_ARCHIVE_SAVE_AS = '{date:%Y}/{date:%m}/index.html'

# Disables archive, author, and tag pages
ARCHIVES_SAVE_AS = False
AUTHOR_SAVE_AS = False
AUTHORS_SAVE_AS = False
CATEGORY_SAVE_AS = False
CATEGORIES_SAVE_AS = False
TAGS_SAVE_AS = False

# Disables Atom feed generation
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

FEED_DOMAIN = SITEURL
FEED_RSS = 'feed.rss'

DEFAULT_PAGINATION = False

MD_EXTENSIONS = ['codehilite(css_class = highlight, linenums = True)', 'extra']

PLUGIN_PATH = 'plugins'
PLUGINS = ['latex', 'neighbors']

# Only enable LaTeX with the "Latex:" metadata property
LATEX = 'article'

DELETE_OUTPUT_DIRECTORY = True
OUTPUT_PATH = 'develop/'
PATH = 'content/'

# Creates icons for social links using the format ('link', 'hover text', 'icon')
SOCIAL = (('m&#97;&#105;l&#116;o&#58;me&#64;&#107;e&#118;inya%7&#48;&#46;ca', 'Email', 'envelope-o'),
          ('http://twitter.com/iKevinY', 'Twitter', 'twitter'),
          ('http://plus.google.com/+KevinYapCA', 'Google+', 'google-plus'),
          ('http://github.com/iKevinY', 'GitHub', 'github'),
          ('http://soundcloud.com/iKevinY', 'SoundCloud', 'music'),
          ('http://kevinyap.ca/feed.rss', 'RSS Feed', 'rss')
          )

# MD5 hash of email address for Gravatar
GRAVATAR_HASH = '0d1d263a229548db35dffba8c55e19f7'
