========
Overview
========



Imports Alienvault OTX pulses to a MISP instance.

* Free software: Apache 2.0 license

Installation
============

::

    pip install otx-misp

Documentation
=============

https://otx-misp.readthedocs.io/

Alienvault OTX SDK
==================

All files in the `src/otx_misp/otx` directory are Copyright 2015 AlienVault, Inc. and under the Apache 2.0 license.




Changelog
=========

1.0.0 (2016-06-21)
------------------

* First stable version
* Pulse Traffic Light Protocol level added as tag in MISP event
* If the last part of a MISP tag and a Pulse tag are the same, tag the MISP event
* MISP attributes `to_ids` field

0.3.0 (2016-06-20)
------------------

* Fix default handling for distribution, threat_level and analysis parameters
* Better performance: Use OTXv2 generator API and remove some delays

0.2.0 (2016-06-14)
------------------

* Integrate OTXv2 as a subtree.

0.1.0 (2016-06-14)
------------------

* First release on PyPI.


