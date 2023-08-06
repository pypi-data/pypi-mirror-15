Home-page: https://github.com/thombashi/pathvalidate
Author: Tsuyoshi Hombashi
Author-email: gogogo.vm@gmail.com
License: MIT License
Description: pathvalidate
        =============
        
        .. image:: https://img.shields.io/pypi/pyversions/pathvalidate.svg
            :target: https://pypi.python.org/pypi/pathvalidate
        .. image:: https://travis-ci.org/thombashi/pathvalidate.svg?branch=master
            :target: https://travis-ci.org/thombashi/pathvalidate
        .. image:: https://coveralls.io/repos/github/thombashi/pathvalidate/badge.svg?branch=master
            :target: https://coveralls.io/github/thombashi/pathvalidate?branch=master
        
        Summary
        -------
        
        pathvalidate is a python library to validate/sanitize a string such as filename/variable-name.
        
        Examples
        ========
        
        Filename validation
        ----------------------------
        
        .. code:: python
        
            import pathvalidate
        
            filename = "a*b:c<d>e%f(g)h+i_0.txt"
            try:
                pathvalidate.validate_filename(filename)
            except ValueError:
                print("invalid filename!")
        
        .. code::
        
            invalid filename!
        
        Sanitize a file path
        ----------------------------
        
        .. code:: python
        
            import pathvalidate
        
            filename = "a*b:c<d>e%f(g)h+i_0.txt"
            print(pathvalidate.sanitize_filename(filename))
        
        .. code::
        
            abcde%f(g)h+i_0.txt
        
        
        For more information
        --------------------
        More examples are available at 
        http://pathvalidate.readthedocs.org/en/latest/pages/examples/index.html
        
        
        Installation
        ============
        
        ::
        
            pip install pathvalidate
        
        
        Dependencies
        ============
        
        Python 2.6+ or 3.3+
        
        - `DataPropery <https://github.com/thombashi/DataProperty>`__
        
        
        Test dependencies
        -----------------
        
        - `pytest <http://pytest.org/latest/>`__
        - `pytest-runner <https://pypi.python.org/pypi/pytest-runner>`__
        - `tox <https://testrun.org/tox/latest/>`__
        
        Documentation
        =============
        
        http://pathvalidate.readthedocs.org/en/latest/
        
        
Keywords: path,validation
Platform: UNKNOWN
Classifier: Development Status :: 4 - Beta
Classifier: Intended Audience :: Developers
Classifier: License :: OSI Approved :: MIT License
Classifier: Operating System :: Microsoft :: Windows
Classifier: Operating System :: POSIX
Classifier: Operating System :: POSIX :: Linux
Classifier: Programming Language :: Python :: 2
Classifier: Programming Language :: Python :: 2.6
Classifier: Programming Language :: Python :: 2.7
Classifier: Programming Language :: Python :: 3
Classifier: Programming Language :: Python :: 3.3
Classifier: Programming Language :: Python :: 3.4
Classifier: Programming Language :: Python :: 3.5
Classifier: Topic :: Software Development :: Libraries
Classifier: Topic :: Software Development :: Libraries :: Python Modules
