

import arrow


def yesorno(s):
    if s == 'Yes':
        return True
    elif s == 'No':
        return False
    raise ValueError


def parse_date(tally_date):
    date_st = "{0}-{1}-{2}".format(tally_date[0:4], tally_date[4:6], tally_date[6:8])
    return arrow.get(date_st)
