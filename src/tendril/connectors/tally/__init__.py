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
Tally XML Primitives and API Engine
-----------------------------------
"""


from copy import copy
from six import BytesIO
from six import iteritems
from six import string_types
from inspect import isclass
from collections import namedtuple

from lxml import etree
from bs4 import BeautifulSoup

from requests import post
from requests.exceptions import ConnectionError
from requests.structures import CaseInsensitiveDict

from .utils.dates import get_date_range
from .utils.converters import TallyPropertyConverter
from .utils.cache import cachefs

try:
    from tendril.config import TALLY_HOST
    from tendril.config import TALLY_PORT
except ImportError:
    TALLY_HOST = 'localhost'
    TALLY_PORT = 9002


TallyQueryParameters = namedtuple('TallyQueryParameters',
                                  'header body')

TallyRequestHeader = namedtuple('TallyRequestHeader',
                                'version tallyrequest type id')

TallyConversionSpec = namedtuple('TallyConversionSpec',
                                 'tag tx hardfail')


class TallyConversionError(Exception):
    pass


class TallyTagNotFound(TallyConversionError):
    pass


class TallyTagAmbiguous(TallyConversionError):
    pass


class TallyConverterNotSupported(TallyConversionError):
    pass


class TallyNotAvailable(ConnectionError):
    pass


class TallyObject(object):
    def __init__(self, soup):
        self._soup = soup


class TallyElement(TallyObject):
    def __init__(self, soup, ctx=None):
        super(TallyElement, self).__init__(soup)
        self._ctx = ctx
        self._populate()

    elements = {}
    descendent_elements = {}
    attrs = {}
    lists = {}

    @property
    def company_name(self):
        return self._ctx.company_name

    @property
    def company_masters(self):
        # TODO Provide 2.x compatible import
        from . import masters
        return masters.get_master(self.company_name)

    def _convert_from_tally(self, spec, candidates):
        try:
            if len(candidates) == 0:
                raise TallyTagNotFound(spec, self.name)
            if len(candidates) > 1:
                raise TallyTagAmbiguous(spec, candidates)

            elif isinstance(candidates[0], string_types):
                candidate_text = candidates[0]
            elif isclass(spec.tx) and issubclass(spec.tx, TallyElement):
                candidate_text = candidates[0]
            elif isinstance(spec.tx, TallyPropertyConverter):
                candidate_text = candidates[0].text
            else:
                raise TallyConverterNotSupported(spec, candidates)
            if isinstance(spec.tx, TallyPropertyConverter):
                return spec.tx.from_tallyxml(candidate_text)
            elif isclass and issubclass(spec.tx, TallyElement):
                return spec.tx(candidate_text, self._ctx)
            else:
                raise TallyConverterNotSupported(spec, candidates)
        except TallyConversionError:
            if spec.hardfail:
                raise
            else:
                return None

    def _process_elements(self, elements=None, recursive=False):
        if elements is None:
            elements = self.elements
        for k, v in iteritems(elements):
            spec = TallyConversionSpec(*v)
            try:
                candidates = self._soup.findChildren(v[0], recursive=recursive)
            except AttributeError as e:
                raise TallyTagNotFound(spec, e)
            val = self._convert_from_tally(spec, candidates)
            setattr(self, k, val)

    def _process_descendent_elements(self):
        self._process_elements(self.descendent_elements, recursive=True)

    def _process_attrs(self):
        for k, v in iteritems(self.attrs):
            spec = TallyConversionSpec(*v)
            try:
                candidate = self._soup.attrs[spec.tag]
            except KeyError as e:
                raise TallyTagNotFound(spec, e)
            val = self._convert_from_tally(spec, [candidate])
            setattr(self, k, val)

    def _process_lists(self):
        for k, v in iteritems(self.lists):
            spec = TallyConversionSpec(*v)
            try:
                candidates = self._soup.findChildren(v[0] + '.list', recursive=False)
            except AttributeError as e:
                raise TallyTagNotFound(spec, e)
            val = [self._convert_from_tally(spec, [c]) for c in candidates]
            setattr(self, k, val)

    def _populate(self):
        self._process_attrs()
        self._process_elements()
        self._process_lists()
        self._process_descendent_elements()


class TallyReport(object):
    _header = 'Export Data'
    _container = None
    _cachename = None
    _content = {}

    def __init__(self, company_name, dt=None, end_dt=None):
        self._xion = None
        self._soup = None
        self._dt = dt
        self._end_dt = end_dt
        self._company_name = company_name

    @property
    def company_name(self):
        return self._company_name

    @property
    def cachename(self):
        if not self._cachename:
            return None
        company_name = copy(self.company_name)
        company_name = company_name.replace(' ', '_')
        company_name = company_name.replace('.', '')
        company_name = company_name.replace('-', '')
        return "{0}.{1}".format(self._cachename, company_name)

    @staticmethod
    def _build_fetchlist(parent, fetchlist):
        for item in fetchlist:
            f = etree.SubElement(parent, 'FETCH')
            f.text = item

    def _set_request_date(self, svnode, dt=None, end_dt=None):
        if dt is None and self._dt:
            dt = self._dt
        (start, end), current = get_date_range(dt, end_dt)
        svfd = etree.SubElement(svnode, 'SVFROMDATE', TYPE='Date')
        svfd.text = start.strftime("%d-%m-%Y")
        svtd = etree.SubElement(svnode, 'SVTODATE', TYPE='Date')
        svtd.text = end.strftime("%d-%m-%Y")
        svcd = etree.SubElement(svnode, 'SVCURRENTDATE', TYPE='Date')
        svcd.text = current.strftime("%d-%m-%Y")

    def _set_request_staticvariables(self, svnode):
        svef = etree.SubElement(svnode, 'SVEXPORTFORMAT')
        svef.text = '$$SysName:XML'
        svec = etree.SubElement(svnode, 'ENCODINGTYPE')
        svec.text = 'UNICODE'
        if self.company_name:
            svcc = etree.SubElement(svnode, 'SVCURRENTCOMPANY', TYPE="String")
            svcc.text = self.company_name

    def _build_request_body(self):
        raise NotImplementedError

    def _build_request_header(self):
        # TODO Move into the engine?
        h = etree.Element('HEADER')
        if isinstance(self._header, str):
            tr = etree.SubElement(h, 'TALLYREQUEST')
            tr.text = self._header
        elif isinstance(self._header, TallyRequestHeader):
            v = etree.SubElement(h, 'VERSION')
            v.text = str(self._header.version)
            tr = etree.SubElement(h, 'TALLYREQUEST')
            tr.text = self._header.tallyrequest
            ty = etree.SubElement(h, 'TYPE')
            ty.text = self._header.type
            rid = etree.SubElement(h, 'ID')
            rid.text = self._header.id
        return etree.ElementTree(h)

    def _acquire_raw_response(self):
        self._xion = TallyXMLEngine()
        query = TallyQueryParameters(self._build_request_header(),
                                     self._build_request_body())
        self._soup = self._xion.execute(query, cachename=self.cachename)

    def _acquire_cached_raw_response(self):
        try:
            with cachefs.open(self.cachename + '.xml', 'rb') as f:
                content = f.read()
            self._soup = BeautifulSoup(content.decode('utf-8', 'ignore'), 'lxml')
        except:
            raise TallyNotAvailable

    @property
    def soup(self):
        if not self._soup:
            try:
                self._acquire_raw_response()
            except TallyNotAvailable:
                if cachefs and self.cachename:
                    print("Trying to return cached response for {0} from {1}"
                          "".format(self.cachename, cachefs))
                    self._acquire_cached_raw_response()
                else:
                    raise
        return self._soup

    def __getattr__(self, item):
        if item not in self._content.keys():
            raise AttributeError(item)
        soup = self.soup
        if self._container:
            soup = soup.find(self._container)
        val = CaseInsensitiveDict()
        for y in [self._content[item][1](x, self)
                  for x in soup.findAll(self._content[item][0])]:
            val[y.name] = y
        self.__setattr__(item, val)
        return val


class TallyXMLEngine(object):
    """
    Very bare-bones architecture. Could do with more structure.  
    """
    def __init__(self):
        self._query = None
        self._response = None

    def execute(self, query, cachename=None):
        self.query = query
        headers = {'Content-Type': 'application/xml'}
        uri = 'http://{0}:{1}'.format(TALLY_HOST, TALLY_PORT)
        xmlstring = BytesIO()
        self.query.write(xmlstring)
        try:
            print("Sending Tally request to {0}".format(uri))
            r = post(uri, data=xmlstring.getvalue(), headers=headers)
        except ConnectionError as e:
            print("Got Exception")
            print(e)
            raise TallyNotAvailable
        if cachefs and cachename:
            with cachefs.open(cachename + '.xml', 'wb') as f:
                f.write(r.content)
        self._response = BeautifulSoup(r.content.decode('utf-8', 'ignore'), 'lxml')
        return self._response

    @staticmethod
    def _query_base():
        root = etree.Element('ENVELOPE')
        query = etree.ElementTree(root)
        return query

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, params):
        q = self._query_base()
        q.getroot().append(params.header.getroot())
        body = etree.SubElement(q.getroot(), 'BODY')
        body.append(params.body.getroot())
        self._query = q

    @property
    def response(self):
        return self._response

    def print_query(self):
        s = BytesIO()
        self.query.write(s)
        print(s.getvalue())
