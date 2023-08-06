===========================================
|pi| Plug&Pie |qs| |bs| |cc| |rtd| |gitter|
===========================================

``plugandpie`` was designed to automatically set up sensors with drivers, making the initial
hardware configuration simpler and faster to implement. It is powered by community contributed
drivers and it's flexible enough to work with devices not yet directly supported. The package
also aims to provide utilities for monitoring and analyzing sensors, so you can make software-level
polling and set up complex observation models.


Driver Examples
---------------

By specifying directly the hardware interface and address, you have an unified access method for
any register on the device.

.. code:: python

    accelerometer = GenericDriver(interface=SMBusAdapter(1), address=0x1D)
    accelerometer.registers[0x2A].set(8)  # inactive
    accelerometer.registers[0x0E].set(0)  # range = 2g
    accelerometer.registers[0x2A].set(9)  # active, 800Hz

By reading a device configuration file that reflects its datasheet, you can have better namings
for your registers.

.. code:: python

    # TODO

By instantiating the correct driver, a standardized API can provide the meaningful data easily.

.. code:: python

    accelerometer = MMA8452Q(interface=SMBusAdapter(1), address=0x1D)
    accelerometer.get_ms2()

By reading a device configuration file, you can initialize all drivers immediately.

.. code:: python

    # TODO

Check out the documentation for examples of basic and advanced usages.

Monitor Examples
----------------

The most common uses of sensors is history analysis and real time telemetry. Both should
seamlessly plug into ``plugandpie`` drivers, so the package includes some utilities for
this purpose.



Installation: |pipv| |pipstatus|  |pipl| |pippyversions| |pipdm|
----------------------------------------------------------------
``plugandpie`` requires ``SMBus``, which at this time has no good Python 3 implementation or bindings.
A workaround can be found at https://procrastinative.ninja/2014/07/21/smbus-for-python34-on-raspberry/

Also, ``SMBus`` requires repeated starts in the ``i2c`` driver. This is not enabled by default on Raspberry Pi
and can be fixed with:

.. code::

 echo -n 1 > /sys/module/i2c_bcm2708/parameters/combined

This configuration resets on boot, so make sure to put this in a startup script.

**setup.sh** is a script that contain a fix for both problems, but does so in an intrusive way.
It is recommended for inexperienced users to install ``plugandpie`` for the first time,
but experienced users should solve those problems individually.


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