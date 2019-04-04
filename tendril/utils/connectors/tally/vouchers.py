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
from .utils import parse_date
from .utils import parse_datetime

from . import TallyElement
from . import TallyReport
from . import TallyRequestHeader

import ledgers
import stock


class TallyVoucherType(TallyElement):
    # NOTE Might not be the same in all masters as in the earlier inventory masters
    descendent_elements = {
        'name': ('name', str, True),
    }
    elements = {
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


class TallyInvoiceOrder(TallyElement):
    elements = {
        'basicorderdate': ('basicorderdate', parse_date, True),
        'basicpurchaseorderno': ('basicpurchaseorderno', str, True),
    }

    def __repr__(self):
        return "<TallyInvoiceOrder {0} {1}>" \
               "".format(self.basicpurchaseorderno,
                         self.basicorderdate.format('DD-MM-YY'))


class TallyVoucher(TallyElement):
    attrs = {
        '_vchtype': ('vchtype', str, True),
        'name': ('remoteid', str, True),
    }

    elements = {
        'activeto': ('activeto', str, False),
        'alteredon': ('alteredon', str, False),
        'date': ('date', parse_date, True),
        'taxchallandate': ('taxchallandate', str, False),
        'reconcilationdate': ('reconcilationdate', str, False),
        'taxchequedate': ('taxchequedate', str, False),
        'form16issuedate': ('form16issuedate', str, False),
        'cstformissuedate': ('cstformissuedate', str, False),
        'cstformrecvdate': ('cstformrecvdate', str, False),
        'fbtfromdate': ('fbtfromdate', str, False),
        'fbttodate': ('fbttodate', str, False),
        'auditedon': ('auditedon', str, False),
        'guid': ('guid', str, True),
        'pricelevel': ('pricelevel', str, False),
        'autocostlevel': ('autocostlevel', str, False),
        'narration': ('narration', str, True),
        'alteredby': ('alteredby', str, False),
        'natureofsales': ('natureofsales', str, False),
        'excisenotificationno': ('excisenotificationno', str, False),
        'exciseunitname': ('exciseunitname', str, False),
        'classname': ('classname', str, False),
        'poscardledger': ('poscardledger', str, False),
        'poscashledger': ('poscashledger', str, False),
        'posgiftledger': ('posgiftledger', str, False),
        'poschequeledger': ('poschequeledger', str, False),
        'taxbankchallannumber': ('taxbankchallannumber', str, False),
        'taxchallanbsrcode': ('taxchallanbsrcode', str, False),
        'taxchequenumber': ('taxchequenumber', str, False),
        'taxbankname': ('taxchequenumber', str, False),
        'vouchertypename': ('vouchertypename', str, False),
        'vouchernumber': ('vouchernumber', str, False),
        'reference': ('reference', str, False),
        'partyledgername': ('partyledgername', str, True),
        'partyname': ('partyname', str, True),
        'basicpartyname': ('basicpartyname', str, True),
        'basicvoucherchequename': ('basicvoucherchequename', str, False),
        'basicvouchercrosscomment': ('basicvouchercrosscomment', str, False),
        'exchcurrencyname': ('exchcurrencyname', str, False),
        'serialmaster': ('serialmaster', str, False),
        'serialnumber': ('serialnumber', str, False),
        'statadjustmenttype': ('statadjustmenttype', str, False),
        'taxbankbranchname': ('taxbankbranchname', str, False),
        'cstformissuetype': ('cstformissuetype', str, False),
        'cstformissuenumber': ('cstformissuenumber', str, False),
        'cstformrecvtype': ('cstformrecvtype', str, False),
        'cstformrecvnnumber': ('cstformrecvnnumber', str, False),
        'excisetreasurynumber': ('excisetreasurynumber', str, False),
        'excisetreasuryname': ('excisetreasuryname', str, False),
        'fbtpaymenttype': ('fbtpaymenttype', str, False),
        'poscardnumber': ('poscardnumber', str, False),
        'poschequenumber': ('poschequenumber', str, False),
        'poschequebankname': ('poschequebankname', str, False),
        'taxadjustment': ('taxadjustment', str, False),
        'challantype': ('challantype', str, False),
        'chequedepositorname': ('chequedepositorname', str, False),
        'basicshippedby': ('basicshippedby', str, False),
        'basicdestinationcountry': ('basicdestinationcountry', str, False),
        'basicbuyername': ('basicbuyername', str, False),
        'basicplaceofreceipt': ('basicplaceofreceipt', str, False),
        'basicshipdocumentno': ('basicshipdocumentno', str, False),
        'basicportofloading': ('basicportofloading', str, False),
        'basicportofdischarge': ('basicportofdischarge', str, False),
        'basicfinaldestination': ('basicfinaldestination', str, False),
        'basicorderref': ('basicorderref', str, False),
        'basicshipvesselno': ('basicshipvesselno', str, False),
        'basicbuyerssalestaxno': ('basicbuyerssalestaxno', str, False),
        'basicduedateofpymt': ('basicduedateofpymt', str, False),
        'basicserialnuminpla': ('basicserialnuminpla', str, False),
        'basicdatetimeofinvoice': ('basicdatetimeofinvoice', parse_datetime, True),
        'basicdatetimeofremoval': ('basicdatetimeofinvoice', parse_datetime, True),
        'vchgstclass': ('vchgstclass', str, False),
        'costcentrename': ('costcentrename', str, False),
        'enteredby': ('enteredby', str, False),
        'requestorrule': ('requestorrule', str, False),
        'destinationgodown': ('destinationgodown', str, False),
        'diffactualqty': ('diffactualqty', yesorno, True),
        'audited': ('audited', yesorno, True),
        'forjobcosting': ('forjobcosting', yesorno, True),
        'isoptional': ('isoptional', yesorno, True),
        'effectivedate': ('effectivedate', parse_date, True),
        'useforinterest': ('useforinterest', yesorno, True),
        'useforgainloss': ('useforgainloss', yesorno, True),
        'useforgodowntransfer': ('useforgodowntransfer', yesorno, True),
        'useforcompound': ('useforcompound', yesorno, True),
        'alterid': ('alterid', int, True),
        'exciseopening': ('exciseopening', yesorno, True),
        'useforfinalproduction': ('useforfinalproduction', yesorno, True),
        'iscancelled': ('iscancelled', yesorno, True),
        'hascashflow': ('hascashflow', yesorno, True),
        'ispostdated': ('ispostdated', yesorno, True),
        'usetrackingnumber': ('usetrackingnumber', yesorno, True),
        'isinvoice': ('isinvoice', yesorno, True),
        'mfgjournal': ('mfgjournal', yesorno, True),
        'hasdiscounts': ('hasdiscounts', yesorno, True),
        'aspayslip': ('aspayslip', yesorno, True),
        'iscostcentre': ('iscostcentre', yesorno, True),
        'isdeleted': ('isdeleted', yesorno, True),
        'asoriginal': ('asoriginal', yesorno, True),
        'poscashreceived': ('poscashreceived', str, False),
        'exchgrate': ('exchgrate', str, False),
    }

    lists = {
        'invoiceorderlist': ('invoiceorderlist', TallyInvoiceOrder, True),
        'ledgerentries': ('ledgerentries', ledgers.TallyLedgerEntry, True),
        'inventoryentries': ('allinventoryentries', stock.TallyInventoryEntry, True),
    }

    multilines = {
        'address': ('address', str, False),
        'basicbuyeraddress': ('basicbuyeraddress', str, False),
        'basicorderterms': ('basicorderterms', str, False),
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
