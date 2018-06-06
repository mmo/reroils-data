# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2017 RERO.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, RERO does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""BNFAUTHTOJSON module tests."""

from __future__ import absolute_import, print_function

from dojson.contrib.marc21.utils import create_record

from reroils_data.documents.dojson.contrib.bnfauthtojson import bnfauthtojson


# identifier_for_person: [003]
def test_bnf_auth_to_identifier_for_person():
    """Test dojson bnf_auth_to_identifier_for_person."""

    http = 'http://data.bnf.fr/ark:/12148/cb10356443j'
    marcxml = """
    <record>
      <controlfield tag="003">{}</controlfield>
    </record>
    """.format(http)
    marcjson = create_record(marcxml)
    data = bnfauthtojson.do(marcjson)
    identifier_for_person = data.get('identifier_for_person')
    assert identifier_for_person.get('source') == 'bnf'
    assert identifier_for_person.get('value') == http


# gender: [120$a]
def test_bnf_auth_to_gender():
    """Test dojson bnf_auth_to_gender."""

    marcxml = """
    <record>
      <datafield tag="120" ind1="1" ind2="0">
        <subfield code="a">a</subfield>
      </datafield>
    </record>
    """
    marcjson = create_record(marcxml)
    data = bnfauthtojson.do(marcjson)
    assert data.get('gender') == 'female'


# language_of_person: [101$a repetitive]
def test_bnf_auth_to_language_of_person():
    """Test dojson bnf_auth_to_language_of_person."""

    marcxml = """
    <record>
      <datafield tag="101" ind1="1" ind2="0">
        <subfield code="a">eng</subfield>
      </datafield>
    </record>
    """
    marcjson = create_record(marcxml)
    data = bnfauthtojson.do(marcjson)
    assert data.get('language_of_person') == ('eng',)

    marcxml = """
    <record>
      <datafield tag="101" ind1="1" ind2="0">
        <subfield code="a">eng</subfield>
        <subfield code="a">ger</subfield>
      </datafield>
    </record>
    """
    marcjson = create_record(marcxml)
    data = bnfauthtojson.do(marcjson)
    assert data.get('language_of_person') == ('eng', 'ger')


# biographical_information: [300$a 34x$a repetitive]
def test_bnf_auth_to_biographical_information():
    """Test dojson bnf_auth_to_biographical_information."""

    marcxml = """
    <record>
      <datafield tag="300" ind1="1" ind2="0">
        <subfield code="a">Chef des bureaux</subfield>
      </datafield>
    </record>
    """
    marcjson = create_record(marcxml)
    data = bnfauthtojson.do(marcjson)
    biographical_informations = data.get('biographical_information')
    assert biographical_informations == [
        {
            'source': 'bnf',
            'language': 'fre',
            'value': 'Chef des bureaux'
        }
    ]

    marcxml = """
    <record>
      <datafield tag="300" ind1="1" ind2="0">
        <subfield code="a">Chef des bureaux</subfield>
      </datafield>
      <datafield tag="341" ind1="1" ind2="0">
        <subfield code="a">Chef des bureaux 2</subfield>
      </datafield>
    </record>
    """
    marcjson = create_record(marcxml)
    data = bnfauthtojson.do(marcjson)
    biographical_informations = data.get('biographical_information')
    assert biographical_informations == [
        {
            'source': 'bnf',
            'language': 'fre',
            'value': 'Chef des bureaux'
        },
        {
            'source': 'bnf',
            'language': 'fre',
            'value': 'Chef des bureaux 2'
        }
    ]
