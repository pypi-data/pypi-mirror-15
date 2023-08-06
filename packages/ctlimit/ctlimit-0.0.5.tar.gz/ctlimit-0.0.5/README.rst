ctlimit - child time limit
==========================

A Glib and systemd based daemon to limit the daily computer usage time of our children.


Documentation
-------------

Please read the source or create the html-documentation using the following command::

	python setup.py build_sphinx


Changelog
---------

xxxx-xx-xx Version 0.0.5:

Documentation updates.

2016-06-08 Version 0.0.4:

Fix an incompatibility with the latest released version of pydbus.

2016-06-08 Version 0.0.3:

Add a DBus interface to ctlimit. It is now possible to get the
current usage time of a user and to set/increase the limit of the current day.
Code cleanups and a bit more documentation.

2016-05-07 Version 0.0.2:

Separate the sd-daemon logic and the time-logic
The new module sddaemon contains a base class for new style daemons.

2016-04-24 Version 0.0.1:

A first working version.
