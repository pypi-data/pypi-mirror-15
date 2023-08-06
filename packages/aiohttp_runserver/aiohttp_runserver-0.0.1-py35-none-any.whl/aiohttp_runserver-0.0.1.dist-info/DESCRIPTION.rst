aiohttp-runserver
=================

CLI based development server for
`aiohttp <http://aiohttp.readthedocs.io/en/stable/>`__ based web apps.

Includes: \* auto-reload on code changes. \* optional static file
serving without modifying your app. \* optional Livereload of css,
javascript and full pages using
`livereload.js <https://github.com/livereload/livereload-js>`__ and a
livereload websocket interface built using aiohttp's excellent websocket
support. \* (soon) optional batteries included support for
`aiohttp\_debugtoolbar <https://github.com/aio-libs/aiohttp_debugtoolbar>`__.

.. figure:: https://s3.amazonaws.com/samuelcolvin/aiohttp-runserver-screenshot.png
   :alt: aiohttp runserver screenshot

   aiohttp-runserver-screenshot

Usage
-----

Usage is via a command line interface ``aiohttp-runserver`` or briefer
alias ``arun``:

::

    arun --help

Simple usage:

::

    arun src/app.py get_app

Where ``get_app`` is a function in ``src/app.py`` with takes one
argument ``loop`` and returns an instance of ``web.Application``.

Installation
------------

::

    pip install aiohttp_runserver


