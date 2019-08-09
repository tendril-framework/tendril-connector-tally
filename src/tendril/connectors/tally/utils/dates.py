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
Tally Date Range Utilities
--------------------------
"""

import re
import arrow
from six import string_types
from datetime import date


def get_financial_year(dt, half=None, quarter=None):
    if isinstance(dt, arrow.Arrow):
        dt = dt.date()

    if dt.month >= 4:
        year = dt.year
    else:
        year = dt.year - 1

    if quarter:
        quarter = int(quarter)
        if quarter == 1:
            start = arrow.get(date(year, 4, 1))
            end = arrow.get(date(year, 6, 30))
        elif quarter == 2:
            start = arrow.get(date(year, 7, 1))
            end = arrow.get(date(year, 9, 30))
        elif quarter == 3:
            start = arrow.get(date(year, 10, 1))
            end = arrow.get(date(year, 12, 31))
        elif quarter == 4:
            start = arrow.get(date(year + 1, 1, 1))
            end = arrow.get(date(year + 1, 3, 31))
        else:
            raise ValueError
    elif half:
        half = int(half)
        if half == 1:
            start = arrow.get(date(year, 4, 1))
            end = arrow.get(date(year, 9, 30))
        elif half == 2:
            start = arrow.get(date(year, 10, 1))
            end = arrow.get(date(year + 1, 3, 31))
        else:
            raise ValueError
    else:
        start = arrow.get(date(year, 4, 1))
        end = arrow.get(date(year + 1, 3, 31))

    return start, end


def get_calendar_year(dt, half=None, quarter=None):
    if isinstance(dt, arrow.Arrow):
        dt = dt.date()
    year = dt.year

    if quarter:
        quarter = int(quarter)
        if quarter == 1:
            start = arrow.get(date(year, 1, 1))
            end = arrow.get(date(year, 3, 31))
        elif quarter == 2:
            start = arrow.get(date(year, 4, 1))
            end = arrow.get(date(year, 6, 30))
        elif quarter == 3:
            start = arrow.get(date(year, 7, 1))
            end = arrow.get(date(year, 9, 30))
        elif quarter == 4:
            start = arrow.get(date(year, 10, 1))
            end = arrow.get(date(year, 12, 31))
        else:
            raise ValueError
    elif half:
        half = int(half)
        if half == 1:
            start = arrow.get(date(year, 1, 1))
            end = arrow.get(date(year, 6, 30))
        elif half == 2:
            start = arrow.get(date(year, 7, 1))
            end = arrow.get(date(year, 12, 31))
        else:
            raise ValueError
    else:
        start = arrow.get(date(year, 1, 1))
        end = arrow.get(date(year, 12, 31))

    return start, end


rex_fy = re.compile(r"^(?P<type>[FC]Y)((20)?(?P<y1>\d\d)-)?(20)?(?P<y2>\d\d) ?(Q(?P<quarter>[1234])|H(?P<half>[12]))?$")


def get_date_range(dt=None, end_dt=None):
    if isinstance(dt, date):
        dt = arrow.get(dt)
    if isinstance(end_dt, date):
        end_dt = arrow.get(end_dt)
    if not dt:
        dt = arrow.get(date.today())
        return get_financial_year(dt), dt
    if end_dt:
        assert isinstance(dt, arrow.Arrow)
        assert isinstance(end_dt, arrow.Arrow)
        return (dt, end_dt), end_dt
    if isinstance(dt, arrow.Arrow):
        return get_financial_year(dt), dt
    if isinstance(dt, string_types):
        m = rex_fy.match(dt)
        if m and m.group('type') == 'FY':
            ed = arrow.get(date(2000 + int(m.group('y2')), 3, 31))
            return get_financial_year(ed, m.group('half'), m.group('quarter')), ed
        elif m and m.group('type') == 'CY':
            ed = arrow.get(date(2000 + int(m.group('y2')), 12, 31))
            return get_calendar_year(ed, m.group('half'), m.group('quarter')), ed
    raise ValueError("Could not get a date range for {0}, {1}"
                     "".format(dt, end_dt))
