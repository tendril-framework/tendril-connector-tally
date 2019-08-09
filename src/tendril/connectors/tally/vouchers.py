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
Tally Vouchers and Voucher Types
--------------------------------
"""


from lxml import etree
from six import iteritems

from .utils.converters import TXBoolean
from .utils.converters import TXString
from .utils.converters import TXInteger
from .utils.converters import TXDate
from .utils.converters import TXDateTime
from .utils.converters import TXMultilineString

from . import TallyElement
from . import TallyReport
from . import TallyRequestHeader

from . import ledgers
from . import stock


class TallyVoucherType(TallyElement):
    # NOTE Might not be the same in all masters as in the earlier inventory masters
    attrs = {
        'name': ('name', TXString(required=True), True),
        'reservedname': ('reservedname', TXString(), False),
    }
    descendent_elements = {
        'extendedname': ('name.list', TXMultilineString(required=True), True),
    }
    elements = {
        '_parent': ('parent', TXString(), True),
        'mailingname': ('mailingname', TXString(), True),
        'numberingmethod': ('numberingmethod', TXString(), True),
        'isdeemedpositive': ('isdeemedpositive', TXBoolean(), False),
        'affectsstock': ('affectsstock', TXBoolean(), False),
        'preventduplicates': ('preventduplicates', TXBoolean(), False),
        'prefillzero': ('prefillzero', TXBoolean(), False),
        'printaftersave': ('printaftersave', TXBoolean(), False),
        'formalreceipt': ('formalreceipt', TXBoolean(), False),
        'isoptional': ('isoptional', TXBoolean(), False),
        'asmfgjrnl': ('asmfgjrnl', TXBoolean(), False),
        'effectivedate': ('effectivedate', TXBoolean(), False),
        'commonnarration': ('commonnarration', TXBoolean(), False),
        'multinarration': ('multinarration', TXBoolean(), False),
        'istaxinvoice': ('istaxinvoice', TXBoolean(), False),
        'useforposinvoice': ('useforposinvoice', TXBoolean(), False),
        'useforexcisetraderinvoice': ('useforexcisetraderinvoice', TXBoolean(), False),  # noqa
        'useforexcise': ('useforexcise', TXBoolean(), False),
        'useforjobwork': ('useforjobwork', TXBoolean(), False),
        'isforjobworkin': ('isforjobworkin', TXBoolean(), False),
        'allowconsumption': ('allowconsumption', TXBoolean(), False),
    }

    @property
    def parent(self):
        if self._parent and self._parent != self.name:
            return self.company_masters.vouchertypes[self._parent]

    def __repr__(self):
        return "<TallyVoucherType {0}>".format(self.name)


class TallyInvoiceOrder(TallyElement):
    elements = {
        'basicorderdate': ('basicorderdate', TXDate(), True),
        'basicpurchaseorderno': ('basicpurchaseorderno', TXString(), True),
    }

    def __repr__(self):
        return "<TallyInvoiceOrder {0} {1}>" \
               "".format(self.basicpurchaseorderno,
                         self.basicorderdate.format('DD-MM-YY'))


class TallyVoucher(TallyElement):
    attrs = {
        '_vchtype': ('vchtype', TXString(), True),
        'name': ('remoteid', TXString(), True),
    }

    elements = {
        'activeto': ('activeto', TXString(), False),
        'alteredon': ('alteredon', TXString(), False),
        'date': ('date', TXDate(), True),
        'taxchallandate': ('taxchallandate', TXString(), False),
        'reconcilationdate': ('reconcilationdate', TXString(), False),
        'taxchequedate': ('taxchequedate', TXString(), False),
        'form16issuedate': ('form16issuedate', TXString(), False),
        'cstformissuedate': ('cstformissuedate', TXString(), False),
        'cstformrecvdate': ('cstformrecvdate', TXString(), False),
        'fbtfromdate': ('fbtfromdate', TXString(), False),
        'fbttodate': ('fbttodate', TXString(), False),
        'auditedon': ('auditedon', TXString(), False),
        'guid': ('guid', TXString(), True),
        'pricelevel': ('pricelevel', TXString(), False),
        'autocostlevel': ('autocostlevel', TXString(), False),
        'narration': ('narration', TXString(), True),
        'alteredby': ('alteredby', TXString(), False),
        'natureofsales': ('natureofsales', TXString(), False),
        'excisenotificationno': ('excisenotificationno', TXString(), False),
        'exciseunitname': ('exciseunitname', TXString(), False),
        'classname': ('classname', TXString(), False),
        'poscardledger': ('poscardledger', TXString(), False),
        'poscashledger': ('poscashledger', TXString(), False),
        'posgiftledger': ('posgiftledger', TXString(), False),
        'poschequeledger': ('poschequeledger', TXString(), False),
        'taxbankchallannumber': ('taxbankchallannumber', TXString(), False),
        'taxchallanbsrcode': ('taxchallanbsrcode', TXString(), False),
        'taxchequenumber': ('taxchequenumber', TXString(), False),
        'taxbankname': ('taxchequenumber', TXString(), False),
        'vouchertypename': ('vouchertypename', TXString(), False),
        'vouchernumber': ('vouchernumber', TXString(), False),
        'reference': ('reference', TXString(), False),
        'partyledgername': ('partyledgername', TXString(), True),
        'partyname': ('partyname', TXString(), True),
        'basicpartyname': ('basicpartyname', TXString(), False),
        'basicvoucherchequename': ('basicvoucherchequename', TXString(), False),
        'basicvouchercrosscomment': ('basicvouchercrosscomment', TXString(), False),
        'exchcurrencyname': ('exchcurrencyname', TXString(), False),
        'serialmaster': ('serialmaster', TXString(), False),
        'serialnumber': ('serialnumber', TXString(), False),
        'statadjustmenttype': ('statadjustmenttype', TXString(), False),
        'taxbankbranchname': ('taxbankbranchname', TXString(), False),
        'cstformissuetype': ('cstformissuetype', TXString(), False),
        'cstformissuenumber': ('cstformissuenumber', TXString(), False),
        'cstformrecvtype': ('cstformrecvtype', TXString(), False),
        'cstformrecvnnumber': ('cstformrecvnnumber', TXString(), False),
        'excisetreasurynumber': ('excisetreasurynumber', TXString(), False),
        'excisetreasuryname': ('excisetreasuryname', TXString(), False),
        'fbtpaymenttype': ('fbtpaymenttype', TXString(), False),
        'poscardnumber': ('poscardnumber', TXString(), False),
        'poschequenumber': ('poschequenumber', TXString(), False),
        'poschequebankname': ('poschequebankname', TXString(), False),
        'taxadjustment': ('taxadjustment', TXString(), False),
        'challantype': ('challantype', TXString(), False),
        'chequedepositorname': ('chequedepositorname', TXString(), False),
        'basicshippedby': ('basicshippedby', TXString(), False),
        'basicdestinationcountry': ('basicdestinationcountry', TXString(), False),
        'basicbuyername': ('basicbuyername', TXString(), False),
        'basicplaceofreceipt': ('basicplaceofreceipt', TXString(), False),
        'basicshipdocumentno': ('basicshipdocumentno', TXString(), False),
        'basicportofloading': ('basicportofloading', TXString(), False),
        'basicportofdischarge': ('basicportofdischarge', TXString(), False),
        'basicfinaldestination': ('basicfinaldestination', TXString(), False),
        'basicorderref': ('basicorderref', TXString(), False),
        'basicshipvesselno': ('basicshipvesselno', TXString(), False),
        'basicbuyerssalestaxno': ('basicbuyerssalestaxno', TXString(), False),
        'basicduedateofpymt': ('basicduedateofpymt', TXString(), False),
        'basicserialnuminpla': ('basicserialnuminpla', TXString(), False),
        'basicdatetimeofinvoice': ('basicdatetimeofinvoice', TXDateTime(), True),
        'basicdatetimeofremoval': ('basicdatetimeofinvoice', TXDateTime(), True),
        'vchgstclass': ('vchgstclass', TXString(), False),
        'costcentrename': ('costcentrename', TXString(), False),
        'enteredby': ('enteredby', TXString(), False),
        'requestorrule': ('requestorrule', TXString(), False),
        'destinationgodown': ('destinationgodown', TXString(), False),
        'diffactualqty': ('diffactualqty', TXBoolean(), True),
        'audited': ('audited', TXBoolean(), True),
        'forjobcosting': ('forjobcosting', TXBoolean(), True),
        'isoptional': ('isoptional', TXBoolean(), True),
        'effectivedate': ('effectivedate', TXDate(), True),
        'useforinterest': ('useforinterest', TXBoolean(), True),
        'useforgainloss': ('useforgainloss', TXBoolean(), True),
        'useforgodowntransfer': ('useforgodowntransfer', TXBoolean(), True),
        'useforcompound': ('useforcompound', TXBoolean(), True),
        'alterid': ('alterid', TXInteger(), True),
        'exciseopening': ('exciseopening', TXBoolean(), True),
        'useforfinalproduction': ('useforfinalproduction', TXBoolean(), True),
        'iscancelled': ('iscancelled', TXBoolean(), True),
        'hascashflow': ('hascashflow', TXBoolean(), True),
        'ispostdated': ('ispostdated', TXBoolean(), True),
        'usetrackingnumber': ('usetrackingnumber', TXBoolean(), True),
        'isinvoice': ('isinvoice', TXBoolean(), True),
        'mfgjournal': ('mfgjournal', TXBoolean(), True),
        'hasdiscounts': ('hasdiscounts', TXBoolean(), True),
        'aspayslip': ('aspayslip', TXBoolean(), True),
        'iscostcentre': ('iscostcentre', TXBoolean(), True),
        'isdeleted': ('isdeleted', TXBoolean(), True),
        'asoriginal': ('asoriginal', TXBoolean(), True),
        'poscashreceived': ('poscashreceived', TXString(), False),
        'exchgrate': ('exchgrate', TXString(), False),
        'address': ('address.list', TXMultilineString(), False),
        'basicbuyeraddress': ('basicbuyeraddress.list', TXMultilineString(), False),
        'basicorderterms': ('basicorderterms.list', TXMultilineString(), False),
    }

    lists = {
        'invoiceorderlist': ('invoiceorderlist', TallyInvoiceOrder, True),
        'ledgerentries': ('ledgerentries', ledgers.TallyLedgerEntry, True),
        'inventoryentries': ('allinventoryentries', stock.TallyInventoryEntry, True),
        'inventoryentriesin': ('inventoryentriesin', stock.TallyInventoryEntry, True),
        'inventoryentriesout': ('inventoryentriesout', stock.TallyInventoryEntry, True),
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


def get_list_proforma_invoice(*args, **kwargs):
    filters = kwargs.pop('filters', {})
    filters['VoucherTypeName'] = 'Performa Invoice'
    return TallyVouchersList(*args, filters=filters, **kwargs)


def get_list_stock_journal(*args, **kwargs):
    filters = kwargs.pop('filters', {})
    filters['VoucherTypeName'] = 'Stock Journal'
    return TallyVouchersList(*args, filters=filters, **kwargs)


def get_list_manufacturing_journal(*args, **kwargs):
    filters = kwargs.pop('filters', {})
    filters['VoucherTypeName'] = 'Manufacturing Journal'
    return TallyVouchersList(*args, filters=filters, **kwargs)
