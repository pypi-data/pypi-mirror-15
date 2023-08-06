.. image:: https://raw.githubusercontent.com/HackEdit/hackedit/master/docs/_static/banner.png

|

.. image:: https://img.shields.io/pypi/v/hackedit.svg
   :target: https://pypi.python.org/pypi/hackedit/
   :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/dm/hackedit.svg
   :target: https://pypi.python.org/pypi/hackedit/
   :alt: Number of PyPI downloads

.. image:: https://img.shields.io/pypi/l/hackedit.svg


.. image:: https://travis-ci.org/HackEdit/hackedit.svg?branch=master
   :target: https://travis-ci.org/HackEdit/hackedit
   :alt: Travis-CI Build Status

.. image:: https://ci.appveyor.com/api/projects/status/ncjwicmi79ljvuyg?svg=true
    :target: https://ci.appveyor.com/project/ColinDuquesnoy/hackedit
    :alt: Appveyor Build Status


.. image:: https://coveralls.io/repos/HackEdit/hackedit/badge.svg?branch=master&service=github
  :target: https://coveralls.io/github/HackEdit/hackedit?branch=master
  :alt: API Coverage

.. image:: https://www.quantifiedcode.com/api/v1/project/a24d2603c5914cd389686da2799ac4da/badge.svg
  :target: https://www.quantifiedcode.com/app/project/a24d2603c5914cd389686da2799ac4da
  :alt: Code issues

|

.. image:: https://badges.gitter.im/Join%20Chat.svg
   :alt: Join the chat at https://gitter.im/HackEdit/hackedit
   :target: https://gitter.im/HackEdit/hackedit?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge

|

- `About`_
- `Status`_
- `Resources`_
- `License`_
- `Features`_
- `Dependencies`_
- `Plugins`_
- `Installation`_

  * `GNU/Linux`_
  * `Windows`_
  * `OS X`_

.. _About: https://github.com/HackEdit/hackedit#about
.. _Status: https://github.com/HackEdit/hackedit#status
.. _Resources: https://github.com/HackEdit/hackedit#resources
.. _Features: https://github.com/HackEdit/hackedit#features
.. _License: https://github.com/HackEdit/hackedit#license
.. _Installation: https://github.com/HackEdit/hackedit#installation
.. _GNU/Linux: https://github.com/HackEdit/hackedit#linux
.. _Windows: https://github.com/HackEdit/hackedit#windows
.. _OS X: https://github.com/HackEdit/hackedit#osx
.. _Plugins: https://github.com/HackEdit/hackedit#plugins

About
=====

The hackable IDE, built with `Python3`_, `PyQt5`_ and `pyQode`_.

HackEdit is an open platform to build an Integrated Development Environment.

This repository contains the core application which setups a basic IDE with a
plugin infrastructure and an API that you can use to enhance the application
and make it a full stack IDE for a particular technology.

The name stands from *Hackable Editor*, but there is another meaning: once
you've contributed to the project or made your own plugin, you can say that
you've *hacked it*.

**Note that the core application is actually pretty dumb, you need to install
some** `Plugins`_ **to make something out of HackEdit!**

Status
======

HackEdit is in **ALPHA**. Expects to find bugs and features not implemented.

At the moment there is **no user manual**, **no documentation**,
**no Windows installer**, **no linux packages**.

All those will come with future releases.

The **API** is **not** considered **stable** and we don't recommend to hack in
HackEdit. It's probably better to wait for the beta release, at that point,
there will be more resources available.

For now, just give it a try and **report** any issue you encountered, give your
**feedback** and submit any **idea** that you have.

You can discuss about HackEdit on `Gitter`_.

.. _Gitter: https://gitter.im/HackEdit/hackedit

Resources
=========

- `Homepage`_
- `Issue tracker`_
- `Changelog`_
- `Roadmap`_
- `Screenshots`_

.. _Homepage: https://github.com/HackEdit/hackedit
.. _Issue tracker: https://github.com/HackEdit/hackedit/issues
.. _Changelog: https://github.com/HackEdit/hackedit/blob/master/docs/changelog.rst
.. _Roadmap: https://github.com/HackEdit/hackedit/wiki/Roadmap
.. _Screenshots: https://github.com/HackEdit/hackedit/wiki/Screenshots

License
=======

HackEdit is released under the GPL version 2.

We are using the `Hack`_ font which is licensed under the Hack Open Font
License v2.0 and the Bitstream Vera License and the `Breeze`_ icon theme,
licensed under the LGPL.

Features
========

The core application provides the following features:

- cross platform: works on Linux, OS X and Windows
- coded in 100% pure Python, using the PyQt GUI toolkit
- plugin architecture with customisable workspaces: you can choose exactly what
  plugins to use for a specific project
- multi-window IDE with multiple undo stack
- splittable editor tabs
- supports multiple programming languages through plugins (at the momement we
  have support for Python and COBOL)
- configurable interface (custom shortcuts, native theme or dark theme,...)
- a clean and simple high level API for interacting with the IDE
- core plugins included: find/search in directories, editor outline view,
  simple terminal widget for running commands, open documents view,
  image viewer


Dependencies
============

**Main dependencies**:

- `Python3`_ (>= 3.4)
- `PyQt5`_
- `setuptools`_ and `pip`_ (might be included with your python installation).

**Optional dependencies**:

- `babel`_  (to see translated language name instead of the language code in the application preferences)
- `PyGObject`_ and `libnotify`_ on GNU/Linux for nicer notifications on gtk based desktops.


The following dependencies are `bundled`_ with the hackedit package:

- `pyqode.qt`_
- `pyqode.core`_
- `pyqode.cobol`_
- `pyqode.python`_
- `pyqode.rst`_
- `pyqode.json`_
- `pygments`_
- `future`_
- `pep8`_
- `pyflakes`_
- `jedi`_
- `qdarkstyle`_
- `restructuredtext_lint`_

.. _bundled: https://github.com/HackEdit/hackedit/tree/master/hackedit/vendor

Plugins
=======

Plugins are regular python packages that install one or more setuptools entry-points.

You can install plugins for HackEdit either by using the builtin plugin manager
interface or by using the python package manager: `pip`_.

Here is the list of official plugins (made by the core team):

- `hackedit-python`_: Python support (python2 and python3 are supported)
- `hackedit-cobol`_: COBOL support

*Note: the plugin manager interface has not been implemented yet, you need to use pip to install the plugins*

Here is how you can install the official plugins::

    pip3 install hackedit-python hackedit-cobol


Installation
============

General instructions:
---------------------


Install the following dependencies using your favorite package manager:

- Python 3
- pip (the python package manager) for Python3
- PyQt5 for python3  .


Use pip to install ``hackedit`` and its python dependencies::

      pip3 install hackedit --pre --upgrade


To install the latest development version, run the following command instead::

      pip3 install git+https://github.com/HackEdit/hackedit.git --upgrade

Once you've installed the core application, you will want to install some
`Plugins`_.

Linux
-----

Ubuntu/Debian
~~~~~~~~~~~~~

1. Install pip, setuptools and pyqt5::

    sudo apt-get install python3-setuptools python3-pip python3-pyqt5 python3-pyqt5.qtsvg git

2. Install optional dependencies (for nicer notifications on Gnome Shell 3.x/Unity)::

    sudo apt-get install python3-gi libnotify-dev

3. Install hackedit::

    sudo pip3 install hackedit --pre --upgrade --install-option="--install-layout=deb"

4. If you're using a gtk based desktop, update the gtk icon cache::

    sudo gtk-update-icon-cache /usr/share/icons/hicolor/

5. Run hackedit::

    hackedit


ArchLinux
~~~~~~~~~

1. Install pip, setuptools and pyqt5 using pacman::

    sudo pacman -S python-pyqt5 python-pip python-setuptools qt5-svg git

2. Install optional dependencies (for nicer notification on Gnome Shell 3.x)::

    sudo pacman -S libnotify python-gobject

3. Install hackedit::

    sudo pip3 install hackedit --pre --upgrade

4. If you're using a gtk based desktop, update the gtk icon cache::

    sudo gtk-update-icon-cache /usr/share/icons/hicolor/

5. Run hackedit::

    hackedit

Windows
-------

1. Install `Python 3.4`_

2. Install `PyQt5 for Python 3.4`_

3. Open a command line prompt and run the following commands:

* Install hackedit using pip::

    pip install hackedit --pre --upgrade

* Run hackedit in GUI mode::

    hackedit

* Or, run hackedit in console mode::

    hackedit-console

*Note: In the future, there will be a windows installer with a native launcher that your can pin to you taskbar.*


OSX
---

1. Install `Homebrew`_

2. Install Python3 and PyQt5 using::

    brew install pyqt5 --with-python3

3. Install hackedit::

    pip3 install hackedit --pre --upgrade

4. Run hackedit from the terminal::

    hackedit

*Note: in the future, you will have a native launcher that you can keep in your dock.*

.. links section:

.. _github: https://github.com/HackEdit/hackedit
.. _hackedit-cobol: https://github.com/HackEdit/hackedit-cobol
.. _hackedit-python: https://github.com/HackEdit/hackedit-python

.. _Homebrew: http://brew.sh/

.. _Python3: https://www.python.org/
.. _PyQt5: http://www.riverbankcomputing.com/software/pyqt/download5
.. _setuptools: https://pypi.python.org/pypi/setuptools
.. _pip: https://pypi.python.org/pypi/pip

.. _pyQode: https://github.com/pyQode/pyQode
.. _pyqode.qt: https://github.com/pyQode/pyqode.qt
.. _pyqode.core: https://github.com/pyQode/pyqode.core
.. _pyqode.python: https://github.com/pyQode/pyqode.python
.. _pyqode.cobol: https://github.com/pyQode/pyqode.cobol
.. _pyqode.rst: https://github.com/pyQode/pyqode.rst
.. _pyqode.json: https://github.com/pyQode/pyqode.json

.. _pygments: https://pypi.python.org/pypi/pygments
.. _future: https://pypi.python.org/pypi/future
.. _pep8: https://pypi.python.org/pypi/pep8
.. _pyflakes: https://pypi.python.org/pypi/pyflakes
.. _jedi: https://pypi.python.org/pypi/jedi
.. _boss: https://pypi.python.org/pypi/boss
.. _cement: https://pypi.python.org/pypi/cement
.. _qdarkstyle: https://pypi.python.org/pypi/cement
.. _restructuredtext_lint: https://pypi.python.org/pypi/restructuredtext_lint
.. _git: https://git-scm.com/
.. _Python 3.4: https://www.python.org/ftp/python/3.4.3/python-3.4.3.msi
.. _PyQt5 for Python 3.4: http://downloads.sourceforge.net/project/pyqt/PyQt5/PyQt-5.5.1/PyQt5-5.5.1-gpl-Py3.4-Qt5.5.1-x32.exe?r=&ts=1446908240&use_mirror=heanet
.. _Git for Windows: https://git-scm.com/download/win
.. _PyGObject: https://wiki.gnome.org/Projects/PyGObject
.. _libnotify: http://www.linuxfromscratch.org/blfs/view/svn/x/libnotify.html
.. _babel: https://github.com/python-babel/babel


.. _Hack: https://github.com/chrissimpkins/Hack
.. _Breeze: https://github.com/NitruxSA/breeze-icon-theme
