.. image:: https://travis-ci.org/GreatFruitOmsk/qrc_pathlib.svg?branch=master

qrc_pathlib
===========

`Qt Resource System <http://doc.qt.io/qt-5/resources.html>`_ allows to store files
inside binaries and read them by using Qt's file system abstraction (QFile, QDir etc).

This package extends `pathlib <https://docs.python.org/3/library/pathlib.html>`_ introduced in Python 3.4
by implementing ``Path`` and ``PurePath`` for QRS:

.. code-block:: python

    from qrc_pathlib import QrcPath
    
    QrcPath(':my_resource.svg').read_bytes()
    
    with QrcPath(':hello.txt').open() as f:
        print(f.read())

Since QRS is read-only all methods that are supposed to modify files raise ``PermissionError``. Other inapplicable methods
such as ``stat`` will raise ``NotImplementedError``.
