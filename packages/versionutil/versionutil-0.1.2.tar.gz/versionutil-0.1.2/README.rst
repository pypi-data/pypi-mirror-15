versionutil
===========

Convenience function for comparing Python system version

Installation
------------

From the project root directory::

    $ python setup.py install

Usage
-----

Provides compare_python version so that you can check against the major, minor and micro version::
    
    from versionutil import compare_python, PYTHON

    # compare_python will return a boolean value against the current system version.
    # PYTHON represents an instance of an object that is the current system version.

    # It will check at the most significant value you signify. Default is equality check.
    # True using 2.7.9:
    PYTHON == '2'
    PYTHON == '2.7'
    PYTHON == '2.7.9'
    compare_python('2')
    compare_python('2.7')
    compare_python('2.7.9')

    # True using 3.4.4:
    PYTHON == '3'
    PYTHON == '3.4'
    PYTHON == '3.4.4'
    compare_python('3')
    compare_python('3.4')
    compare_python('3.4.4')

    # False in 3.4.4:
    PYTHON != '3.5'
    PYTHON != '3.4.5'
    compare_python('3.5')
    compare_python('3.4.5')
    
    # Works with ints and even floats:
    PYTHON == 2.7
    compare_python(2.7)

    # Different comparisons exist, default comp='=='
    PYTHON != 3
    PYTHON < 3
    PYTHON < 3.0
    PYTHON > 2.6
    PYTHON >= 2.7
    PYTHON < 3.1
    compare_python(3, '!=')
    compare_python(3, '<')
    compare_python(3.0, '<')
    compare_python(2.6, '>')
    compare_python(2.7, '>=')
    compare_python(3.1, comp='<')

    # To test against a custom system version (ignore sys.version_info):
    compare_python(5.4, sysv=(5, 4, 5))
    # or to create a PYTHON like object for 5.4.5:
    from versionutil import PythonVersion
    pv545 = PythonVersion(sysv=(5, 4, 5))
    if pv545 == 5.4: # True...

    # Useful for handling imports, where otherwise pyfuture and pasteurize might not have what you need.
    if PYTHON < 3:
        from oldapi import OldAPI as API
    elif PYTHON == 3.0 or PYTHON == 3.1:
        from newapi import OtherAPI as API
    elif PYTHON >= 3.2:
        from newapi import NewAPI as API

Release Notes
-------------

:0.1.2:
    Check is_instance(str) for 3.4 and basestring for <
:0.1.1:
    Added PYTHON global and PythonVersion class for easier usage (PYTHON < 2.7)
:0.1.0:
    Alpha finished, tested fully with tox
:0.0.1:
    Project created
