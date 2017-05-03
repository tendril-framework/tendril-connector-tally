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
Docstring for stock
"""

from lxml import etree
from tendril.inventory.acquire import InventoryReaderBase

from . import TallyXMLEngine
from . import TallyQueryParameters
from . import TallyNotAvailable
from . import TallyMasterElement
from . import yesorno


class TallyStockGroup(TallyMasterElement):
    elements = {
        'name': ('name', str, True),
        '_parent': ('parent', str, True),
        'narration': ('narration', str, True),
        'costingmethod': ('costingmethod', str, True),
        'valuationmethod': ('valuationmethod', str, True),
        '_baseunits': ('baseunits', str, True),
        '_additionalunits': ('additionalunits', str, True),
        'isbatchwiseon': ('isbatchwiseon', yesorno, True),
        'isperishableon': ('isperishableon', yesorno, True),
        'isaddable': ('isaddable', yesorno, True),
        'ignorephysicaldifference': ('ignorephysicaldifference', yesorno, True),
        'ignorenegativestock': ('ignorenegativestock', yesorno, True),
        'treatsalesasmanufactured': ('treatsalesasmanufactured', yesorno, True),
        'treatpurchasesasconsumed': ('treatpurchasesasconsumed', yesorno, True),
        'treatrejectsasscrap': ('treatrejectsasscrap', yesorno, True),
        'hasmfgdate': ('hasmfgdate', yesorno, True),
        'allowuseofexpireditems': ('allowuseofexpireditems', yesorno, True),
        'ignorebatches': ('ignorebatches', yesorno, True),
        'ignoregodowns': ('ignoregodowns', yesorno, True),
    }

    @property
    def parent(self):
        if self._parent and self._parent != self.name:
            return self._ctx.stockgroups[self._parent]

    @property
    def path(self):
        if self.parent:
            return ' / '.join([self.parent.path, self.name])
        else:
            return self.name

    @property
    def baseunits(self):
        if self._baseunits:
            return self._ctx.units[self._baseunits]

    @property
    def additionalunits(self):
        if self._additionalunits:
            return self._ctx.units[self._additionalunits]

    def __repr__(self):
        return "<TallyStockGroup {1}>".format(self.__class__, self.name)


class TallyStockCategory(TallyMasterElement):
    elements = {
        'name': ('name', str, True),
        '_parent': ('parent', str, True),
        'narration': ('narration', str, True),
    }

    @property
    def parent(self):
        if self._parent and self._parent != self.name:
            return self._ctx.stockcategories[self._parent]


class TallyStockItem(TallyMasterElement):
    elements = {
        'name': ('name', str, True),
        '_parent': ('parent', str, True),
        'narration': ('narration', str, True),
        '_category': ('category', str, False),
        'taxclassificationname': ('taxclassificationname', str, False),
        'ledgername': ('ledgername', str, False),
        '_costingmethod': ('costingmethod', str, True),
        '_valuationmethod': ('valuationmethod', str, True),
        '_baseunits': ('baseunits', str, True),
        '_additionalunits': ('additionalunits', str, True),
        'description': ('description', str, True),
        'natureofitem': ('natureofitem', str, True),
        'isbatchwiseon': ('isbatchwiseon', yesorno, True),  # TODO Inherit
        'isperishableon': ('isperishableon', yesorno, True),  # TODO Inherit
        'iscostcentreson': ('iscostcentreson', yesorno, False),
        'isentrytaxapplicable': ('isentrytaxapplicable', yesorno, False),
        'iscosttrackingon': ('iscosttrackingon', yesorno, False),
        'ignorephysicaldifference': ('ignorephysicaldifference', yesorno, True),  # TODO Inherit
        'ignorenegativestock': ('ignorenegativestock', yesorno, True),  # TODO Inherit
        'treatsalesasmanufactured': ('treatsalesasmanufactured', yesorno, True),  # TODO Inherit
        'treatpurchasesasconsumed': ('treatpurchasesasconsumed', yesorno, True),  # TODO Inherit
        'treatrejectsasscrap': ('treatrejectsasscrap', yesorno, True),  # TODO Inherit
        'hasmfgdate': ('hasmfgdate', yesorno, True),  # TODO Inherit
        'allowuseofexpireditems': ('allowuseofexpireditems', yesorno, True),  # TODO Inherit
        'ignorebatches': ('ignorebatches', yesorno, True),  # TODO Inherit
        'ignoregodowns': ('ignoregodowns', yesorno, True),  # TODO Inherit
        'calconmrp': ('calconmrp', yesorno, True),  # TODO Inherit
        'excludejrnlforvaluation': ('excludejrnlforvaluation', yesorno, True),  # TODO Inherit
        '_openingbalance': ('openingbalance', str, True),
        '_openingvalue': ('openingvalue', str, True),
        '_openingrate': ('openingrate', str, True),
        '_godownname': ('godownname', str, False),
        'batchname': ('batchname', str, False),
    }

    @property
    def parent(self):
        if self._parent and self._parent != self.name:
            return self._ctx.stockgroups[self._parent]

    @property
    def catgory(self):
        if self._parent and self._parent != self.name:
            return self._ctx.stockcategories[self._parent]

    @property
    def baseunits(self):
        if self._baseunits:
            return self._ctx.units[self._baseunits]

    @property
    def additionalunits(self):
        if self._additionalunits:
            return self._ctx.units[self._additionalunits]

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
    def godown(self):
        if self._godownname:
            return self._ctx.godowns[self._godownname]

    @property
    def path(self):
        if self.parent:
            return ' / '.join([self.parent.path, self.name])
        else:
            return self.name

    def __repr__(self):
        return "<TallyStockItem {1}>".format(self.__class__, self.name)


class TallyGodown(TallyMasterElement):
    elements = {
        'name': ('name', str, True),
        '_parent': ('parent', str, True),
        'narration': ('narration', str, True),
        'hasnospace': ('hasnospace', yesorno, False),
        'hasnostock': ('hasnostock', yesorno, False),
        'isexternal': ('isexternal', yesorno, False),
        'isinternal': ('isinternal', yesorno, False),
    }

    @property
    def parent(self):
        if self._parent and self._parent != self.name:
            return self._ctx.godowns[self._parent]

    def __repr__(self):
        return "<TallyGodown {1}>".format(self.__class__, self.name)


class TallyVoucherType(TallyMasterElement):
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
            return self._ctx.vouchertypes[self._parent]


class TallyUnit(TallyMasterElement):
    elements = {
        'name': ('name', str, True),
        'originalname': ('originalname', str, False),
        'decimalplaces': ('decimalplaces', int, True),
        'issimpleunit': ('issimpleunit', yesorno, True),
        'additionalunits': ('additionalunits', str, False),
        'conversion': ('conversion', float, False)
    }


class TallyStockMaster(object):
    def __init__(self):
        self._xion = None
        self._soup = None
        self._stockgroups = None
        self._stockitems = None
        self._stockcategories = None
        self._vouchertypes = None
        self._units = None
        self._godowns = None
        self._acquire_raw_master()

    @staticmethod
    def _master_request():
        r = etree.Element('EXPORTDATA')
        rd = etree.SubElement(r, 'REQUESTDESC')
        rn = etree.SubElement(rd, 'REPORTNAME')
        rn.text = 'List of Accounts'
        sv = etree.SubElement(rd, 'STATICVARIABLES')
        svef = etree.SubElement(sv, 'SVEXPORTFORMAT')
        svef.text = '$$SysName:XML'
        at = etree.SubElement(sv, 'ACCOUNTTYPE')
        at.text = 'All Inventory Masters'
        return etree.ElementTree(r)

    def _acquire_raw_master(self):
        self._xion = TallyXMLEngine()
        query = TallyQueryParameters("Export Data", self._master_request())
        self._soup = self._xion.execute(query)

    @property
    def soup(self):
        if not self._soup:
            self._acquire_raw_master()
        return self._soup

    @property
    def stockgroups(self):
        return self._stockgroups or self._get_stockgroups()

    @property
    def stockitems(self):
        return self._stockitems or self._get_stockitems()

    @property
    def stockcategories(self):
        return self._stockcategories or self._get_stockcategories()

    @property
    def godowns(self):
        return self._godowns or self._get_godowns()

    @property
    def vouchertypes(self):
        return self._vouchertypes or self._get_vouchertypes()

    @property
    def units(self):
        return self._units or self._get_units()

    # TODO Combine these and push it up the hierarchy

    def _get_stockgroups(self):
        self._stockgroups = {
            y.name: y
            for y in [TallyStockGroup(x, self)
                      for x in self.soup.findAll('stockgroup')]}
        return self._stockgroups

    def _get_stockitems(self):
        self._stockitems = {
            y.name: y
            for y in [TallyStockItem(x, self)
                      for x in self.soup.findAll('stockitem')]}
        return self._stockitems

    def _get_stockcategories(self):
        self._stockcategories = {
            y.name: y
            for y in [TallyStockCategory(x, self)
                      for x in self.soup.findAll('stockcategory')]}
        return self._stockcategories

    def _get_godowns(self):
        self._godowns = {y.name: y
                         for y in [TallyGodown(x, self)
                                   for x in self.soup.findAll('godown')]}
        return self._godowns

    def _get_vouchertypes(self):
        self._vouchertypes = \
            {y.name: y
             for y in [TallyVoucherType(x, self)
                       for x in self.soup.findAll('vouchertype')]}
        return self._vouchertypes

    def _get_units(self):
        self._units = {y.name: y
                       for y in [TallyUnit(x, self)
                                 for x in self.soup.findAll('unit')]}
        return self._units


class InventoryTallyReader(InventoryReaderBase):
    def __init__(self, tfpath):
        super(InventoryTallyReader, self).__init__(tfpath)

    def _row_gen(self):
        if not master_available:
            get_master()
        pass


def get_master(force=False):
    global _master
    global master_available
    if not force and master_available:
        return _master
    try:
        _master = TallyStockMaster()
        master_available = True
    except TallyNotAvailable:
        _master = None
        master_available = False
    return _master

master_available = False
_master = get_master()
