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

from six import iteritems
from lxml import etree
from warnings import warn
from decimal import Decimal
from decimal import DecimalException
from tendril.inventory.acquire import InventoryReaderBase

from . import TallyReport
from . import TallyRequestHeader
from . import TallyNotAvailable
from . import TallyElement
from . import yesorno

try:
    from tendril.utils.types.lengths import Length
    from tendril.utils.types.mass import Mass
    from tendril.utils.types import ParseException
except ImportError:
    ParseException = DecimalException
    Length = Decimal
    Mass = Decimal


class TallyStockGroup(TallyElement):
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
        if self.parent and self.parent.path:
            return self.parent.path + [self.name]
        else:
            return [self.name]

    @property
    def baseunits(self):
        if self._baseunits:
            return self._ctx.units[self._baseunits]

    @property
    def additionalunits(self):
        if self._additionalunits:
            return self._ctx.units[self._additionalunits]

    def __repr__(self):
        return "<TallyStockGroup {0}>".format(self.name)


class TallyStockCategory(TallyElement):
    elements = {
        'name': ('name', str, True),
        '_parent': ('parent', str, True),
        'narration': ('narration', str, True),
    }

    @property
    def parent(self):
        if self._parent and self._parent != self.name:
            return self._ctx.stockcategories[self._parent]

    def __repr__(self):
        return "<TallyStockCategory {0}>".format(self.name)


class TallyStockItem(TallyElement):
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
            try:
                return self._ctx.stockgroups[self._parent]
            except KeyError:
                print self.name
                print self._parent
                print self._ctx.stockgroups.keys()
                raise

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
    def godowns(self):
        if self._godownname:
            if ':' in self._godownname:
                names = set(self._godownname.split(':'))
            else:
                names = [self._godownname]
            return [self._ctx.godowns[x] for x in names]
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
        return "<TallyGodown {0}>".format(self.name)


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
            return self._ctx.vouchertypes[self._parent]


class TallyUnit(TallyElement):
    elements = {
        'name': ('name', str, True),
        'originalname': ('originalname', str, False),
        'decimalplaces': ('decimalplaces', int, True),
        'issimpleunit': ('issimpleunit', yesorno, True),
        'additionalunits': ('additionalunits', str, False),
        'conversion': ('conversion', float, False)
    }

    def __repr__(self):
        return "<TallyUnit {0}>".format(self.name)


class TallyStockMaster(TallyReport):
    _cachename = 'TallyStockMaster'

    def _build_request_body(self):
        r = etree.Element('EXPORTDATA')
        rd = etree.SubElement(r, 'REQUESTDESC')
        rn = etree.SubElement(rd, 'REPORTNAME')
        rn.text = 'List of Accounts'
        sv = etree.SubElement(rd, 'STATICVARIABLES')
        if self.company_name:
            svcc = etree.SubElement(sv, 'SVCURRENTCOMPANY', TYPE="String")
            svcc.text = self.company_name
        svef = etree.SubElement(sv, 'SVEXPORTFORMAT')
        svef.text = '$$SysName:XML'
        at = etree.SubElement(sv, 'ACCOUNTTYPE')
        at.text = 'All Inventory Masters'
        return etree.ElementTree(r)

    _content = {
        'stockitems': ('stockitem', TallyStockItem),
        'stockgroups': ('stockgroup', TallyStockGroup),
        'stockcategories': ('stockcatogory', TallyStockCategory),
        'godowns': ('godown', TallyGodown),
        'vouchertypes': ('vouchertype', TallyVoucherType),
        'units': ('unit', TallyUnit)
    }


class TallyStockItemPosition(TallyElement):
    elements = {
        'name': ('name', str, True),
        '_parent': ('parent', str, True),
        '_baseunits': ('baseunits', str, True),
        'closingbalance': ('closingbalance', str, True),
        'closingvalue': ('closingvalue', str, True),
        'closingrate': ('closingrate', str, True),
    }

    @property
    def parent(self):
        try:
            return get_master(self._ctx.company_name).stockgroups[self._parent]
        except KeyError:
            warn("Could not find Parent {0} for {1}"
                 "".format(self._parent, self.name))
            return self._parent

    @property
    def baseunits(self):
        return get_master(self._ctx.company_name).units[self._baseunits]


class TallyStockPosition(TallyReport):
    _cachename = 'TallyStockPosition'
    _header = TallyRequestHeader(1, 'Export', 'Collection',
                                 'All items under Groups')

    def _build_request_body(self):
        r = etree.Element('DESC')
        sv = etree.SubElement(r, 'STATICVARIABLES')
        svef = etree.SubElement(sv, 'SVEXPORTFORMAT')
        svef.text = '$$SysName:XML'
        if self.company_name:
            svcc = etree.SubElement(sv, 'SVCURRENTCOMPANY', TYPE="String")
            svcc.text = self.company_name
        svec = etree.SubElement(sv, 'ENCODINGTYPE')
        svec.text = 'UNICODE'
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
        'items': ('stockitem', TallyStockItemPosition)
    }


def _strip_unit(value, baseunit):
    return value.rstrip(baseunit.name)


def _rewrite_mass(value, baseunit):
    if isinstance(baseunit, TallyUnit):
        uname = baseunit.name
    else:
        uname = baseunit
    if uname.strip() == 'gm':
        value = value.replace(' gm', ' g')
    elif uname.strip() == 'Kg':
        value = value.replace(' Kg', ' kg')
    return value


class InventoryTallyReader(InventoryReaderBase):
    def __init__(self, sname=None, location=None, company_name=None,
                 godown_name=None, tfpath=''):
        self._location = location
        self._sname = sname
        self._company_name = company_name
        self._godown_name = godown_name
        super(InventoryTallyReader, self).__init__(tfpath)

    _typeclass = {
        'qty': (int, _strip_unit),
        'Pc':  (int, _strip_unit),
        'gm': (Mass, _rewrite_mass),
        'Kg': (Mass, _rewrite_mass),
        'ft': (Length, None),
        'cm': (Length, None),
        'Inch': (Length, None),
        'Feet': (Length, None),
        'meter': (Length, None),
        'mtr': (Length, None),
    }

    def _parse_quantity(self, value, item):
        masteritem = get_master(self._company_name).stockitems[item.name]
        additionalunits = masteritem.additionalunits
        baseunit = item.baseunits
        if not value:
            return 0
        if additionalunits:
            value = value.split('=')[0]
        value = value.strip()
        if baseunit.issimpleunit:
            unitname = baseunit.name.strip()
            if self._typeclass[unitname][1]:
                value = self._typeclass[unitname][1](value, baseunit)
            return self._typeclass[unitname][0](value)
        else:
            # Very ugly hacks
            uparts = baseunit.name.split(' of ')
            assert len(uparts) == 2
            uparts[1] = uparts[1].split()[1]
            if self._typeclass[uparts[0]][0] == self._typeclass[uparts[1]][0]:
                vparts = value.split(' ')
                plen = len(vparts) / 2
                assert plen * 2 == len(vparts)
                vpart0 = ' '.join(vparts[0:plen])
                if self._typeclass[uparts[0]][1]:
                    vpart0 = self._typeclass[uparts[0]][1](vpart0, uparts[0])
                rv = self._typeclass[uparts[0]][0](vpart0)
                vpart1 = ' '.join(vparts[plen:])
                if self._typeclass[uparts[1]][1]:
                    vpart1 = self._typeclass[uparts[1]][1](vpart1, uparts[1])
                rv += self._typeclass[uparts[1]][0](vpart1)
                return rv
        raise ValueError

    def _row_gen(self):
        position = get_position(self._company_name)
        for name, item in iteritems(position.items):
            imaster = get_master(self._company_name).stockitems[name]
            try:
                # TODO Needs a godown filter here if the XML tags ever surface
                qty = self._parse_quantity(item.closingbalance, item)
                meta = {'godowns': [x.name for x in imaster.godowns],
                        'path': ' / '.join(imaster.parent.path) if imaster.parent else None}  # noqa
                yield name, qty, meta
            except (ParseException, ValueError):
                pass

    def dump(self):
        position = get_position(self._company_name)
        idx = 0
        for name, item in iteritems(position.items):
            idx += 1
            try:
                qstring = '{3:4} {0:>10} {1:40} {2}'.format(
                    self._parse_quantity(item.closingbalance, item),
                    item.name, item.baseunits, idx
                )
                print(qstring)
            except (ParseException, ValueError, AssertionError) as e:
                master = get_master(self._company_name).stockitems[name]
                print(name, item.closingbalance, item.baseunits,
                      item.baseunits.issimpleunit, master.additionalunits, e)


def get_master(company_name, force=False):
    global _masters
    if not force and company_name in _masters.keys():
        return _masters[company_name]
    try:
        _masters[company_name] = TallyStockMaster(company_name)
    except TallyNotAvailable:
        _masters[company_name] = None
    return _masters[company_name]

_masters = {}


def get_position(company_name, force=False):
    global _positions
    if not force and company_name in _positions.keys():
        return _positions
    try:
        _positions[company_name] = TallyStockPosition(company_name)
    except TallyNotAvailable:
        _positions[company_name] = None
    return _positions[company_name]

_positions = {}
