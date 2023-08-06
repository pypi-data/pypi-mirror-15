Cattleprod
==========

A quick-and-dirty Python wrapper for the Rancher API. Tries do be dynamic in what it does, so that every API action is mapped dynamically into the API without the need to update source code. For a quickstart introduction please see the github repository.

The wrapper is far from complete, so YMMV if you try to use it, but I hope it is stable.

CHANGELOG
=========

0.6.0
-----

Date: 2016-06-14

- Authentication using HTTP basic auth works now (and pretty much everything else which is provided by the ``requests`` module)


0.5.1
-----

Date: 2016-06-07

- 5.0.1 release because of download issues with PyPI. No idea why.


0.5.0
-----

Date: 2016-05-12

- BREAKING: Different object name (``RancherObject`` -> ``Rod``)
- BREAKING: Different entry point (``cattleprod.poke(url)``)
- FEATURE: Based on ``DotMap`` now (`DotMap github URL <https://github.com/drgrib/dotmap/>`_)
- FEATURE: Providing ``do_*(data=None)`` wrappers now for the ``actions { ... }`` links
- DOC: Updated readme in source repository


0.4.0
-----

Date: 2015-12-18

- initial public release



