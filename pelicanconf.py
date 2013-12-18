#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
from pilkit.processors import *

AUTHOR = u'Nick Bennett'
SITENAME = u'ohrho'
SITEURL = 'http://ohrho.com'
GITHUB_URL = 'https://github.com/tothebeat'

TIMEZONE = 'America/Chicago'

DEFAULT_LANG = u'en'

PATH = 'content'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS =  (('Hacker News', 'http://news.ycombinator.com/'),
        ('lobste.rs', 'http://lobste.rs/'),
        ('Joel Spolsky', 'http://joelonsoftware.com'),
        ('Derek Sivers', 'http://sivers.org/'),
        ('Pelican Themes', 'http://pelicanthemes.com/'),
        )

# Social widget
SOCIAL = (('my linkedin', 'https://linkedin.com/in/nicholasrrbennett/'),
          ('my twitter', 'https://twitter.com/nicksdomainhack'),
          ('my github', 'https://github.com/tothebeat'),)

DEFAULT_PAGINATION = 8

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
RESIZE = [
        ('posts', '', [ResizeToFit(600, 1000)])
      ]
