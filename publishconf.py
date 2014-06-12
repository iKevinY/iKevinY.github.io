#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys, os
sys.path.append(os.getcwd())
from pelicanconf import *

"""Contains settings that are only applied when publishing the site."""

SITEURL = 'http://kevinyap.ca'
RELATIVE_URLS = False
OUTPUT_PATH = 'output/'
DISQUS_SITENAME = 'kevinyap'
GOOGLE_ANALYTICS = 'UA-41937659-1'
DOMAIN = 'kevinyap.ca'
