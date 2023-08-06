:mod:`degu.applib` --- Library of RGI components
================================================

.. module:: degu.applib
   :synopsis: Library of RGI applications and middleware

.. versionadded:: 0.16

The goal of this module is to provide a number of pre-built RGI application
and middleware components for common scenarios.

.. warning::
    None of the classes in this module are yet API stable, use them at your
    own risk!


:class:`RouterApp`
------------------

.. class:: RouterApp(appmap)

    Generic RGI routing middleware.

    >>> def foo_app(session, request, api):
    ...     return (200, 'OK', {}, b'foo')
    ... 
    >>> def bar_app(session, request, api):
    ...     return (200, 'OK', {}, b'bar')
    ...
    >>> from degu.applib import RouterApp
    >>> router = RouterApp({'foo': foo_app, 'bar': bar_app})

    .. attribute:: appmap

        The *appmap* argument passed to the constructor.

    .. method:: __call__(session, request, api)

        RGI callable.



:class:`ProxyApp`
-----------------

.. class:: ProxyApp(client, key='conn')

    Generic RGI reverse-proxy application.

    .. attribute:: client

        The *client* argument passed to the constructor.

    .. attribute:: key

        The *key* argument passed to the constructor.

    .. method:: __call__(session, request, api)

        RGI callable.

