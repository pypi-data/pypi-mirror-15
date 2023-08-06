# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016 CERN.
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
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""Implementention of various utility functions."""

from __future__ import absolute_import, print_function

from flask import request
from invenio_oauth2server import require_api_auth, require_oauth_scopes

from .scopes import write_scope


def check_oauth2_scope(can_method, *myscopes):
    """Check OAuth2 scope."""
    def check(record, *args, **kwargs):
        @require_api_auth()
        @require_oauth_scopes(*myscopes)
        def can(self):
            return can_method(record)

        return type('CheckOAuth2Scope', (), {'can': can})()
    return check


def can_elasticsearch(record):
    """Try to search for given record."""
    search = request._methodview.search_class()
    search = search.get_record(str(record.id))
    return search.count() == 1


check_oauth2_scope_write = check_oauth2_scope(lambda x: True, write_scope.id)

check_oauth2_scope_write_elasticsearch = check_oauth2_scope(
    can_elasticsearch, write_scope.id)
