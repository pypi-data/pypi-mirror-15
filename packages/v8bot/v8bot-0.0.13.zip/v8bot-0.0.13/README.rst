V8Bot
=====

V8Bot gives you the ability to script chat bots for Hitbox.tv in JavaScript using the V8 engine by Google.

Prerequisits
------------

``V8Bot`` uses the ``PyV8`` package, you can download it here: https://code.google.com/archive/p/pyv8/downloads

Linux Installation
------------------

The installation via ``pip`` seems currently broken, so you have to build and install PyV8 manually :(
But is not so hard, on Debian follow these steps:

    # apt-get install subversion scons libboost-all-dev libboost-python-dev
    $ svn checkout http://v8.googlecode.com/svn/trunk/ v8
    $ svn checkout http://pyv8.googlecode.com/svn/trunk/ pyv8
    $ cd v8
    $ export V8_HOME=`pwd`
    $ cd ../pyv8
    $ python setup.py build

Now, if you want to install ``V8Bot`` as system wide side package

    # python setup.py install

Or if you using ``virtualenv``

    $ virtualenv venv
    $ . venv/bin/activate
    $ python setup.py install

If you using Debian lenny you also can use a binary distribution from me built for x64 with ``libboost v1.55.0.2``.
You find it here: https://v8bot.ewelt.net/dist/pyv8/

Now download the ``V8Bot`` source files and install it using ``setup.py`` as usual.

    # python setup.py install

Windows Installation
--------------------

**From source**

Download the ``PyV8`` installer for your architecture from here: https://code.google.com/archive/p/pyv8/downloads
and install it.

Download the ``V8Bot`` source from here https://v8bot.ewelt.net/dist/ and install it using ``setup.py`` or use the provided ``msi`` installer.

**Standalone builds from Py2Exe**

On https://v8bot.ewelt.net/dist/ you can also find standalone builds generated with ``Py2Exe``

Usage
-----

To start a bot instance type

    $ v8b -u username -p password -c channel script_file.js

Where ``username`` and ``password`` are the Hitbox.tv credentials the bot should use. Its no problem to use your own credentials,
the bot will then have your nickname. You can let him join the same channels you are in, there is no duplicate check or something.
