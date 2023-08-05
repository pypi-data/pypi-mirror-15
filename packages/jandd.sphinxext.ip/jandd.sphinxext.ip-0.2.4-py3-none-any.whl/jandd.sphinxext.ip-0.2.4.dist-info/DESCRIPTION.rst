==================
jandd.sphinxext.ip
==================

This is an IP address extension for `Sphinx`_. The extension provides a domain
*ip* that allows marking IPv4 and IPv6 addresses in documentation and contains
directives to collect information regarding IP addresses in IP ranges.

.. _Sphinx: http://www.sphinx-doc.org/

Development
===========

The extension is developed in a git repository that can be cloned by running::

    git clone https://git.dittberner.info/sphinxext-ip.git

A repository browser is available at
https://git.dittberner.info/?p=sphinxext-ip.git.

Contributors
============

* `Jan Dittberner`_

.. _Jan Dittberner: https://jan.dittberner.info/


Changes
=======

0.2.4 - 2016-05-07
------------------

* fix index generation issue

0.2.3 - 2016-05-05
------------------

* fix regression in HTML builder that has been introduced in 0.2.2

0.2.2 - 2016-05-05
------------------

* fix index entries that broke the latex builder

0.2.1 - 2016-05-05
------------------

* fix handling of invalid IP address/range values
* implement a proper clear_doc method for the ip domain

0.2.0 - 2016-05-04
------------------

* display IP address lists as tables
* sort IP address lists numericaly


