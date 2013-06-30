#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# import os
# import sys
# sys.path.append(os.curdir)
# from pelicanconf import *

AUTHOR = 'Kevin Yap'
SITENAME = 'Kevin Yap'
SITEURL = 'http://www.kevinyap.ca'

# Custom text for index page meta description, biography, and footer
INDEX_DESCRIPTION = 'Developer and musician from Vancouver, BC.'
BIO_TEXT = 'Developer and musician from Vancouver, BC.'
FOOTER_TEXT = 'Generated with <a href="http://getpelican.com">Pelican</a>. Theme designed by <a href="http://www.gregreda.com/">Greg Reda</a>. Hosted with <a href="https://www.nearlyfreespeech.net/">NearlyFreeSpeech</a>.'

RELATIVE_URLS = False

THEME = 'simply'
TYPOGRIFY = True

TIMEZONE = 'America/Vancouver'
DEFAULT_DATE_FORMAT = '%B %d, %Y'

ARTICLE_URL = 'posts/{date:%Y}/{date:%m}/{slug}/'
ARTICLE_SAVE_AS = 'posts/{date:%Y}/{date:%m}/{slug}/index.html'

PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'

YEAR_ARCHIVE_SAVE_AS = 'posts/{date:%Y}/index.html'
MONTH_ARCHIVE_SAVE_AS = 'posts/{date:%Y}/{date:%m}/index.html'

CATEGORY_URL = 'category/{slug}/'
CATEGORY_SAVE_AS = 'category/{slug}/index.html'

ARCHIVES_SAVE_AS = False
AUTHOR_SAVE_AS = False
TAGS_SAVE_AS= False

# Disables Atom feed generation
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# FEED_DOMAIN = SITEURL
# FEED_RSS = 'feed.xml'

# MD_EXTENSIONS = [ 'codehilite' ]

DELETE_OUTPUT_DIRECTORY = False
PATH = "content/"

# Creates icons for social links using the format ('link', 'hover text', 'icon')
SOCIAL = (  ('m&#97;&#105;l&#116;o&#58;me&#64;&#107;e&#118;inya%7&#48;&#46;ca', 'Email', 'icon-envelope'),
          	('http://twitter.com/iKevinY', 'Twitter', 'icon-twitter'),
						('http://plus.google.com/110479238274720428388', 'Google+', 'icon-google-plus'),
						('http://github.com/iKevinY', 'GitHub', 'icon-github'),
						('http://soundcloud.com/iKevinY', 'SoundCloud', 'icon-music'),
         )

DISQUS_SITENAME = "kevinyap"
TWITTER_USERNAME = "iKevinY"
GOOGLE_ANALYTICS = "UA-41937659-1"

DEFAULT_PAGINATION = 10

OUTPUT_PATH = ''