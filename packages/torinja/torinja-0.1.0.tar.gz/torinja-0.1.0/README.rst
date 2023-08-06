Torinja
=======

.. image:: https://travis-ci.org/afg984/torinja.svg?branch=master
    :target: https://travis-ci.org/afg984/torinja

Integrate Tornado Web Framework and Jinja2 Templates

Requires Python >= 3.3 or Python 2.7.

Installation
------------

.. code-block:: bash

    pip install torinja

Usage
-----

Configuration
~~~~~~~~~~~~~

Use torinja's ``Jinja2Env`` as the ``template_loader`` of your ``Application``.

.. code-block:: python

    from tornado.web import Application
    from torinja import Jinja2Env
    from jinja2 import PackageLoader

    application = Application(
        handlers=[],
        template_loader=Jinja2Env(
            loader=PackageLoader('myapp', 'templates'),  # You can pass any jinja2 loaders
        ),
        **other_settings
    )

``Jinja2Env`` is a ``jinja2.Environment`` subclass, so it accepts all the `options <http://jinja.pocoo.org/docs/dev/api/#jinja2.Environment>`_ to ``jinja2.Environment``.

The only difference is that ``autoescape`` is set to ``True`` by default.

Handlers
~~~~~~~~

In your handlers, you can call ``RequestHandler.render`` or ``RequestHandler.render_string`` as you would do with tornado templates.

.. code-block:: python

    class MyHandler(RequestHandler):

        def get(self):
            self.render('index.html', tornado='awesome', jinja2='rocks')

Templates
~~~~~~~~~

To use ``xsrf_form_html`` in your ``jinja2`` templates, use it as a variable.

.. code-block:: jinja2

    <form>
        {{ xsrf_form_html }}
        <input type="text" name="text">
        <!-- ... -->
    </form>

Tests
-----

To run the tests:

.. code-block:: bash

    python tests.py
