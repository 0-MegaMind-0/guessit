#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# GuessIt - A library for guessing information from filenames
# Copyright (c) 2013 Nicolas Wack <wackou@gmail.com>
# Copyright (c) 2013 Rémi Alvergnat <toilal.dev@gmail.com>
# Copyright (c) 2011 Ricard Marxer <ricardmp@gmail.com>
#
# GuessIt is free software; you can redistribute it and/or modify it under
# the terms of the Lesser GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# GuessIt is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# Lesser GNU General Public License for more details.
#
# You should have received a copy of the Lesser GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from __future__ import absolute_import, division, print_function, unicode_literals

from .containers import PropertiesContainer
from . import build_or_pattern
from pkg_resources import resource_stream


container = PropertiesContainer(enhance_patterns=False, canonical_from_pattern=False)

tlds = []

f = resource_stream('guessit', 'tlds-alpha-by-domain.txt')
f.readline()
next(f)
for tld in f:
    tld = tld.strip()
    if b'--' in tld:
        continue
    tlds.append(tld.decode("utf-8"))
f.close()

tlds_pattern = build_or_pattern(tlds)  # All registered domain extension
safe_tlds_pattern = build_or_pattern(['com', 'org', 'net'])  # For sure a website extension
safe_subdomains_pattern = build_or_pattern(['www'])  # For sure a website subdomain
safe_prefix_tlds_pattern = build_or_pattern(['co', 'com', 'org', 'net'])  # Those words before a tlds are sure

container.register_property('website', None, '(?:' + safe_subdomains_pattern + '\.)+' + r'(?:[a-z-]+\.)+' + r'(?:' + tlds_pattern + r')+')

container.register_property('website', None, '(?:' + safe_subdomains_pattern + '\.)*' + r'[a-z-]+\.' + r'(?:' + safe_tlds_pattern + r')+')

container.register_property('website', None, '(?:' + safe_subdomains_pattern + '\.)*' + r'[a-z-]+\.' + r'(?:' + safe_prefix_tlds_pattern + r'\.)+' + r'(?:' + tlds_pattern + r')+')
