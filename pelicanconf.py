from __future__ import unicode_literals

AUTHOR = 'ddaa'
SITENAME = "ddaa's blog"
ALT_NAME = "#! " + SITENAME
SITESUBTITLE = "Write-ups for CTF."
EMAIL = "0xddaa@gmail.com"
SITEURL = 'http://ddaa.tw'
#META_IMAGE = SITEURL + "/static/img/og_logo.jpg"
#META_IMAGE_TYPE = "image/jpeg"

PATH = 'content'

TIMEZONE = 'Asia/Taipei'

DEFAULT_LANG = 'en'
THEME = "themes/mg"


# Social widget
SOCIAL = (('facebook-square', 'http://www.facebook.com/xddaa'),
        ('github', 'https://github.com/0xddaa'),
        ('twitter', 'https://twitter.com/0xddaa'),
        ('envelope', 'mailto:0xddaa@gmail.com'),)

SHARE = True

FOOTER = ("&copy; 2015 <a href=\"mailto:0xddaa@gmail.com\">ddaa</a>. All rights reserved.<br>")

DEFAULT_PAGINATION = 10

TAG_SAVE_AS = ''
AUTHOR_SAVE_AS = ''
DIRECT_TEMPLATES = ('index', 'categories', 'archives', 'search', 'tipue_search')
TIPUE_SEARCH_SAVE_AS = 'tipue_search.json'
STATIC_PATHS = ['images']

RELATIVE_URLS = False

TWITTER_USERNAME = '0xddaa'
DISQUS_SITENAME = "ddaactf"

SUMMARY_MAX_LENGTH = 0
DEFAULT_DATE = 'fs'
