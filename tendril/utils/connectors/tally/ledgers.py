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
Docstring for stock
"""


from lxml import etree

from .utils import parse_date
from .utils import yesorno

from . import TallyReport
from . import TallyRequestHeader
from . import TallyNotAvailable
from . import TallyElement


class TallyLedger(TallyElement):
    attrs = {
        'name': ('name', str, True),
        'reservedname': ('reservedname', str, False),
    }

    elements = {
        'lastvoucherdate': ('lastvoucherdate', parse_date, False),
        'parent': ('parent', str, False),
        'tax': ('tax', str, False),
        'servicecategory': ('servicecategory', str, False),
        'ledgerfbtcategory': ('ledgerfbtcategory', str, False),
        'isfbtapplicable': ('isfbtapplicable', yesorno, False),
        'closingbalance': ('closingbalance', str, False),
        'onaccountvalue': ('onaccountvalue', str, False),
        'tbalopening': ('tbalopening', str, False),
        'isfbtdutiesledger': ('isfbtdutiesledger', yesorno, False),
        'closingonacctvalue':  ('closingonacctvalue', str, False),
        'closingdronacctvalue': ('closingdronacctvalue', yesorno, False),
        'ledopeningbalance': ('ledopeningbalance', str, False),
    }

    def __repr__(self):
        return "<TallyLedgerStub {0}>".format(self.name)


class TallyLedgersList(TallyReport):
    _cachename = 'TallyLedgersList'
    _header = TallyRequestHeader(1, 'Export', 'Collection', 'Ledger')

    def _build_request_body(self):
        r = etree.Element('DESC')
        sv = etree.SubElement(r, 'STATICVARIABLES')
        self._set_request_staticvariables(sv)
        self._set_request_date(sv)
        return etree.ElementTree(r)

    _container = 'collection'
    _content = {
        'ledgers': ('ledger', TallyLedger)
    }


def get_list(company_name, force=False):
    global _lists
    if not force and company_name in _lists.keys():
        return _lists[company_name]
    try:
        _lists[company_name] = TallyLedgersList(company_name)
    except TallyNotAvailable:
        _lists[company_name] = None
    return _lists[company_name]


_lists = {}
