#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# Production settings, used by `task build:prod` and the GitHub Pages
# workflow.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

# Pages link to each other with relative URLs, so one build works both
# at https://michel.albert.lu and under https://exhuma.github.io/blog.
# Feeds still need absolute URLs and take them from SITEURL, which
# PELICAN_SITEURL overrides. An empty value counts as unset.
SITEURL = os.environ.get('PELICAN_SITEURL') or 'https://michel.albert.lu'
RELATIVE_URLS = True

FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'

DELETE_OUTPUT_DIRECTORY = True

# Following items are often useful when publishing

GOOGLE_ANALYTICS = "UA-54507261-1"
