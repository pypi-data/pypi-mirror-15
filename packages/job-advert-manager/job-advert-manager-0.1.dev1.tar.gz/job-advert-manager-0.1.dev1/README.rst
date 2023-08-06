=====================
`Job Advert Manager`_
=====================

Copyright (c) 2015 Jeremie DECOCK (http://www.jdhp.org)


* Web site: http://www.jdhp.org/projects_en.html
* Source code: https://github.com/jeremiedecock/job-advert-manager
* Issue tracker: https://github.com/jeremiedecock/job-advert-manager/issues


Description
===========

`Job Advert Manager`_ is an open source tool to manage job adverts for job
seekers.

Note:

    This project is still in beta stage.


Dependencies
============

- Python >= 3.0
- GTK+3 with Python 3 bindings
- Matplotlib


.. _install:

Installation
============

Gnu/Linux
---------

You can install, upgrade, uninstall Job Advert Manager with these commands (in a
terminal)::

    pip install --pre job-advert-manager
    pip install --upgrade job-advert-manager
    pip uninstall job-advert-manager

Or, if you have downloaded the Job Advert Manager source code::

    python3 setup.py install

.. There's also a package for Debian/Ubuntu::
.. 
..     sudo apt-get install job-advert-manager

Windows
-------

.. Note:
.. 
..     The following installation procedure has been tested to work with Python
..     3.4 under Windows 7.
..     It should also work with recent Windows systems.

You can install, upgrade, uninstall Job Advert Manager with these commands (in a
`command prompt`_)::

    py -m pip install --pre job-advert-manager
    py -m pip install --upgrade job-advert-manager
    py -m pip uninstall job-advert-manager

Or, if you have downloaded the Job Advert Manager source code::

    py setup.py install

MacOSX
-------

Note:

    The following installation procedure has been tested to work with Python
    3.5 under MacOSX 10.9 (*Mavericks*).
    It should also work with more recent MacOSX systems.

You can install, upgrade, uninstall Job Advert Manager with these commands (in a
terminal)::

    pip install --pre job-advert-manager
    pip install --upgrade job-advert-manager
    pip uninstall job-advert-manager

Or, if you have downloaded the Job Advert Manager source code::

    python3 setup.py install

Job Advert Manager requires GTK+3 and its Python 3 bindings plus few additional
libraries to run.
These dependencies can be installed using MacPorts::

    port install gtk3
    port install py35-gobject3
    port install py35-matplotlib

.. or with Hombrew::
.. 
..     brew install gtk+3
..     brew install pygobject3


Bug reports
===========

To search for bugs or report them, please use the Job Advert Manager Bug Tracker at:

    https://github.com/jeremiedecock/job-advert-manager/issues




License
=======

This project is provided under the terms and conditions of the
`MIT License`_.


.. _MIT License: http://opensource.org/licenses/MIT
.. _Job Advert Manager: https://github.com/jeremiedecock/job-advert-manager
