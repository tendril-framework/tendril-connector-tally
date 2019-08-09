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
Tally Ledgers and Ledger Masters
--------------------------------
"""

from lxml import etree

from .utils.converters import TXBoolean
from .utils.converters import TXDate
from .utils.converters import TXString
from .utils.converters import TXDecimal
from .utils.converters import TXMultilineString

from . import TallyReport
from . import TallyRequestHeader
from . import TallyNotAvailable
from . import TallyElement


class TallyLedgerMaster(TallyElement):
    attrs = {
        'name': ('name', TXString(required=True), True),
        'reservedname': ('reservedname', TXString(), False),
    }

    def __repr__(self):
        return "<TallyLedgerMaster {0}>".format(self.name)


class TallyLedgerEntry(TallyElement):
    elements = {
        'narration': ('narration', TXString(), True),
        'taxclassificationname': ('taxclassificationname', TXString(), False),
        'roundtype': ('roundtype', TXString(), False),
        'ledgername': ('ledgername', TXString(required=True), False),
        'methodtype': ('methodtype', TXString(), False),
        'classrate': ('classrate', TXString(), False),
        'tdspartyname': ('tdspartyname', TXString(), False),
        'voucherfbtcategory': ('voucherfbtcategory', TXString(), False),
        'typeoftaxpayment': ('typeoftaxpayment', TXString(), False),
        'gstclass': ('gstclass', TXString(), False),
        'stnotificationno': ('stnotificationno', TXString(), False),
        'isdeemedpositive': ('isdeemedpositive', TXBoolean(), True),
        'ledgerfromitem': ('ledgerfromitem', TXBoolean(), True),
        'removezeroentries': ('removezeroentries', TXBoolean(), True),
        'ispartyledger': ('ispartyledger', TXBoolean(), True),
        'stcradjpercent': ('stcradjpercent', TXDecimal(), True),
        'roundlimit': ('roundlimit', TXDecimal(), True),
        'rateofaddlvat': ('rateofaddlvat', TXDecimal(), True),
        'rateofcessonvat': ('rateofcessonvat', TXDecimal(), True),
        'previnvtotalnum': ('previnvtotalnum', TXDecimal(), True),
        'amount': ('amount', TXString(required=True), True),
        'fbtexemptamount': ('fbtexemptamount', TXString(), False),
        'vatassessablevalue': ('vatassessablevalue', TXString(), False),
        'prevamount': ('prevamount', TXString(), False),
        'previnvtotalamt': ('previnvtotalamt', TXString(), False),
    }

    @property
    def ledger(self):
        return get_list(self.company_name).ledgers[self.ledgername]

    def __repr__(self):
        return "<TallyLedgerEntry {1} {0}>".format(self.ledgername, self.amount)


class TallyAccountingAllocation(TallyLedgerEntry):
    def __repr__(self):
        return "<TallyAccountingAllocation {1} {0}>".format(self.ledgername, self.amount)


class TallyLedger(TallyElement):
    attrs = {
        'name': ('name', TXString(required=True), True),
        'reservedname': ('reservedname', TXString(), False),
    }
    descendent_elements = {
        'extendedname': ('name.list', TXMultilineString(required=True), True),
    }
    elements = {
        'lastvoucherdate': ('lastvoucherdate', TXDate(), False),
        'parent': ('parent', TXString(), False),
        'tax': ('tax', TXString(), False),
        'servicecategory': ('servicecategory', TXString(), False),
        'ledgerfbtcategory': ('ledgerfbtcategory', TXString(), False),
        'isfbtapplicable': ('isfbtapplicable', TXBoolean(), False),
        'closingbalance': ('closingbalance', TXString(), False),
        'onaccountvalue': ('onaccountvalue', TXString(), False),
        'tbalopening': ('tbalopening', TXString(), True),
        'isfbtdutiesledger': ('isfbtdutiesledger', TXBoolean(), False),
        'closingonacctvalue':  ('closingonacctvalue', TXString(), False),
        'closingdronacctvalue': ('closingdronacctvalue', TXBoolean(), False),
        'ledopeningbalance': ('ledopeningbalance', TXString(), False),
    }

    @property
    def master(self):
        return self.company_masters.ledgers[self.name]

    def __repr__(self):
        return "<TallyLedger {0}>".format(self.name)


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
