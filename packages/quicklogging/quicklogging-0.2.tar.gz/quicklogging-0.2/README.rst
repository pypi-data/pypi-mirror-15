.. _majerti: http://majerti.fr

|docs| - read the doc there (github rst is broken): http://quicklogging.readthedocs.io/en/latest/

Documentation for quicklogging
================================

*quicklogging* is a Python :py:mod:`logging` wrapper to 

    * remove a bit of logging boilerplate,
    * redirect print output.

``quicklogging`` transparently provides a logger with a name relevant 
to the code at hand: 

.. important:: 

    the name of the logger is the name of the module making the call

For instance, if you log from ``project/models/chair.py``, your logger will be named ``project.models.chair``.



*Advantage #1 of this naming scheme* 

        the configuration of the :py:class:`logging.Logger` s and handlers is much 
        easier -muting, changing verbosity for a particular piece of code etc

*Advantage #2*

        we can provide a :py:func:`quicklogging.catch_prints` and a :py:func:`quicklogging.warn_prints`  functionality to catch calls 
        to print() from specific modules (typically: the module you're editing).

Licence, original authors
---------------------------

* MIT (see file ``LICENCE`` ).
* authors: majerti_ - Feth AREZKI


Contents
---------

.. toctree::
   :numbered:
   :maxdepth: 2

   user_guide
   task_oriented
   source_doc
   logging_survival

.. |docs| image:: https://readthedocs.org/projects/quicklogging/badge/?version=latest
    :alt: Documentation Status
    :scale: 100%
    :target: https://quicklogging.readthedocs.io/en/latest/?badge=latest
