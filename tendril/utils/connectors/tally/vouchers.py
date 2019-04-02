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


from . import TallyElement
from .utils import yesorno


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
