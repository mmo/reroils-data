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

"""ITEM JSON schema tests."""

from __future__ import absolute_import, print_function

from json import loads

import pytest
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from pkg_resources import resource_string


def item_test_required(item_schema, item_minimal_record):
    """Test required for item jsonschema."""
    validate(item_minimal_record, item_schema)

    with pytest.raises(ValidationError):
        validate({}, item_schema)


def test_itemid(item_schema, item_minimal_record):
    """Test itemid for item jsonschema."""
    validate(item_minimal_record, item_schema)

    with pytest.raises(ValidationError):
        minimal_record['itemid'] = 25
        validate(item_minimal_record, item_schema)


def test_barcode(item_schema, item_minimal_record):
    """Test barcode for item jsonschema."""
    validate(item_minimal_record, item_schema)

    with pytest.raises(ValidationError):
        minimal_record['barcode'] = '2'
        validate(item_minimal_record, item_schema)


def test_callNumber(item_schema, item_minimal_record):
    """Test call_number for item jsonschema."""
    validate(item_minimal_record, item_schema)

    with pytest.raises(ValidationError):
        minimal_record['callNumber'] = 25
        validate(item_minimal_record, item_schema)


def test_localisation(item_schema, item_minimal_record):
    """Test location for item jsonschema."""
    validate(item_minimal_record, item_schema)

    with pytest.raises(ValidationError):
        minimal_record['localisation'] = 25
        validate(item_minimal_record, item_schema)