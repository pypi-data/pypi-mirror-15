
===================
Package Dependency
===================


.. contents::

Validates package requirements

Requirements
--------------

* Python:

  - termcolor == 1.1.0

Installation
--------------

The last stable release is available on PyPI and can be installed with ``pip``

::
	
    $ pip install pkgdependency


Example
------------

Using Function

::

    from pkgdependency import verify_dependency
    verify_dependency(path/to/requirements)


Using Command

::

    $ pkgdep path/to/requirements


Example of a case in which the requirements are not met

::

    >>> VERSION CONFLICT: examplepkg(1.0.0) => (2.0)
    >>> NOT FOUND: examplepkg(any)


Create requirement text

::

    $ my_project $ tree requirements/
    /requirements/
    ├── base.txt
    ├── local.txt
    └── server.txt

Create base requirement

::

    $ pip freeze > base.txt


Create environment requirement

::

    -r base.txt
    pytest==2.7.0
    
Copyright
------------

Copyright - Copyright (C) 2016 gumi Inc.    
    
