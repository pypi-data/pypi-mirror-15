=====================================
Twitcher: A simple OWS Security Proxy 
=====================================

.. image:: https://travis-ci.org/bird-house/twitcher.svg?branch=master
   :target: https://travis-ci.org/bird-house/twitcher
   :alt: Travis Build

Twitcher (the bird-watcher)
  *a birdwatcher mainly interested in catching sight of rare birds.* (`Leo <https://dict.leo.org/ende/index_en.html>`_).

Twitcher is a security proxy for Web Processing Services (WPS). The execution of a WPS process is blocked by the proxy. The proxy service provides access tokens (uuid, Macaroons) which needs to be used to run a WPS process. The access tokens are valid only for a short period of time.

The implementation is not restricted to WPS services. It will be extended to more OWS services like WMS (Web Map Service) and CSW (Catalogue Service for the Web) and might also be used for Thredds catalog services.

Twitcher is a **prototype** implemented in Python with the `Pyramid`_ web framework.

Twitcher is part of the `Birdhouse`_ project. The documentation is on `ReadTheDocs`_.

.. _Pyramid: http://www.pylonsproject.org
.. _Birdhouse: http://bird-house.github.io
.. _ReadTheDocs: http://twitcher.readthedocs.io/en/latest/


Changes
*******

0.1.6 (2016-06-01)
==================

* updated docs.
* renamed python package to pyramid_twitcher.
* conda envionment.yml added.
* using get_sane_name().
* replaced httplib2 by requests.

Bugfixes:

* don't check token for allowed requests (#14).
* ignore decoding errors of response content (#13).
* fixed twitcher app config: wrong egg name.

0.1.5 (2016-04-22)
==================

* fixed docs links

0.1.4 (2016-04-19)
==================

* Fixed MANIFEST.in
* Fixed service database index.
* Updated makefile.
* Added more links to appendix.

0.1.0 (2015-12-07)
==================

Initial Release.



