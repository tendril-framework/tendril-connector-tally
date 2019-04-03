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
from .utils import parse_date


class TallyCurrencyDailyRate(TallyElement):
    elements = {
        'date': ('date', parse_date, True),
        'specifiedrate': ('specifiedrate', str, True),
        'transactedrate': ('transactedrate', str, False),
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
        'name': ('name', str, True),
        'reservedname': ('reservedname', str, True),
    }

    elements = {
        'activefrom': ('activefrom', str, False),
        'activeto': ('activeto', str, False),
        'narration': ('narration', str, False),
        'mailingname': ('mailingname', str, False),
        'expandedsymbol': ('expandedsymbol', str, False),
        'decimalsymbol': ('decimalsymbol', str, False),
        'originalsymbol': ('originalsymbol', str, False),
        'issuffix': ('issuffix', yesorno, False),
        'hasspace': ('hasspace', yesorno, False),
        'inmillions': ('inmillions', yesorno, False),
        'sortposition': ('sortposition', int, False),
        'decimalplaces': ('decimalplaces', int, False),
        'decimalplacesforprinting': ('decimalplacesforprinting', int, False),
    }

    lists = {
        'dailystdrates': ('dailystdrates', TallyCurrencyDailyStdRate, False),
        'dailybuyingrates': ('dailybuyingrates', TallyCurrencyDailyBuyingRate, False),
        'dailysellingrates': ('dailysellingrates', TallyCurrencyDailySellingRate, False),
    }

    def __repr__(self):
        return "<TallyCurrency {0}>".format(self.name)
