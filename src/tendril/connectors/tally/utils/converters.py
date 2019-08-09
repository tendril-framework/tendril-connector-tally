#!/usr/bin/env python
# encoding: utf-8

# Copyright (C) 2019 Chintalagiri Shashank
#
# This file is part of tendril-connector-tally.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Bidirectional Converters for Tally XML Data Types
-------------------------------------------------
"""

import arrow
from decimal import Decimal


class TallyPropertyConverter(object):
    def __init__(self, required=False):
        self.required = required

    def _from_tallyxml(self, soup):
        raise NotImplementedError

    def _to_tallyxml(self, value):
        raise NotImplementedError

    def from_tallyxml(self, soup):
        if not soup.strip():
            if not self.required:
                return None
            else:
                raise ValueError
        return self._from_tallyxml(soup.strip())

    def to_tallyxml(self, value):
        if value is None:
            if not self.required:
                return ''
            else:
                raise ValueError
        return self._to_tallyxml(value)


class TXString(TallyPropertyConverter):
    def _from_tallyxml(self, soup):
        return soup

    def _to_tallyxml(self, value):
        return value


class TXMultilineString(TallyPropertyConverter):
    def _from_tallyxml(self, soup):
        return str(soup)

    def _to_tallyxml(self, value):
        raise NotImplementedError


class TXInteger(TallyPropertyConverter):
    def _from_tallyxml(self, soup):
        return int(soup)

    def _to_tallyxml(self, value):
        return str(value)


class TXDecimal(TallyPropertyConverter):
    def _from_tallyxml(self, soup):
        return Decimal(soup)

    def _to_tallyxml(self, value):
        return str(value)


class TXBoolean(TallyPropertyConverter):
    def _from_tallyxml(self, soup):
        if soup == 'Yes':
            return True
        elif soup == 'No':
            return False
        raise ValueError

    def _to_tallyxml(self, value):
        if value is True:
            return 'Yes'
        else:
            return 'No'


class TXDate(TallyPropertyConverter):
    def _from_tallyxml(self, soup):
        return arrow.get(soup, 'YYYYMMDD')

    def _to_tallyxml(self, value):
        if isinstance(value, arrow.Arrow):
            value = value.date()
        return "{0:04d}{1:02d}{2:02d}".format(value.year, value.month, value.day)


class TXDateTime(TallyPropertyConverter):
    def _from_tallyxml(self, soup):
        return arrow.get(' '.join([x.strip() for x in soup.split('at')]),
                         'D-MMM-YYYY HH:mm')

    def _to_tallyxml(self, value):
        return ' at '.join(value.format('D-MMM-YYYY HH:mm').split())
