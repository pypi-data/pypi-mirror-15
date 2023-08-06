=============================
python-xirsys
=============================
A Python 3 interface to the XirSys API

Badges
------

.. image:: https://img.shields.io/travis/kavdev/python-xirsys/master.svg?style=flat-square
        :target: https://travis-ci.org/kavdev/python-xirsys
.. image:: https://img.shields.io/codecov/c/github/kavdev/python-xirsys/master.svg?style=flat-square
        :target: http://codecov.io/github/kavdev/python-xirsys?branch=master
.. image:: https://img.shields.io/requires/github/kavdev/python-xirsys.svg?style=flat-square
        :target: https://requires.io/github/kavdev/python-xirsys/requirements/?branch=master
.. image:: https://img.shields.io/codacy/fd05754e919f4a18b4cfada7ef9632fa.svg?style=flat-square
        :target: https://www.codacy.com/app/kavanaugh-development/python-xirsys/dashboard

.. image:: https://img.shields.io/pypi/v/python-xirsys.svg?style=flat-square
        :target: https://pypi.python.org/pypi/python-xirsys
.. image:: https://img.shields.io/pypi/dw/python-xirsys.svg?style=flat-square
        :target: https://pypi.python.org/pypi/python-xirsys

.. image:: https://img.shields.io/github/issues/kavdev/python-xirsys.svg?style=flat-square
        :target: https://github.com/kavdev/python-xirsys/issues
.. image:: https://img.shields.io/github/license/kavdev/python-xirsys.svg?style=flat-square
        :target: https://github.com/kavdev/python-xirsys/blob/master/LICENSE

Usage
-----

Install python-xirsys:

.. code-block:: bash

    pip install python-xirsys

Build a Connection object:

.. code-block:: python

    from python-xirsys import Connection

    connection = Connection(username="<xirsys_username>", secret_key="<xirsys_secret_key>"

Grab XirSys signaling server:

.. code-block:: python

    >>> SignalingServer.list_all(connection=connection)
    <SignalingServer [server_address]>
    >>> server = SignalingServer.list_all(connection=connection)
    >>> server.address
    '<server_address>'

Generate a XirSys WebSocket token:

.. code-block:: python

    >>> from python_xirsys.objects import SignalingServer
    >>> SignalingServer.generate_token(connection=connection, domain="domain.com", application="application", room="room", secure=True)
    '<token>'

Grab a list of XirSys ICE servers:

.. code-block:: python

    >>> from python_xirsys.objects import ICEServer
    >>> ICEServer.list_all(connection=connection, domain="domain.com", application="application", room="room", secure=True, timeout=30)
    [<ICEServer [url]>, ...]
    >>> ice_servers = ICEServer.list_all(connection=connection, domain="domain.com", application="application", room="room", secure=True, timeout=30)
    >>> ice_server = ice_servers[0]
    >>> ice_server.url
    '<url>'
    >>> ice_server.server_type
    'stun'
    >>> ice_server.username
    None
    >>> ice_server.credential
    None
    >>> ice_server = ice_servers[1]
    >>> ice_server.url
    '<url>'
    >>> ice_server.server_type
    'turn'
    >>> ice_server.username
    '<username>'
    >>> ice_server.credential
    '<credential>'

Manage XirSys domains:

.. code-block:: python

    >>> from python_xirsys.objects import Domain
    >>> Domain.create(connection=connection, domain="test.com")
    <Domain [test.com]>
    >>> Domain.list_all(connection=connection)
    [<Domain [domain.com]>, <Domain [test.com]>]
    >>> domains = Domain.list_all(connection=connection)
    >>> domain = domains[domains.index("test.com")]
    >>> domain.applications
    [<Application [default]>, ...]
    >>> domain.disable()

Manage XirSys applications:

.. code-block:: python

    >>> from python_xirsys.objects import Application
    >>> domains = Domain.list_all(connection=connection)
    >>> domain = domains[domains.index("domain.com")]
    >>> Application.create(connection=connection, domain=domain, application="test")
    <Application [test]>
    >>> Application.list_all(connection=connection, domain=domain)
    [<Application [default]>, <Application [test]>]
    >>> Application.list_all(connection=connection, domain="domain.com")
    [<Application [default]>, <Application [test]>]
    >>> applications = Application.list_all(connection=connection, domain=domain)
    >>> application = applications[applications.index("test")]
    >>> application.rooms
    [<Room [default]>, ...]
    >>> application.disable()

Manage XirSys rooms:

.. code-block:: python

    >>> from python_xirsys.objects import Room
    >>> Room.create(connection=connection, domain="domain.com", application="default", room="test_room")
    <Room [test_room]>
    >>> rooms = Room.list_all(connection=connection, domain="domain.com", application="default")
    [<Room [default]>, <Room [test_room]>]
    >>> room = rooms[rooms.index("test_room")]
    >>> application.room()

Running the Tests
------------------

.. code-block:: bash

    pip install -r requirements/test.txt
    ./runtests.py




Changes
=======

0.1.0 (2016-05-??)
----------------------

* Initial release


