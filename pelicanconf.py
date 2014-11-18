# Theme-specific settings
SITENAME = 'Kevin Yap'
DOMAIN = 'kevinyap.ca'
BIO_TEXT = 'Developer and musician from Vancouver, BC.'
FOOTER_TEXT = 'Powered by <a href="http://getpelican.com">Pelican</a> and <a href="http://pages.github.com">GitHub&nbsp;Pages</a>.'

SITE_AUTHOR = 'Kevin Yap'
TWITTER_USERNAME = '@iKevinY'
GOOGLE_PLUS_URL = 'https://plus.google.com/+KevinYapCA'
INDEX_DESCRIPTION = 'Website and blog of Kevin Yap, a developer and musician from Vancouver, BC.'

SIDEBAR_LINKS = [
    '<a href="/about/">About</a>',
    '<a href="/projects/">Projects</a>',
]

SOCIAL_ICONS = [
    ('m&#97;&#105;l&#116;o&#58;me&#64;&#107;e&#118;inya&#112;&#46;ca', 'Email', 'fa-envelope'),
    ('http://twitter.com/iKevinY', 'Twitter', 'fa-twitter'),
    ('http://plus.google.com/+KevinYapCA', 'Google+', 'fa-google-plus-square'),
    ('http://github.com/iKevinY', 'GitHub', 'fa-github'),
    ('http://soundcloud.com/iKevinY', 'SoundCloud', 'fa-soundcloud'),
]

# Pelican settings
RELATIVE_URLS = True
SITEURL = 'http://localhost'
TIMEZONE = 'America/Vancouver'
DEFAULT_DATE_FORMAT = '%B %d, %Y'
DEFAULT_PAGINATION = False

THEME = 'pneumatic'

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

templates = ['404.html']
TEMPLATE_PAGES = {page: page for page in templates}

STATIC_PATHS = ['images', 'uploads', 'extra']
IGNORE_FILES = ['.DS_Store']

extras = ['CNAME', 'favicon.ico', 'keybase.txt', 'robots.txt']
EXTRA_PATH_METADATA = {'extra/%s' % file: {'path': file} for file in extras}

PLUGIN_PATHS = ['plugins']
PLUGINS = ['assets', 'neighbors']
ASSET_SOURCE_PATHS = ['static']
ASSET_CONFIG = [
    ('cache', False),
    ('manifest', False),
    ('url_expire', False),
    ('versions', False),
]
