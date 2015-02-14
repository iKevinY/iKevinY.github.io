# Extend pelicanconf.py and apply some additional settings
import os, sys
sys.path.append(os.curdir)
from pelicanconf import *

SITEURL = 'http://kevinyap.ca'
RELATIVE_URLS = False
OUTPUT_PATH = 'output/'

GOOGLE_ANALYTICS = 'UA-41937659-1'
