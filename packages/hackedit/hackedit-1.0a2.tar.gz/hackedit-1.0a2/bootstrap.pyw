#!/usr/bin/env python3
"""
The bootstrap script lets you run HackEdit from source checkout:

1) patch sys.path with the vendor package that contains most external libraries


Before running this script, you should:

1) install python3 and pyqt5 using your package manager (or the installer
   files for your platform)

2) install hackedit as an editable package::

       (sudo) pip3 install -e

   This is needed so that the plugin entrypoints are written to
   hackedit.egg-info/

3) install additional plugins (e.g. hackedit-cobol, hackedit-python) as
   editable packages (pip3 install -e .)

4) run the script: python3 bootstrap.pyw

"""
import glob
import os
import os.path as osp
import sys


# --------- bootstrapping HackEdit
print("Executing HackEdit from source checkout")

# ------ patching sys.path
DEVPATH = osp.dirname(osp.abspath(__file__))
sys.path.insert(0, DEVPATH)

print("01. Patched sys.path with %r" % DEVPATH)

# ------ check if python setup.py develop has been executed
if len(glob.glob('*.egg-info')) == 0:
    print('Please run ``(sudo) pip3 install -e .`` to install all dependencies and plugins...')

# ------ check PyQt5
try:
    from PyQt5.QtCore import PYQT_VERSION_STR
    from PyQt5.QtCore import QT_VERSION_STR
    from PyQt5.QtGui import QIcon
except ImportError:
    print('02. Failed to import PyQt5, package not found.')
    sys.exit(1)
else:
    print('02. Imported PyQt5')
    print('    [Qt %s, PyQt5 %s]' % (QT_VERSION_STR, PYQT_VERSION_STR))
    icons_path = os.path.join(sys.prefix, 'share', 'hackedit', 'icons')
    if 'linux' not in sys.platform.lower() and not os.path.exists(icons_path):
        paths = QIcon.themeSearchPaths()
        paths.append('data/resources/icons')
        QIcon.setThemeSearchPaths(paths)


# ------ run the application
try:
    from hackedit.main import main
    from hackedit.app import versions
except ImportError:
    print('03. Failed to import hackedit')
else:
    all_versions = versions.get_versions()
    print("03. Imported HackEdit %s (%s)" % (
        all_versions['hackedit'], versions.get_vcs_revision()))
    print("    [Python %s %dbits, on %s]" % (
        all_versions['python'], all_versions['bitness'],
        all_versions['system']))
    main()
