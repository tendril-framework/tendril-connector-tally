

import re
import arrow
from six import string_types
from datetime import date


def get_financial_year(dt):
    if dt.month >= 4:
        start = date(dt.year, 4, 1)
        end = date(dt.year + 1, 3, 31)
    else:
        start = date(dt.year - 1, 4, 1)
        end = date(dt.year, 3, 31)
    return start, end


rex_fy = re.compile(r"^FY((20)?(?P<y1>\d\d)-)?(20)?(?P<y2>\d\d)$")


def get_date_range(dt=None, end_dt=None):
    if not dt:
        dt = date.today()
        return get_financial_year(dt), dt
    if end_dt:
        assert isinstance(dt, date)
        assert isinstance(end_dt, date)
        return dt, end_dt, end_dt
    if isinstance(dt, date):
        return get_financial_year(dt), dt
    if isinstance(dt, string_types):
        m = rex_fy.match(dt)
        if m:
            ed = date(int(m.group('y2')), 3, 31)
            return get_financial_year(ed), ed
    raise ValueError("Could not get a date range for {0}, {1}"
                     "".format(dt, end_dt))


def yesorno(s):
    if s == 'Yes':
        return True
    elif s == 'No':
        return False
    raise ValueError


def parse_date(tally_date):
    date_st = "{0}-{1}-{2}".format(tally_date[0:4], tally_date[4:6], tally_date[6:8])
    return arrow.get(date_st)
