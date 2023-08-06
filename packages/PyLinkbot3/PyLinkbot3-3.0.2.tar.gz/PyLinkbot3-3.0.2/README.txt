PyLinkbot3
==========

PyLinkbot - A Python package for controlling Barobo Linkbots
Contact: David Ko <david@barobo.com>

Linkbots are small modular robots designed to play an interactive role in
computer science and mathematics curricula. More information may be found at
http://www.barobo.com .

Requirements
------------

This package makes extensive use of asyncio which is only available in Python
3.5 and greater.

This package also requires protobuf>=3.0.0b2 and PySfp.

Installation
------------

The recommended way to install this package is through setuptools utilities,
such as "easy_install" or "pip". For example:

    easy_install3 PyLinkbot

or

    pip3 install PyLinkbot

Usage Options
-------------

This version of PyLinkbot3 can communicate with old SFP based baromeshd daemons
and new websockets based daemons. By default, the library will search for an
SFP based daemon located at localhost:42000. The following environment
variables control this library's behavior:

LINKBOT_USE_SFP=1 # Makes PyLinkbot use the old SFP transport instead of
                  # WebSockets.
LINKBOT_DAEMON_HOSTPORT="hostname:port" # Makes PyLinkbot use the specified
    # host:port as its daemon. For instance, if you want to use the daemon
    # running on a local linkbot-hub, set this environment variable to the
    # hostname and port of the linkbot hub.
