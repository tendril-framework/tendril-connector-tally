#!/usr/bin/env python
# encoding: utf-8

# Copyright (C) 2017 Chintalagiri Shashank
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
Tally Stock Masters and Positions
---------------------------------
"""

from lxml import etree
from warnings import warn

from .utils.converters import TXBoolean
from .utils.converters import TXString
from .utils.converters import TXDecimal
from .utils.converters import TXMultilineString

from . import TallyReport
from . import TallyRequestHeader
from . import TallyNotAvailable
from . import TallyElement

from . import ledgers


class TallyStockGroup(TallyElement):
    # NOTE All masters has more fields?
    attrs = {
        'name': ('name', TXString(required=True), True),
        'reservedname': ('reservedname', TXString(), False),
    }
    descendent_elements = {
        'extendedname': ('name.list', TXMultilineString(required=True), True),
    }
    elements = {
        '_parent': ('parent', TXString(), True),
        'narration': ('narration', TXString(), True),
        'costingmethod': ('costingmethod', TXString(), True),
        'valuationmethod': ('valuationmethod', TXString(), True),
        '_baseunits': ('baseunits', TXString(), True),
        '_additionalunits': ('additionalunits', TXString(), True),
        'isbatchwiseon': ('isbatchwiseon', TXBoolean(), True),
        'isperishableon': ('isperishableon', TXBoolean(), True),
        'isaddable': ('isaddable', TXBoolean(), True),
        'ignorephysicaldifference': ('ignorephysicaldifference', TXBoolean(), True),
        'ignorenegativestock': ('ignorenegativestock', TXBoolean(), True),
        'treatsalesasmanufactured': ('treatsalesasmanufactured', TXBoolean(), True),
        'treatpurchasesasconsumed': ('treatpurchasesasconsumed', TXBoolean(), True),
        'treatrejectsasscrap': ('treatrejectsasscrap', TXBoolean(), True),
        'hasmfgdate': ('hasmfgdate', TXBoolean(), True),
        'allowuseofexpireditems': ('allowuseofexpireditems', TXBoolean(), True),
        'ignorebatches': ('ignorebatches', TXBoolean(), True),
        'ignoregodowns': ('ignoregodowns', TXBoolean(), True),
    }

    @property
    def parent(self):
        if self._parent and self._parent != self.name:
            return self.company_masters.stockgroups[self._parent]

    @property
    def path(self):
        if self.parent and self.parent.path:
            return self.parent.path + [self.name]
        else:
            return [self.name]

    @property
    def baseunits(self):
        if self._baseunits:
            return self.company_masters.units[self._baseunits]

    @property
    def additionalunits(self):
        if self._additionalunits:
            return self.company_masters.units[self._additionalunits]

    def __repr__(self):
        return "<TallyStockGroup {0}>".format(self.name)


class TallyStockCategory(TallyElement):
    # NOTE All masters has more fields?
    descendent_elements = {
        'name': ('name', TXString(required=True), True),
    }
    elements = {
        '_parent': ('parent', TXString(), True),
        'narration': ('narration', TXString(), True),
    }

    @property
    def parent(self):
        if self._parent and self._parent != self.name:
            return self.company_masters.stockcategories[self._parent]

    def __repr__(self):
        return "<TallyStockCategory {0}>".format(self.name)


class TallyStockItem(TallyElement):
    # NOTE All masters has more fields?
    attrs = {
        'name': ('name', TXString(required=True), True),
        'reservedname': ('reservedname', TXString(), False),
    }
    descendent_elements = {
        'extendedname': ('name.list', TXMultilineString(required=True), True),
        '_godownname': ('godownname', TXString(), False),
    }
    elements = {
        '_parent': ('parent', TXString(), True),
        'narration': ('narration', TXString(), True),
        '_category': ('category', TXString(), False),
        'taxclassificationname': ('taxclassificationname', TXString(), False),
        'ledgername': ('ledgername', TXString(), False),
        '_costingmethod': ('costingmethod', TXString(), True),
        '_valuationmethod': ('valuationmethod', TXString(), True),
        '_baseunits': ('baseunits', TXString(), True),
        '_additionalunits': ('additionalunits', TXString(), True),
        'description': ('description', TXString(), True),
        'natureofitem': ('natureofitem', TXString(), False),
        'isbatchwiseon': ('isbatchwiseon', TXBoolean(), True),
        'isperishableon': ('isperishableon', TXBoolean(), True),
        'iscostcentreson': ('iscostcentreson', TXBoolean(), False),
        'isentrytaxapplicable': ('isentrytaxapplicable', TXBoolean(), False),
        'iscosttrackingon': ('iscosttrackingon', TXBoolean(), False),
        'ignorephysicaldifference': ('ignorephysicaldifference', TXBoolean(), True),
        'ignorenegativestock': ('ignorenegativestock', TXBoolean(), True),
        'treatsalesasmanufactured': ('treatsalesasmanufactured', TXBoolean(), True),
        'treatpurchasesasconsumed': ('treatpurchasesasconsumed', TXBoolean(), True),
        'treatrejectsasscrap': ('treatrejectsasscrap', TXBoolean(), True),
        'hasmfgdate': ('hasmfgdate', TXBoolean(), True),
        'allowuseofexpireditems': ('allowuseofexpireditems', TXBoolean(), True),
        'ignorebatches': ('ignorebatches', TXBoolean(), True),
        'ignoregodowns': ('ignoregodowns', TXBoolean(), True),
        'calconmrp': ('calconmrp', TXBoolean(), False),
        'excludejrnlforvaluation': ('excludejrnlforvaluation', TXBoolean(), True),
        '_openingbalance': ('openingbalance', TXString(), True),
        '_openingvalue': ('openingvalue', TXString(), True),
        '_openingrate': ('openingrate', TXString(), True),
        'batchname': ('batchname', TXString(), False),
    }

    @property
    def parent(self):
        if self._parent and self._parent != self.name:
            try:
                return self.company_masters.stockgroups[self._parent]
            except KeyError:
                print(self.name)
                print(self._parent)
                print(self.company_masters.stockgroups.keys())
                raise

    @property
    def catgory(self):
        if self._parent and self._parent != self.name:
            return self.company_masters.stockcategories[self._parent]

    @property
    def baseunits(self):
        if self._baseunits:
            return self.company_masters.units[self._baseunits]

    @property
    def additionalunits(self):
        if self._additionalunits:
            return self.company_masters.units[self._additionalunits]

    @property
    def costingmethod(self):
        if self._costingmethod:
            return self._costingmethod
        if self.parent:
            return self.parent.costingmethod

    @property
    def valuationmethod(self):
        if self._valuationmethod:
            return self._valuationmethod
        if self.parent:
            return self.parent.valuationmethod

    @property
    def openingbalance(self):
        raise NotImplementedError

    @property
    def openingrate(self):
        raise NotImplementedError

    @property
    def openingvalue(self):
        raise NotImplementedError

    @property
    def godowns(self):
        if self._godownname:
            if ':' in self._godownname:
                names = set(self._godownname.split(':'))
            else:
                names = [self._godownname]
            return [self.company_masters.godowns[x] for x in names]
        else:
            return []

    @property
    def path(self):
        if self.parent and self.parent.path:
            return self.parent.path + [self.name]
        else:
            return [self.name]

    def __repr__(self):
        return "<TallyStockItem {0}>".format(self.name)


class TallyGodown(TallyElement):
    # NOTE All masters has more fields?
    attrs = {
        'name': ('name', TXString(required=True), True),
        'reservedname': ('reservedname', TXString(), False),
    }
    descendent_elements = {
        'extendedname': ('name.list', TXMultilineString(required=True), True),
    }
    elements = {
        '_parent': ('parent', TXString(), True),
        'narration': ('narration', TXString(), True),
        'hasnospace': ('hasnospace', TXBoolean(), False),
        'hasnostock': ('hasnostock', TXBoolean(), False),
        'isexternal': ('isexternal', TXBoolean(), False),
        'isinternal': ('isinternal', TXBoolean(), False),
    }

    @property
    def parent(self):
        if self._parent and self._parent != self.name:
            return self.company_masters.godowns[self._parent]

    def __repr__(self):
        return "<TallyGodown {0}>".format(self.name)


class TallyStockBatchAllocation(TallyElement):
    pass


class TallyVoucherBatchAllocation(TallyElement):
    elements = {
        'mfdon': ('mfdon', TXString(), False),
        'godownname': ('godownname', TXString(), True),
        'batchname': ('batchname', TXString(), True),
        'destinationgodownname': ('destinationgodownname', TXString(), True),
        'indentno': ('indentno', TXString(), False),
        'orderno': ('orderno', TXString(), False),
        'trackingnumber': ('trackingnumber', TXString(), False),
        'addlamount': ('addlamount', TXString(), False),
        'amount': ('amount', TXString(), True),
        'actualqty': ('actualqty', TXString(), True),  #
        'billedqty': ('billedqty', TXString(), True),  #
        'expiryperiod': ('expiryperiod', TXString(), False),
        'indentduedate': ('indentduedate', TXString(), False),
        'orderduedate': ('orderduedate', TXString(), False),
    }

    @property
    def godown(self):
        return self.company_masters.godowns[self.godownname]

    @property
    def batch(self):
        raise NotImplementedError

    @property
    def destinationgodown(self):
        return self.company_masters.godowns[self.destinationgodownname]

    def __repr__(self):
        return "<TallyVoucherBatchAllocation {0} {1} {2}>" \
               "".format(self.amount, self.actualqty, self.godownname)


class TallyInventoryEntry(TallyElement):
    elements = {
        'isdeemedpositive': ('isdeemedpositive', TXBoolean(), True),
        'amount': ('amount', TXString(), True),
        'actualqty': ('actualqty', TXString(), True),  #
        'billedqty': ('billedqty', TXString(), True),  #
        'description': ('description', TXString(), False),
        'stockitemname': ('stockitemname', TXString(required=True), True),
        'excisetariff': ('excisetariff', TXString(), False),
        'exciseexemption': ('exciseexemption', TXString(), False),
        'tradercnsalesnumber': ('tradercnsalesnumber', TXString(), False),
        'basicpackagemarks': ('basicpackagemarks', TXString(), False),
        'basicnumpackages': ('basicnumpackages', TXString(), False),
        'sdtaxclassificationname': ('sdtaxclassificationname', TXString(), False),
        'addlamount': ('addlamount', TXString(), False),
        'isautonegate': ('isautonegate', TXBoolean(), True),
        'rate': ('rate', TXString(), True),  #
        'discount': ('discount', TXString(), True),  #
        'mrprate': ('mrprate', TXString(), False),
        'basicuserdescription': ('basicuserdescription.list', TXMultilineString(), False),
    }

    lists = {
        'accountingallocations': ('accountingallocations', ledgers.TallyAccountingAllocation, True),
        'batchallocations': ('batchallocations', TallyVoucherBatchAllocation, True)
    }

    @property
    def name(self):
        return 'Unnamed'

    @property
    def stockitem(self):
        return self.company_masters.stockitems[self.stockitemname]

    def __repr__(self):
        return "<TallyInventoryEntry {0}, {1}@{2}>".format(self.stockitemname, self.billedqty, self.rate)


class TallyStockItemPosition(TallyElement):
    attrs = {
        'name': ('name', TXString(required=True), True),
        'reservedname': ('reservedname', TXString(), False),
    }
    descendent_elements = {
        'extendedname': ('name.list', TXMultilineString(required=True), True),
    }
    elements = {
        '_parent': ('parent', TXString(), True),
        '_baseunits': ('baseunits', TXString(), True),
        'closingbalance': ('closingbalance', TXString(), True),
        'closingvalue': ('closingvalue', TXDecimal(), True),
        'closingrate': ('closingrate', TXString(), True),
    }

    @property
    def parent(self):
        try:
            return self.company_masters.stockgroups[self._parent]
        except KeyError:
            warn("Could not find Parent {0} for {1}"
                 "".format(self._parent, self.name))
            return self._parent

    @property
    def baseunits(self):
        if getattr(self, '_baseunits', None):
            try:
                return self.company_masters.units[self._baseunits]
            except KeyError:
                return None

    def __repr__(self):
        return "<TallyStockItemPosition {0}, {1}>".format(self.name, self.closingbalance)


class TallyStockPosition(TallyReport):
    _cachename = 'TallyStockPosition'
    _header = TallyRequestHeader(1, 'Export', 'Collection',
                                 'All items under Groups')

    def _build_request_body(self):
        r = etree.Element('DESC')
        sv = etree.SubElement(r, 'STATICVARIABLES')
        self._set_request_staticvariables(sv)
        self._set_request_date(sv)
        tdl = etree.SubElement(r, 'TDL')
        tdlmessage = etree.SubElement(tdl, 'TDLMESSAGE')
        collection = etree.SubElement(tdlmessage, 'COLLECTION', ISMODIFY='No',
                                      NAME="All items under Groups")
        colltype = etree.SubElement(collection, 'TYPE')
        colltype.text = 'stock item'
        fetchlist = ['Name', 'Parent', 'BaseUnits',
                     'ClosingBalance', 'ClosingRate', 'ClosingValue']
        self._build_fetchlist(collection, fetchlist)
        return etree.ElementTree(r)

    _container = 'collection'
    _content = {
        'stockitems': ('stockitem', TallyStockItemPosition)
    }


def get_position(company_name, dt=None, end_dt=None, force=False):
    global _positions
    if not force and company_name in _positions.keys() and not dt:
        return _positions[company_name]
    try:
        _positions[company_name] = TallyStockPosition(company_name, dt=dt, end_dt=end_dt)
    except TallyNotAvailable:
        _positions[company_name] = None
    return _positions[company_name]


_positions = {}
