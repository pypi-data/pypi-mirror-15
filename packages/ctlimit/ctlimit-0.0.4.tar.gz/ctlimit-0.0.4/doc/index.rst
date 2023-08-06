.. pyheapdump documentation master file, created by
   sphinx-quickstart on Wed Jun 22 14:05:04 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

ctlimit - child time limit
==========================


Installation
------------

First make sure, that your system meets the following requirements

1. Your operating system uses systemd and polkit. Meanwhile most Linux distributions do.

2. Your desktop uses a supported session manager. I tested the logout with gnome, mate and lxde.
   Others might work too. To add a new session manager, edit the logout script :program:`logout_X11.bash`.

3. The following commands are required to run ctlimit:

   1. :program:`python3.4` or any later version

   2. :program:`play`. On debian install package *sox*.

   3. :program:`dbus-send`. On debian install package *dbus*.

   4. :program:`notify-send`. On debian install package *libnotify-bin*.

4. ctlimit uses gobject interospection (GI) to access system libraties. Therefore you must install
   the distribution packages that provide

   1. The Python 3 binding generator for libraries that support gobject-introspection.
      On debian install package *python3-gi*.

   2. The GI introspection data for the GLib, Gio, Gobject libraries. On debian install package *gir1.2-glib-2.0*.

5. To install ctlimit you need additionally:

   1. The Python extension *pip*. If the command ``python3.4 -m pip`` fails,
      you need to install pip. On debian install package *python3-pip*.

   2. The command :program:`pkg-config`. On debian install package *pkg-config*.

   3. The development files for systemd. Make sure the command ``pkg-config systemd --variable=systemdsystemunitdir``
      emits a sensible location.

Then execute the following commands as root::

   # python3 -m pip install ctlimit
   # python3 -m ctlimit -c /dev/null --install-system-files
   # systemctl start ctlimit.service
   # systemctl enable ctlimit.service


Configuration
-------------

By default ctlimit reads its configuration from /etc/ctlimit.conf and uses :class:`~configparser.Configparser`
to parse the file. This :class:`~configparser.Configparser` preserves case and suppors :class:`~configparser.ExtendedInterpolation`.
The installation creates a sample configuration file, that describes the options.

.. literalinclude:: ../ctlimit/ctlimit.conf

Don't forget to reload the configuration after changing the configuration::

   $ sudo systemctl reload ctlimit.service

Alternatively you can send a send SIGHUP to the ctlimit process.

DBus-Interface
--------------

The ctlimit DBus service shows you the current (=for the current day) usage time and the limit for each user and
lets you change the current limit, if you want to grant some additional time. To prevent unauthorized
changes to the current limit, the system dbus policy configuration file
:file:`/etc/dbus-1/system.d/de.kruis.ctlimit1.conf` allows this function only for root and members of the unix group *parents*.

Examples
^^^^^^^^

Query the current time of user ``alice``::

    $ dbus-send --system --type=method_call --print-reply \
    > --dest=de.kruis.ctlimit1 "/de/kruis/ctlimit1/User$(id -u alice)" \
    > org.freedesktop.DBus.Properties.Get \
    > string:'de.kruis.ctlimit1.User' string:'CurrentTime'

Give another 30 minutes (=1800 seconds) to user ``bob``::

    $ dbus-send --system --type=method_call --print-reply \
    > --dest=de.kruis.ctlimit1 "/de/kruis/ctlimit1/User$(id -u alice)" \
    > de.kruis.ctlimit1.User.IncreaseCurrentLimit \
    > int32:1800

Attach a Pydevd remote debugging server. Requires root.::

    $ PYDEVD_DIR=$(find $(dirname $(which eclipse)) -type d -name pysrc)
    $ # check the value of PYDEVD_DIR! It must contain pydevd.py
    $ sudo dbus-send --system --type=method_call \
    > --dest=de.kruis.ctlimit1 "/de/kruis/ctlimit1" \
    > de.kruis.ctlimit1.Daemon.AttachPydevd \
    > string:"$PYDEVD_DIR" \
    > string:'{"stderrToServer": true, "stdoutToServer": true}'

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

