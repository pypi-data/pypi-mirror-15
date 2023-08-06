# Copyright (c) 2015. Librato, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of Librato, Inc. nor the names of project contributors
#       may be used to endorse or promote products derived from this software
#       without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL LIBRATO, INC. BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


"""
The API supports the notion of a thread-based context stack. Implemented as a thread local variable, the stack
enables the aggregattion and reporting of telemetry for different dimenions of activity.

For example, a SQL query might be measured in the context of:
*	    a SQL statement (e.g., "SELECT u.name from users as u where id=?")
*	    a database connection pool
*	    the database schema
*	    the database host
*	    a user-defined context (e.g., "create-account")
*	    the HTTP request route
*	    the process identity

Context is implemented as a stack. Each item on the context stack has an identifier.

Auto-instrumentation is currently determined using hard-coded configuration.

Metrics are accumulated individually and as an intersection of the context.
"""
from collections import defaultdict

from librato_python_web.instrumentor.custom_logging import getCustomLogger

logger = getCustomLogger(__name__)


class _globals:
    context = None


def _get_context():
    if not _globals.context:
        threading = __import__('threading')
        _globals.context = threading.local()
    return _globals.context


def _set_state(state):
    """
    Assigns the state the given state.

    :param state: an set of state entries
    """
    _get_context().state = defaultdict(int, state)


def _get_state():
    """
    Returns this thread's state.

    :return: the state
    :rtype: dict
    """
    ctx = _get_context()
    if not getattr(ctx, 'state', None):
        _set_state({})
    return ctx.state


def push_state(name):
    if name:
        logger.debug('pushing state %s', name)
        _get_state()[name] += 1
        if '.' in name:
            name = name.split('.')[0]
            _get_state()[name] += 1


def pop_state(name):
    if name:
        logger.debug('popping state %s', name)
        count = _get_state().get(name)
        if count is None:
            logger.error('pop_state state does not contain %s', name)
        elif count > 1:
            _get_state()[name] = count - 1
        else:
            del _get_state()[name]

        if '.' in name:
            name = name.split('.')[0]
            count = _get_state().get(name)
            if count is None:
                logger.error('pop_state state does not contain %s', name)
            elif count > 1:
                _get_state()[name] = count - 1
            else:
                del _get_state()[name]


def has_state(name):
    return _get_state().get(name, 0) > 0
