# -*- coding: utf-8 -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2016 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU Affero General Public License as published by the Free
#  Software Foundation, either version 3 of the License, or (at your option)
#  any later version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for
#  more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Database Utilities
"""

from __future__ import unicode_literals, absolute_import

import pprint
import logging

from sqlalchemy import orm

# TODO: Deprecate/remove these imports.
from alembic.util import obfuscate_url_pw
from rattail.db.config import engine_from_config, get_engines, get_default_engine, configure_session


log = logging.getLogger(__name__)


def maxlen(attr):
    """
    Return the maximum length for the given attribute.
    """
    if len(attr.property.columns) == 1:
        type_ = attr.property.columns[0].type
        return getattr(type_, 'length', None)


def make_topo_sortkey(model, metadata=None):
    """
    Returns a function suitable for use as a ``key`` kwarg to a standard Python
    sorting call.  This key function will expect a single class mapper and
    return a sequence number associated with that model.  The sequence is
    determined by SQLAlchemy's topological table sorting.
    """
    if metadata is None:
        metadata = model.Base.metadata

    tables = {}
    for i, table in enumerate(metadata.sorted_tables, 1):
        tables[table.name] = i

    log.debug("topo sortkeys for '{}' will be:\n{}".format(model.__name__, pprint.pformat(
        [(i, name) for name, i in sorted(tables.iteritems(), key=lambda t: t[1])])))

    def sortkey(name):
        mapper = orm.class_mapper(getattr(model, name))
        return tuple(tables[t.name] for t in mapper.tables)

    return sortkey
