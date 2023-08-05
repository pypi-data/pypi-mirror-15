# -*- coding: utf-8 -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2015 Lance Edgar
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
Database Configuration
"""

from __future__ import unicode_literals

import logging

from rattail.util import load_object
from rattail.exceptions import SQLAlchemyNotInstalled


log = logging.getLogger(__name__)


def engine_from_config(configuration, prefix='sqlalchemy.', **kwargs):
    """
    Custom version of the identically-named SQLAlchemy function.

    The purpose of the customization is to allow the ``poolclass`` parameter to
    be specified within the configuration.  If this option is present in the
    configuration dictionary, it will be coerced to the Python class it
    references and passed as a keyword argument to the "upstream" function.

    An example of the configuration leveraging this feature:

    .. code-block:: ini

       [rattail.db]
       sqlalchemy.url = sqlite:///tmp/rattail.sqlite
       sqlalchemy.poolclass = sqlalchemy.pool:NullPool
    """
    try:
        from sqlalchemy import engine_from_config
    except ImportError as error:
        raise SQLAlchemyNotInstalled(error)

    config = dict(configuration)

    # Convert 'poolclass' arg to actual class.
    key = '{}poolclass'.format(prefix)
    if key in config:
        kwargs.setdefault('poolclass', load_object(config[key]))
        del config[key]

    # Store 'record_changes' flag as private attr on engine.
    record_changes = False
    key = '{}record_changes'.format(prefix)
    if key in config:
        value = config.pop(key)
        # TODO: this logic was copied from `RattailConfig.getbool()`
        record_changes = value.lower() in ('true', 'yes', 'on', '1')

    engine = engine_from_config(config, prefix, **kwargs)
    if record_changes:
        engine._rattail_record_changes = True
    return engine


def get_engines(config, section='rattail.db'):
    """
    Fetch all database engines defined within a given config section.

    :returns: A dictionary of SQLAlchemy engine instances, with keys matching
       those found in config.
    """
    keys = config.get(section, 'keys', usedb=False)
    if keys:
        keys = keys.split(',')
    else:
        keys = ['default']

    engines = {}
    cfg = config.get_dict(section)
    for key in keys:
        key = key.strip()
        try:
            engines[key] = engine_from_config(cfg, prefix='{0}.'.format(key))
        except KeyError:
            if key == 'default':
                try:
                    engines[key] = engine_from_config(cfg, prefix='sqlalchemy.')
                except KeyError:
                    pass
    return engines


# TODO: Deprecate/remove this.
def get_default_engine(config, section='rattail.db'):
    """
    Fetch the default database engine defined in the given config object for a
    given section.

    :param config: A ``ConfigParser`` instance containing app configuration.

    :type section: string
    :param section: Optional section name within which the configuration
       options are defined.  If not specified, ``'rattail.db'`` is assumed.

    :returns: A SQLAlchemy engine instance, or ``None``.

    .. note::
       This function calls :func:`get_engines()` for the heavy lifting; see
       that function for more details on how the engine configuration is read.
    """
    return get_engines(config, section=section).get('default')


def configure_session(config, session):
    """
    Configure a session factory or instance.  Currently all this does is
    install the hook to record changes, if so config so dictates.
    """
    from rattail.db.changes import record_changes

    if config.getbool('rattail.db', 'changes.record', usedb=False):
        ignore_role_changes = config.getbool(
            'rattail.db', 'changes.ignore_roles', default=True, usedb=False)
        record_changes(session, ignore_role_changes)


def configure_versioning(config, manager=None, plugins=None, **kwargs):
    """
    Configure Continuum versioning.
    """
    if not config.getbool('rattail.db', 'versioning.enabled', default=False, usedb=False):
        return

    try:
        import sqlalchemy_continuum as continuum
        from rattail.db.continuum import versioning_manager, RattailPlugin
    except ImportError as error:
        raise SQLAlchemyNotInstalled(error)
    else:
        if manager is None:
            manager = versioning_manager
        if plugins is None:
            plugins = [RattailPlugin()]
        log.info("enabling Continuum versioning")
        continuum.make_versioned(manager=manager, plugins=plugins, **kwargs)
