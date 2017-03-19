#!/usr/bin/env python
#
# Copyright (c) 2014 Hewlett-Packard Development Company, L.P.
# Copyright (c) 2013 OpenStack Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging

from functools import wraps
from bottle import abort, BottleException

LOG = logging.getLogger(__name__)


def catchall(func):
    """
    Wrapper to catch all exceptions
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except DwarfException as e:
            # Turn internal dwarf exceptions into bottle aborts
            LOG.warn('Dwarf exception caught: %s (%s)', e.message, e.status)
            abort(e.status, e.message)
        except BottleException as e:
            # Re-raise bottle exceptions
            LOG.warn('Bottle exception caught: %s', e.message)
            raise
        except Exception as e:   # pylint: disable=W0703
            LOG.exception('Unknown exception caught: %s', str(e))
            abort(500, str(e))
    return wrapper


class DwarfException(Exception):
    """
    Base Dwarf exception
    """
    message = 'Unknown failure'
    status = 500

    def __init__(self, **kwargs):
        if 'status' in kwargs:
            self.status = kwargs['status']
        self.message = self.message % kwargs
        super(DwarfException, self).__init__(self.message)


class Failure(DwarfException):
    message = '%(reason)s'
    status = 500


class BadRequest(DwarfException):
    message = '%(reason)s'
    status = 400


class Forbidden(DwarfException):
    message = '%(reason)s'
    status = 403


class NotFound(DwarfException):
    message = '%(reason)s'
    status = 404


class Conflict(DwarfException):
    message = '%(reason)s'
    status = 409


class CommandExecutionError(DwarfException):
    message = 'Failed to run command: %(reason)s'
    status = 500
