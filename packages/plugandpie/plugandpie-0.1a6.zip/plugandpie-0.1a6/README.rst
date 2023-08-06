===========================================
|pi| Plug&Pie |qs| |bs| |cc| |rtd| |gitter|
===========================================

The ``plugandpie`` package goal is to simplify the process of setting up and using sensors with Raspberry Pi.
Just by importing the package, if your sensor interface has a "device driver" available (community contribution) and it gives no ambiguity, you are ready to go.

For example, for a MMA8452Q accelerometer board by Microstack:

.. code:: python

 >>> import plugandpie as pnp
 >>> pnp.accelerometer.get_ms2()
 {'x': 4.50109912109375, 'y': -6.4739212890625, 'z': 5.42047255859375}

``plugandpie`` is specially better for I2C addresses because we can make good guesses about the device given it's address.

There are some cases where things are not going to be so trivial:

- Device could not be automatically identified, but there is a driver for it
- The driver does not give access to all desired registers (or it's buggy)
- No driver has been made for this sensor yet

The first case should be as simple as manually plugging the sensor proxy object (e.g. ``pnp.accelerometer``) to the device.
The second and third cases have different ways to work around:

- Create/Modify the driver for this device (and give it back to the community!)
- Translate the device datasheet into a configuration importable by ``plugandpie``
- Instantiate a generic device reader for the given interface that simply pulls all raw data

Examples of each scenario are present in the documentation.

After plugging your sensors and verifying that its data is accessible, life is all fresh juicy raspberry pie.
``plugandpie`` also aims to provide utilities for monitoring and analyzing sensors, so you can make software-level polling and set up complex observation models. For example, calling some function if the acceleration gets too high or automatically dump sensor data fine-grained to milliseconds.

Installation: |pipv| |pipstatus|  |pipl| |pippyversions| |pipdm|
----------------------------------------------------------------
``plugandpie`` requires ``SMBus``, which at this time has no good Python 3 implementation or bindings. A workaround can be found at https://procrastinative.ninja/2014/07/21/smbus-for-python34-on-raspberry/

Also, ``SMBus`` requires repeated starts in the ``i2c`` driver. This is not enabled by default on Raspberry Pi and can be fixed with:

.. code::

 echo -n 1 > /sys/module/i2c_bcm2708/parameters/combined

This configuration resets on boot, so make sure to put this in a startup script.

.. |pi| image:: https://raw.githubusercontent.com/villasv/plugandpie/master/docs/icon_sm.png
  :width: 30
.. |qs| image:: https://scrutinizer-ci.com/g/villasv/plugandpie/badges/quality-score.png?b=master
  :target: https://scrutinizer-ci.com/g/villasv/plugandpie/?branch=master
.. |bs| image:: https://travis-ci.org/villasv/plugandpie.svg?branch=master
  :target: https://travis-ci.org/villasv/plugandpie
.. |cc| image:: https://coveralls.io/repos/github/villasv/plugandpie/badge.svg?branch=master
  :target: https://coveralls.io/github/villasv/plugandpie?branch=master
.. |rtd| image:: https://readthedocs.org/projects/plugandpie/badge/?version=latest
  :target: http://plugandpie.readthedocs.io/en/latest/?badge=latest
.. |gitter| image:: https://badges.gitter.im/villasv/plugandpie.svg
  :target: https://gitter.im/villasv/plugandpie?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge

.. |pipdm| image:: https://img.shields.io/pypi/dm/plugandpie.svg
  :target: https://pypi.python.org/pypi/plugandpie
.. |pipv| image:: https://img.shields.io/pypi/v/plugandpie.svg
  :target: https://pypi.python.org/pypi/plugandpie
.. |pipl| image:: https://img.shields.io/pypi/l/plugandpie.svg
  :target: https://pypi.python.org/pypi/plugandpie
.. |pippyversions| image:: https://img.shields.io/pypi/pyversions/plugandpie.svg
  :target: https://pypi.python.org/pypi/plugandpie
.. |pipstatus| image:: https://img.shields.io/pypi/status/plugandpie.svg
  :target: https://pypi.python.org/pypi/plugandpie