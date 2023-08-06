bobtemplates.odoo
=================

.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl.html
   :alt: License: AGPL 3.0 or Later
.. image:: https://badge.fury.io/py/bobtemplates.odoo.svg
   :target: http://badge.fury.io/py/bobtemplates.odoo
.. image:: https://travis-ci.org/acsone/bobtemplates.odoo.svg?branch=master
   :target: https://travis-ci.org/acsone/bobtemplates.odoo

``bobtemplates.odoo`` is a set of `mr.bob
<https://mrbob.readthedocs.io/en/latest/>`_
templates to use when developing Odoo addons.

It provides the following templates:

  * ``addon``: an addon skeletton, with optional OCA README and icon
  * ``model``: an Odoo model with accompanying form, tree, action, menu,
    demo data and ACL
  * ``test``: a test class

The following are candidates (pull requests welcome):

  * ``report``
  * ``controller``
  * ``wizard``
  * ``widget``

Install
~~~~~~~

  .. code:: shell

    pip install bobtemplates.odoo

Quickstart
~~~~~~~~~~

CAUTION: it is recommanded to backup or vcs commit your current
directory before running these commands, so you can easily see
what has been generated and/or changed.

Create a new addon in the current directory:

  .. code:: shell

    mrbob bobtemplates.odoo:addon

Now go to the newly created addon directory and run this to
add a new model, with associated views, demo data, and acl:

  .. code:: shell

    mrbob bobtemplates.odoo:model

Add a test class:

  .. code:: shell

    mrbob bobtemplates.odoo:test

Tip: read the `mr.bob user guide
<http://mrbob.readthedocs.io/en/latest/userguide.html>`_.
In particular it explain how to set default values to avoid
retyping the same answers at each run (such as the copyright
author).

Useful links
~~~~~~~~~~~~

* pypi page: https://pypi.python.org/pypi/bobtemplates.odoo
* code repository: https://github.com/acsone/bobtemplates.odoo
* report issues at: https://github.com/acsone/bobtemplates.odoo/issues

Credits
~~~~~~~

Author:

  * Stéphane Bidoul (`ACSONE <http://acsone.eu/>`_)

Inspired by https://github.com/plone/bobtemplates.plone.

Contributors:

  * Olivier Laurent (`ACSONE <http://acsone.eu/>`_)
  * Adrien Peiffer (`ACSONE <http://acsone.eu/>`_) 

Maintainer
----------

.. image:: https://www.acsone.eu/logo.png
   :alt: ACSONE SA/NV
   :target: http://www.acsone.eu

This module is maintained by ACSONE SA/NV.

Changes
~~~~~~~

.. Future (?)
.. ----------
.. -

1.0.0b2 (2016-06-17)
--------------------
- addon template: add optional OCA mode (author, README.rst and icon.svg)
- model template: improve order of import in the model file
- model template: avoid to set ir.model.access data as non updatable record

1.0.0b1 (2016-06-16)
--------------------
- add post render message inviting the user to add the generated xml
  files in __openerp__.py data section
- auto add model import to models/__init__.py
- many improvements and fixes to the model template (views, security,
  demo data, and more)
- addon template
- test template
- tests (with tox and travis)

1.0.0a2 (2016-06-15)
--------------------
- fix broken namespace package distribution

1.0.0a1 (2016-06-15)
--------------------
- first version, very rough template for an Odoo model with view


