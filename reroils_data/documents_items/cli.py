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

"""Click command-line interface for record management."""

from __future__ import absolute_import, print_function

import random
import uuid
from random import randint

import click
from flask.cli import with_appcontext
from invenio_circulation.api import Item
from invenio_db import db
from invenio_indexer.api import RecordIndexer
from invenio_pidstore.models import PersistentIdentifier

from ..items.minters import item_id_minter
from ..locations.api import Location
from .api import DocumentsWithItems


@click.command('createitems')
@click.option('-v', '--verbose', 'verbose', is_flag=True, default=False)
@click.option(
    '-c', '--count', 'count', type=click.INT, default=-1,
    help='default=for all records'
)
@click.option(
    '-i', '--itemscount', 'itemscount', type=click.INT, default=5,
    help='default=1'
)
@with_appcontext
def create_items(verbose, count, itemscount):
    """Create circulation items."""
    records = PersistentIdentifier.query.filter_by(pid_type='doc')
    if count == -1:
        count = records.count()
    record_indexer = RecordIndexer()

    click.secho(
        'Starting generating {0} items, random {1} ...'.format(
            count, itemscount),
        fg='green')

    with click.progressbar(records[:count], length=count) as bar:
        for rec in bar:
            recitem = DocumentsWithItems.get_record(rec.object_uuid)

            for i in range(0, randint(1, itemscount)):
                recitem.add_item(create_random_item())
                # TODO optimize with bulk commit/indexing

            db.session.commit()
            record_indexer.index(recitem)


# @fixtures.command()
# @click.option('-v', '--verbose', 'verbose', is_flag=True, default=False)
# @with_appcontext
# def reindex(verbose):
#     """Reindex records."""
#     click.secho(
#         'Starting reindexing ...',
#         fg='green')
#     record_indexer = RecordIndexer()
#     records = PersistentIdentifier.query.filter_by(pid_type='recid')
#     with click.progressbar(records, length=records.count()) as bar:
#         for rec in bar:
#             recitem = Record.get_record(rec.object_uuid)
#             if verbose:
#                 click.echo('Reindexing {0}'.format(recitem.id))
#             record_indexer.index(recitem)


def create_random_item(verbose=False):
    """Create items with randomised values."""
    item_types = ['standard_loan', 'short_loan', 'no_loan']
    locations_pids = Location.get_all_pids()

    id_ = uuid.uuid4()
    data = {}
    item_id_minter(id_, data)

    n = int(data['pid'])
    data['barcode'] = str(10000000000 + n)
    data['item_type'] = random.choice(item_types)
    data['location_pid'] = random.choice(locations_pids)

    data['callNumber'] = str(n).zfill(5)

    item = Item.create(data, id_=id_)
    if randint(0, 5) == 0:
        item.loan_item()
    elif randint(0, 20) == 0:
        item.lose_item()
    if verbose:
        click.echo(item.id)
    item.commit()
    return item
