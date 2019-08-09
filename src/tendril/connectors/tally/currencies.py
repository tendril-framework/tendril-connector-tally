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
Tally Currency Definitions
--------------------------
"""


from . import TallyElement
from .utils.converters import TXBoolean
from .utils.converters import TXDate
from .utils.converters import TXString
from .utils.converters import TXInteger


class TallyCurrencyDailyRate(TallyElement):
    elements = {
        'date': ('date', TXDate(required=True), True),
        'specifiedrate': ('specifiedrate', TXString(), True),
        'transactedrate': ('transactedrate', TXString(), False),
    }

    def __repr__(self):
        return "<{0} {1} S:{2} T:{3}>" \
               "".format(self.__class__.__name__, self.date.format('DD-MM-YY'),
                         self.specifiedrate, self.transactedrate)


class TallyCurrencyDailyStdRate(TallyCurrencyDailyRate):
    pass


class TallyCurrencyDailyBuyingRate(TallyCurrencyDailyRate):
    pass


class TallyCurrencyDailySellingRate(TallyCurrencyDailyRate):
    pass


class TallyCurrency(TallyElement):
    attrs = {
        'name': ('name', TXString(required=True), True),
        'reservedname': ('reservedname', TXString(), True),
    }

    elements = {
        'activefrom': ('activefrom', TXString(), False),
        'activeto': ('activeto', TXString(), False),
        'narration': ('narration', TXString(), False),
        'mailingname': ('mailingname', TXString(), False),
        'expandedsymbol': ('expandedsymbol', TXString(), False),
        'decimalsymbol': ('decimalsymbol', TXString(), False),
        'originalsymbol': ('originalsymbol', TXString(), False),
        'issuffix': ('issuffix', TXBoolean(), False),
        'hasspace': ('hasspace', TXBoolean(), False),
        'inmillions': ('inmillions', TXBoolean(), False),
        'sortposition': ('sortposition', TXInteger(), False),
        'decimalplaces': ('decimalplaces', TXInteger(), False),
        'decimalplacesforprinting': ('decimalplacesforprinting', TXInteger(), False),
    }

    lists = {
        'dailystdrates': ('dailystdrates', TallyCurrencyDailyStdRate, False),
        'dailybuyingrates': ('dailybuyingrates', TallyCurrencyDailyBuyingRate, False),
        'dailysellingrates': ('dailysellingrates', TallyCurrencyDailySellingRate, False),
    }

    def __repr__(self):
        return "<TallyCurrency {0}>".format(self.name)
