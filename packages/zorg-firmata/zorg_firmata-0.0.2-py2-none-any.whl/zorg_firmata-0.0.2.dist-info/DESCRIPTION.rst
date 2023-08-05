Zorg Firmata
============

|Package Version| |Requirements Status| |Build Status| |Code Climate|
|Coverage Status|

What is Firmata?
----------------

    Firmata is a protocol for communicating with microcontrollers from
    software on a computer (or smartphone/tablet, etc). The protocol can
    be implemented in firmware on any microcontroller architecture as
    well as software on any computer software package (see list of
    client libraries below). ~ `Firmata Protocol
    Documentation <https://github.com/firmata/protocol>`__

Installation
------------

You can install this library on your machine using PIP.

::

    pip install zorg-firmata

Setup
-----

To use this library with your microcontroller, you will need to load the
Standard Firmata software onto it first. See `Uploading StandardFirmata
To
Arduino <https://github.com/MrYsLab/pymata-aio/wiki/Uploading-StandardFirmata-To-Arduino>`__
for an example of how to do this.

Examples
--------

Several examples for using the ``zorg-firmata`` module are available on
GitHub. https://github.com/zorg/zorg-firmata/tree/master/examples

Notes
-----

This module wraps the `PyMata <https://github.com/MrYsLab/PyMata>`__
library to provide Firmata support within the Zorg robotics framework.

.. |Package Version| image:: https://img.shields.io/pypi/v/zorg-firmata.svg
   :target: https://pypi.python.org/pypi/zorg-firmata/
.. |Requirements Status| image:: https://requires.io/github/zorg/zorg-firmata/requirements.svg?branch=master
   :target: https://requires.io/github/zorg/zorg-firmata/requirements/?branch=master
.. |Build Status| image:: https://travis-ci.org/zorg/zorg-firmata.svg?branch=master
   :target: https://travis-ci.org/zorg/zorg-firmata
.. |Code Climate| image:: https://codeclimate.com/github/zorg/zorg-firmata/badges/gpa.svg
   :target: https://codeclimate.com/github/zorg/zorg-firmata
.. |Coverage Status| image:: https://coveralls.io/repos/github/zorg/zorg-firmata/badge.svg?branch=master
   :target: https://coveralls.io/github/zorg/zorg-firmata?branch=master


