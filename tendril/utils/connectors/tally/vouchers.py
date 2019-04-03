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

from lxml import etree
from six import iteritems

from .utils import yesorno

from . import TallyElement
from . import TallyReport
from . import TallyRequestHeader


class TallyVoucherType(TallyElement):
    elements = {
        'name': ('name', str, True),
        '_parent': ('parent', str, True),
        'mailingname': ('mailingname', str, True),
        'numberingmethod': ('numberingmethod', str, True),
        'isdeemedpositive': ('isdeemedpositive', yesorno, False),
        'affectsstock': ('affectsstock', yesorno, False),
        'preventduplicates': ('preventduplicates', yesorno, False),
        'prefillzero': ('prefillzero', yesorno, False),
        'printaftersave': ('printaftersave', yesorno, False),
        'formalreceipt': ('formalreceipt', yesorno, False),
        'isoptional': ('isoptional', yesorno, False),
        'asmfgjrnl': ('asmfgjrnl', yesorno, False),
        'effectivedate': ('effectivedate', yesorno, False),
        'commonnarration': ('commonnarration', yesorno, False),
        'multinarration': ('multinarration', yesorno, False),
        'istaxinvoice': ('istaxinvoice', yesorno, False),
        'useforposinvoice': ('useforposinvoice', yesorno, False),
        'useforexcisetraderinvoice': ('useforexcisetraderinvoice', yesorno, False),  # noqa
        'useforexcise': ('useforexcise', yesorno, False),
        'useforjobwork': ('useforjobwork', yesorno, False),
        'isforjobworkin': ('isforjobworkin', yesorno, False),
        'allowconsumption': ('allowconsumption', yesorno, False),
    }

    @property
    def parent(self):
        if self._parent and self._parent != self.name:
            return self.company_masters.vouchertypes[self._parent]

    def __repr__(self):
        return "<TallyVoucherType {0}>".format(self.name)


class TallyVoucher(TallyElement):
    attrs = {
        '_vchtype': ('vchtype', str, True),
        'name': ('remoteid', str, True),
    }

    elements = {

    }

    lists = {

    }

    @property
    def vchtype(self):
        return self.company_masters.vouchertypes[self._vchtype]

    def __repr__(self):
        return "<TallyVoucher {0} {1}>".format(self._vchtype, self.name)


class TallyVouchersList(TallyReport):
    _cachename = None
    _header = TallyRequestHeader(1, 'Export', 'Data', 'Voucher Register')

    def __init__(self, company_name, dt=None, end_dt=None, filters=None):
        super(TallyVouchersList, self).__init__(company_name)
        self._dt = dt
        self._end_dt = end_dt
        self._filters = filters or {}

    def _build_request_body(self):
        r = etree.Element('DESC')
        sv = etree.SubElement(r, 'STATICVARIABLES')
        self._set_request_staticvariables(sv)
        self._set_request_date(sv, dt=self._dt, end_dt=self._end_dt)
        for tag, value in iteritems(self._filters):
            svft = etree.SubElement(sv, tag)
            svft.text = value
        return etree.ElementTree(r)

    _container = 'requestdata'
    _content = {
        'vouchers': ('voucher', TallyVoucher)
    }


def get_list(*args, **kwargs):
    return TallyVouchersList(*args, **kwargs)


def get_list_sales(*args, **kwargs):
    filters = kwargs.pop('filters', {})
    filters['VoucherTypeName'] = 'Sales'
    return TallyVouchersList(*args, filters=filters, **kwargs)
