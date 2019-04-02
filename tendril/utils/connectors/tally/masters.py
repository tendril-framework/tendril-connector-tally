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

from . import TallyReport
from . import TallyNotAvailable
from .general import TallyUnit
from .stock import TallyStockItem
from .stock import TallyStockGroup
from .stock import TallyStockCategory
from .stock import TallyGodown
from .vouchers import TallyVoucherType


class TallyMasters(TallyReport):
    _cachename = 'TallyMasters'

    def _build_request_body(self):
        r = etree.Element('EXPORTDATA')
        rd = etree.SubElement(r, 'REQUESTDESC')
        rn = etree.SubElement(rd, 'REPORTNAME')
        rn.text = 'List of Accounts'
        sv = etree.SubElement(rd, 'STATICVARIABLES')
        self._set_request_staticvariables(sv)
        at = etree.SubElement(sv, 'ACCOUNTTYPE')
        at.text = 'All Masters'
        return etree.ElementTree(r)

    _content = {
        'stockitems': ('stockitem', TallyStockItem),
        'stockgroups': ('stockgroup', TallyStockGroup),
        'stockcategories': ('stockcatogory', TallyStockCategory),
        'godowns': ('godown', TallyGodown),
        'vouchertypes': ('vouchertype', TallyVoucherType),
        'units': ('unit', TallyUnit)
    }


def get_master(company_name, force=False):
    global _masters
    if not force and company_name in _masters.keys():
        return _masters[company_name]
    try:
        _masters[company_name] = TallyMasters(company_name)
    except TallyNotAvailable:
        _masters[company_name] = None
    return _masters[company_name]


_masters = {}
