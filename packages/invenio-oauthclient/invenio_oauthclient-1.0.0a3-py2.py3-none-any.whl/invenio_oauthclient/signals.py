# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015 CERN.
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

"""Signals used together with various handlers."""

from blinker import Namespace

_signals = Namespace()

account_info_received = _signals.signal('oauthclient-account-info-received')
"""Signal is sent after account info handler response.

Example subscriber:

.. code-block:: python

    from invenio_oauthclient.signals import account_info_received

    # During overlay initialization.
    @account_info_received.connect
    def load_extra_information(remote, token=None, response=None,
                               account_info=None):
        response = remote.get('https://example.org/api/resource')
        # process response

"""

account_setup_received = _signals.signal('oauthclient-account-setup-received')
"""Signal is sent after account info handler response.

Example subscriber:

.. code-block:: python

    from invenio_oauthclient.signals import account_setup_received

    # During overlay initialization.
    @account_setup_received.connect
    def load_extra_information(remote, token=None, response=None,
                               account_setup=None):
        response = remote.get('https://example.org/api/resource')
        # process response

"""
