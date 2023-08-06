============
python-boatd
============

.. image:: https://badge.fury.io/py/python-boatdclient.svg
    :target: http://badge.fury.io/py/python-boatdclient

.. image:: https://travis-ci.org/boatd/python-boatd.png?branch=master
    :target: https://travis-ci.org/boatd/python-boatd

Python module for writing `boatd <https://github.com/boatd/boatd>`_ behavior
scripts.

Installing
==========

``$ pip install python-boatdclient``

class **Boat**
==============

A boat controlled by boatd


**Attributes**
----------------

``heading``:
Return the current heading of the boat in degrees

``position``:
Return a tuple in the form ``(latitude, longitude)``

``version``:
Return the version of boatd

``wind``:
Return a tuple in the form ``(direction, speed)``. This contains the direction of the wind in degrees and the speed the wind is blowing in knots.

**methods**
-----------

``def __init__(self, host='localhost', port=2222)``

Create a boat instance, connecting to boatd at ``host`` on port ``port``

``def __rudder__(self, angle)``

Set the angle of the rudder to be ``angle`` degrees

``def __sail__(self, angle)``

Set the angle of the sail to ``angle`` degrees

