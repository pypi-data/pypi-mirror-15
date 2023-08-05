pytest-single_file_logging
==========================

.. image:: https://travis-ci.org/darthghandi/pytest-single-file-logging.svg?branch=master
    :target: https://travis-ci.org/darthghandi/pytest-single-file-logging
    :alt: See Build Status on travis-ci

.. image:: https://img.shields.io/pypi/v/nine.svg?maxAge=2592000
    :target: https://pypi.python.org/pypi/pytest-single-file-logging
    :alt: Latest PyPi build

Allow for multiple processes to log to a single file

----

This `Pytest`_ plugin was generated with `Cookiecutter`_ along with `@hackebrot`_'s `Cookiecutter-pytest-plugin`_ template.


Features
--------

* Allows all workers created by xdist to log to the same configuration


Requirements
------------

* Pytest
* gevent 1.1+
* xdist


Installation
------------

You can install "pytest-single_file_logging" via `pip`_ from `PyPI`_::

    $ pip install pytest-single_file_logging


Usage
-----

A pytest fixture `logger` is provided by this plugin. Using the fixture is easy::

    def test_warning_log(logger):
    logger.warning('this is your last warning!')


The standard library logging library is used with the logging configuration
pulled from the `--logconfig` option. The supported format for the configuration
file is json and dictconfig. Documentation of dictconfig is located `here`_

Contributing
------------
Contributions are very welcome. Tests can be run with `tox`_, please ensure
the coverage at least stays the same before you submit a pull request.

License
-------

Distributed under the terms of the `Apache Software License 2.0`_ license, "pytest-single_file_logging" is free and open source software


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.

.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`@hackebrot`: https://github.com/hackebrot
.. _`MIT`: http://opensource.org/licenses/MIT
.. _`BSD-3`: http://opensource.org/licenses/BSD-3-Clause
.. _`GNU GPL v3.0`: http://www.gnu.org/licenses/gpl-3.0.txt
.. _`Apache Software License 2.0`: http://www.apache.org/licenses/LICENSE-2.0
.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin
.. _`file an issue`: https://github.com/darthghandi/pytest-single_file_logging/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.org/en/latest/
.. _`pip`: https://pypi.python.org/pypi/pip/
.. _`PyPI`: https://pypi.python.org/pypi
.. _`here`: https://docs.python.org/3.5/library/logging.config.html#logging-config-dictschema

