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
Docstring for __init__.py
"""

from six import iteritems
import requests
from lxml import etree
from StringIO import StringIO
from collections import namedtuple
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError
from tendril.inventory.acquire import MasterNotAvailable

try:
    from tendril.utils.config import TALLY_HOST
except ImportError:
    TALLY_HOST = 'localhost'


TallyQueryParameters = namedtuple('TallyQueryParameters',
                                  'tallyrequest body')


class TallyNotAvailable(MasterNotAvailable):
    pass


def yesorno(s):
    if s == 'Yes':
        return True
    elif s == 'No':
        return False
    raise ValueError


class TallyObject(object):
    def __init__(self, soup):
        self._soup = soup


class TallyMasterElement(TallyObject):
    def __init__(self, soup, ctx):
        super(TallyMasterElement, self).__init__(soup)
        self._ctx = ctx
        self._populate()

    elements = {}

    def _populate(self):
        for k, v in iteritems(self.elements):
            try:
                val = v[1](self._soup.findChild(v[0]).text)
            except (TypeError, AttributeError):
                if not v[2]:
                    val = None
                else:
                    raise
            except ValueError:
                raise
            setattr(self, k, val)


class TallyXMLEngine(object):
    """
    Very bare-bones architecture. Could do with more structure.  
    """
    def __init__(self):
        self._query = None
        self._response = None

    def execute(self, query):
        self.query = query
        headers = {'Content-Type': 'application/xml'}
        uri = 'http://{0}:9002'.format(TALLY_HOST)
        xmlstring = StringIO()
        self.query.write(xmlstring)
        try:
            r = requests.post(uri, data=xmlstring.getvalue(), headers=headers)
        except ConnectionError:
            raise TallyNotAvailable
        self._response = BeautifulSoup(r.content, 'lxml')
        return self._response

    @staticmethod
    def _query_base():
        root = etree.Element('ENVELOPE')
        etree.SubElement(root, 'HEADER')
        etree.SubElement(root, 'BODY')
        query = etree.ElementTree(root)
        return query

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, params):
        q = self._query_base()
        tr = etree.SubElement(q.find('HEADER'), 'TALLYREQUEST')
        tr.text = params.tallyrequest
        q.find('BODY').append(params.body.getroot())
        self._query = q

    @property
    def response(self):
        return self._response

    def print_query(self):
        s = StringIO()
        self.query.write(s)
        print(s.getvalue())

    def print_response(self):
        s = StringIO()
        self.response.write(s)
        print(s.getvalue())
