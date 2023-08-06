Black Box Recorder
==================

:author: Laurent Pointal <laurent.pointal@limsi.fr> <laurent.pointal@laposte.net>
:organization: CNRS - LIMSI
:copyright: CNRS - 2015-2016
:license: New BSD License
:version: 1.0.2


`Module documentation <http://bbrecorder.readthedocs.org/>`_

`Subversion repository & bug tracking <https://sourcesup.renater.fr/scm/viewvc.php?root=bbrecorder>`_
(on french academic SourceSup site).

`Developer page <https://perso.limsi.fr/pointal/dev:bbrecorder>`_

What is it?
-----------

A simple module providing a logging handler to manage caching of last N log records
until they are needed — and then generate them using standard common Python logging
handlers.

Installation
------------

Unless someone built a package for your OS distro, the simplest procedure
is to use ``pip`` to install the module:

    pip install bbrecorder

If you have no admin access to install things on you computer, you may install
a virtualenv and run pip inside this virtual env, or you can do a local user
installation:

    pip install --user bbrecorder

