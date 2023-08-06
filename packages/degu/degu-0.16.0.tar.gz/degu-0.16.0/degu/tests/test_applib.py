# degu: an embedded HTTP server and client library
# Copyright (C) 2014-2016 Novacut Inc
#
# This file is part of `degu`.
#
# `degu` is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# `degu` is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with `degu`.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors:
#   Jason Gerard DeRose <jderose@novacut.com>

"""
Unit tests for the `degu.applib` module.
"""

from unittest import TestCase
import os
from collections import OrderedDict

from ..base import Request
from ..sslhelpers import random_id
from ..misc import TempServer
from ..client import Client
from .. import applib


class TestRouterApp(TestCase):
    def test_init(self):
        def foo_app(session, request, api):
            return (200, 'OK', {}, b'foo')

        def bar_app(session, request, api):
            return (200, 'OK', {}, b'bar')

        # appmap not a dict instance:
        appmap = [('foo', foo_app), ('bar', bar_app)]
        with self.assertRaises(TypeError) as cm:
            applib.RouterApp(appmap)
        self.assertEqual(str(cm.exception),
            'appmap: need a {!r}; got a {!r}: {!r}'.format(dict, list, appmap)
        )

        # appmap has key that is not None or str instance:
        appmap = {'foo': foo_app, 17: bar_app}
        with self.assertRaises(TypeError) as cm:
            applib.RouterApp(appmap)
        self.assertEqual(str(cm.exception),
            'appmap: bad key: need a {!r}; got a {!r}: {!r}'.format(
                str, int, 17
            )
        )

        # appmap has value that isn't callable:
        bar_value = random_id()
        appmap = {'foo': foo_app, 'bar': bar_value}
        with self.assertRaises(TypeError) as cm:
            applib.RouterApp(appmap)
        self.assertEqual(str(cm.exception),
            "appmap['bar']: value not callable: {!r}".format(bar_value)
        )

        # Empty appmap:
        appmap = {}
        app = applib.RouterApp(appmap)
        self.assertIs(app.appmap, appmap)
        self.assertEqual(app.appmap, {})

        appmap = OrderedDict(appmap)
        app = applib.RouterApp(appmap)
        self.assertIs(app.appmap, appmap)
        self.assertEqual(app.appmap, {})

        # appmap single str key:
        appmap = {'foo': foo_app}
        app = applib.RouterApp(appmap)
        self.assertIs(app.appmap, appmap)
        self.assertEqual(app.appmap, {'foo': foo_app})

        appmap = OrderedDict(appmap)
        app = applib.RouterApp(appmap)
        self.assertIs(app.appmap, appmap)
        self.assertEqual(app.appmap, {'foo': foo_app})

        # appmap single key that is None:
        appmap = {None: foo_app}
        app = applib.RouterApp(appmap)
        self.assertIs(app.appmap, appmap)
        self.assertEqual(app.appmap, {None: foo_app})
        
        appmap = OrderedDict(appmap)
        app = applib.RouterApp(appmap)
        self.assertIs(app.appmap, appmap)
        self.assertEqual(app.appmap, {None: foo_app})

        # appmap has two keys, both str:
        appmap = {'foo': foo_app, 'bar': bar_app}
        app = applib.RouterApp(appmap)
        self.assertIs(app.appmap, appmap)
        self.assertEqual(app.appmap, {'foo': foo_app, 'bar': bar_app})

        appmap = OrderedDict(appmap)
        app = applib.RouterApp(appmap)
        self.assertIs(app.appmap, appmap)
        self.assertEqual(app.appmap, {'foo': foo_app, 'bar': bar_app})

        # appmap has two keys, one a str and the other None:
        appmap = {'foo': foo_app, None: bar_app}
        app = applib.RouterApp(appmap)
        self.assertIs(app.appmap, appmap)
        self.assertEqual(app.appmap, {'foo': foo_app, None: bar_app})

        appmap = OrderedDict(appmap)
        app = applib.RouterApp(appmap)
        self.assertIs(app.appmap, appmap)
        self.assertEqual(app.appmap, {'foo': foo_app, None: bar_app})

    def test_call(self):
        def foo_app(session, request, api):
            return (200, 'OK', {}, b'foo')

        def bar_app(session, request, api):
            return (200, 'OK', {}, b'bar')

        # appmap is empty:
        app = applib.RouterApp({})
        r = Request('GET', '/', {}, None, [], [], None)
        self.assertEqual(app(None, r, None), (410, 'Gone', {}, None))
        self.assertEqual(r.mount, [])
        self.assertEqual(r.path, [])
        self.assertEqual(app.appmap, {})

        r = Request('GET', '/foo', {}, None, [], ['foo'], None)
        self.assertEqual(app(None, r, None), (410, 'Gone', {}, None))
        self.assertEqual(r.mount, ['foo'])
        self.assertEqual(r.path, [])
        self.assertEqual(app.appmap, {})

        r = Request('GET', '/foo/', {}, None, ['foo'], [''], None)
        self.assertEqual(app(None, r, None), (410, 'Gone', {}, None))
        self.assertEqual(r.mount, ['foo', ''])
        self.assertEqual(r.path, [])
        self.assertEqual(app.appmap, {})

        # One appmap key, a str:
        app = applib.RouterApp({'foo': foo_app})
        r = Request('GET', '/foo', {}, None, [], ['foo'], None)
        self.assertEqual(app(None, r, None), (200, 'OK', {}, b'foo'))
        self.assertEqual(r.mount, ['foo'])
        self.assertEqual(r.path, [])
        self.assertEqual(app.appmap, {'foo': foo_app})

        r = Request('GET', '/bar', {}, None, [], ['bar'], None)
        self.assertEqual(app(None, r, None), (410, 'Gone', {}, None))
        self.assertEqual(r.mount, ['bar'])
        self.assertEqual(r.path, [])
        self.assertEqual(app.appmap, {'foo': foo_app})

        # One appmap key, an empty str:
        app = applib.RouterApp({'': foo_app})
        r = Request('GET', '/foo/', {}, None, ['foo'], [''], None)
        self.assertEqual(app(None, r, None), (200, 'OK', {}, b'foo'))
        self.assertEqual(r.mount, ['foo', ''])
        self.assertEqual(r.path, [])
        self.assertEqual(app.appmap, {'': foo_app})

        r = Request('GET', '/foo/bar', {}, None, ['foo'], ['bar'], None)
        self.assertEqual(app(None, r, None), (410, 'Gone', {}, None))
        self.assertEqual(r.mount, ['foo', 'bar'])
        self.assertEqual(r.path, [])
        self.assertEqual(app.appmap, {'': foo_app})

        # One appmap key, None:
        app = applib.RouterApp({None: foo_app})
        r = Request('GET', '/', {}, None, [], [], None)
        self.assertEqual(app(None, r, None), (200, 'OK', {}, b'foo'))
        self.assertEqual(r.mount, [])
        self.assertEqual(r.path, [])
        self.assertEqual(app.appmap, {None: foo_app})

        r = Request('GET', '/foo/', {}, None, ['foo'], [''], None)
        self.assertEqual(app(None, r, None), (410, 'Gone', {}, None))
        self.assertEqual(r.mount, ['foo', ''])
        self.assertEqual(r.path, [])
        self.assertEqual(app.appmap, {None: foo_app})

        # Two appmap keys, both str:
        app = applib.RouterApp({'foo': foo_app, 'bar': bar_app})
        r = Request('GET', '/foo', {}, None, [], ['foo'], None)
        self.assertEqual(app(None, r, None), (200, 'OK', {}, b'foo'))
        self.assertEqual(r.mount, ['foo'])
        self.assertEqual(r.path, [])
        self.assertEqual(app.appmap, {'foo': foo_app, 'bar': bar_app})

        r = Request('GET', '/bar', {}, None, [], ['bar'], None)
        self.assertEqual(app(None, r, None), (200, 'OK', {}, b'bar'))
        self.assertEqual(r.mount, ['bar'])
        self.assertEqual(r.path, [])
        self.assertEqual(app.appmap, {'foo': foo_app, 'bar': bar_app})

        r = Request('GET', '/baz', {}, None, [], ['baz'], None)
        self.assertEqual(app(None, r, None), (410, 'Gone', {}, None))
        self.assertEqual(r.mount, ['baz'])
        self.assertEqual(r.path, [])
        self.assertEqual(app.appmap, {'foo': foo_app, 'bar': bar_app})

        # Two appmap keys, one str one None:
        app = applib.RouterApp({'foo': foo_app, None: bar_app})
        r = Request('GET', '/foo', {}, None, [], ['foo'], None)
        self.assertEqual(app(None, r, None), (200, 'OK', {}, b'foo'))
        self.assertEqual(r.mount, ['foo'])
        self.assertEqual(r.path, [])
        self.assertEqual(app.appmap, {'foo': foo_app, None: bar_app})

        r = Request('GET', '/', {}, None, [], [], None)
        self.assertEqual(app(None, r, None), (200, 'OK', {}, b'bar'))
        self.assertEqual(r.mount, [])
        self.assertEqual(r.path, [])
        self.assertEqual(app.appmap, {'foo': foo_app, None: bar_app})

        r = Request('GET', '/foo/', {}, None, ['foo'], [''], None)
        self.assertEqual(app(None, r, None), (410, 'Gone', {}, None))
        self.assertEqual(r.mount, ['foo', ''])
        self.assertEqual(r.path, [])
        self.assertEqual(app.appmap, {'foo': foo_app, None: bar_app})

        # Two appmap keys, one empty str one None:
        app = applib.RouterApp({'': foo_app, None: bar_app})
        r = Request('GET', '/foo/', {}, None, ['foo'], [''], None)
        self.assertEqual(app(None, r, None), (200, 'OK', {}, b'foo'))
        self.assertEqual(r.mount, ['foo', ''])
        self.assertEqual(r.path, [])
        self.assertEqual(app.appmap, {'': foo_app, None: bar_app})

        r = Request('GET', '/', {}, None, [], [], None)
        self.assertEqual(app(None, r, None), (200, 'OK', {}, b'bar'))
        self.assertEqual(r.mount, [])
        self.assertEqual(r.path, [])
        self.assertEqual(app.appmap, {'': foo_app, None: bar_app})

        r = Request('GET', '/foo/bar', {}, None, ['foo'], ['bar'], None)
        self.assertEqual(app(None, r, None), (410, 'Gone', {}, None))
        self.assertEqual(r.mount, ['foo', 'bar'])
        self.assertEqual(r.path, [])
        self.assertEqual(app.appmap, {'': foo_app, None: bar_app})


class TestProxyApp(TestCase):
    def test_live(self):
        class Endpoint:
            def __init__(self, marker):
                self.marker = marker

            def __call__(self, session, request, api):
                return (200, 'OK', {}, self.marker)

        marker = os.urandom(16)
        app1 = Endpoint(marker)
        server1 = TempServer(('127.0.0.1', 0), app1)
        client1 = Client(server1.address)

        app2 = applib.ProxyApp(client1)
        server2 = TempServer(('127.0.0.1', 0), app2)
        client2 = Client(server2.address)

        conn = client2.connect()
        r = conn.get('/', {})
        self.assertEqual(r.status, 200)
        self.assertEqual(r.reason, 'OK')
        self.assertEqual(r.headers, {'content-length': 16})
        self.assertIs(r.body.chunked, False)
        self.assertEqual(r.body.read(), marker)
        conn.close()

