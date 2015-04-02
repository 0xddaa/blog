from __future__ import unicode_literals
import locale

AUTHOR = 'ddaa'
SITENAME = "ddaa's blog"
ALT_NAME = ""
SITESUBTITLE = "Write-ups for CTF."
EMAIL = "0xddaa@gmail.com"
SITEURL = "http://ddaa.tw"
FAVICON = "images/favicon.ico"

PATH = 'content'
THEME = "theme/pelican-mg"

LOCALE = ('en_US.UTF-8')
TIMEZONE = 'Asia/Taipei'
DEFAULT_LANG = 'zh-tw'
DEFAULT_DATE_FORMAT = ("%A %d %B %Y")
DATE_FORMATS = {
    'en': '%a, %d %B %Y',
    'zh-tw': '%a, %d %B %Y',
}
DEFAULT_DATE = 'fs'

# Social widget
SOCIAL = (('facebook-square', 'http://www.facebook.com/xddaa'),
        ('github', 'https://github.com/0xddaa'),
        ('twitter', 'https://twitter.com/0xddaa'),
        ('envelope-o', 'mailto:0xddaa@gmail.com'),)

SHARE = True
DISQUS_SITENAME = "ddaactf"

FOOTER = ("&copy; 2015 <a href=\"mailto:0xddaa@gmail.com\">ddaa</a>. All rights reserved.<br>")

DEFAULT_PAGINATION = 10

AUTHOR_SAVE_AS = ''
#DIRECT_TEMPLATES = ('index', 'categories', 'archives', 'search', 'tipue_search', 'tags')
DIRECT_TEMPLATES = ('index', 'categories', 'archives')
STATIC_PATHS = ["images", "exp"]


PLUGIN_PATHS = ["/usr/local/lib/python2.7/site-packages/pelican/pelican-plugins"]
PLUTIN_ = ["tipue_search"]
TIPUE_SEARCH_SAVE_AS = 'tipue_search.json'

# test / publish
DELETE_OUTPUT_DIRECTORY = True
OUTPUT_PATH = 'output/'
RELATIVE_URLS = False
