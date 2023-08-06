xbus.broker
===========

.. image:: https://drone.xcg.io/api/badges/xcg/xbus.broker/status.svg
   :alt: Build Status
   :target: https://drone.xcg.io/xcg/xbus.broker

xbus.broker is the central piece of the Xbus project.

Related projects:
  - xbus.file_emitter <https://bitbucket.org/xcg/xbus.file_emitter>
  - xbus.monitor <https://bitbucket.org/xcg/xbus.monitor>
  - xbus_monitor_js <https://bitbucket.org/xcg/xbus_monitor_js>
  - xbus.clearinghouse <https://bitbucket.org/xcg/xbus.clearinghouse>


Xbus
----

Xbus is an Enterprise service bus. As such it aims to help IT departments
achieve a better application infrastructure layout by providing a way to
urbanize the IT systems.

The goals of urbanization are:
  - high coherence
  - low coupling

More information about Xbus:
  - Documentation: <http://xbusbroker.readthedocs.org/>
  - Website: <https://xbus.io/>


Installing
----------

Get requirements: python3-dev, 0mq, python3 and redis::

  $ sudo apt-get install libzmq3-dev python3 python3-dev redis-server virtualenvwrapper

Set up a virtualenv with Python 3::

  $ mkvirtualenv -p /usr/bin/python3 xbus

Install the xbus.broker package::

  $ pip install xbus.broker


Configuring
-----------

Create configuration files (eg for the 0.1.3 version)::

  $ wget https://bitbucket.org/xcg/xbus.broker/raw/0.1.3/etc/config.ini-example -O config.ini
  $ wget https://bitbucket.org/xcg/xbus.broker/raw/0.1.3/etc/logging.ini-example -O logging.ini

Edit the files following comments written inside.
Note: Ensure the path to the logging file is an absolute path.


Initialize the database
-----------------------

Run the "setup_xbusbroker" program::

  $ setup_xbusbroker -c config.ini


Migrating an existing database
------------------------------

Use the "migrate_xbus_broker" project. Instructions are on
<https://bitbucket.org/xcg/migrate_xbus_broker/>.


Running
-------

Run the "start_xbusbroker" program::

  $ start_xbusbroker -c config.ini
