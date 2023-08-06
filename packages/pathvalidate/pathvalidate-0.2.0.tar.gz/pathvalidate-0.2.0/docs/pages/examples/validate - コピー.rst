Filename validation
----------------------------

The :py:func:`.validate_filename()` function will raise ``ValueError`` if
the filename includes invalid character(s) for a filename.

.. code-block:: python
    :caption: Sample code
    
    import pathvalidate

    filename = "a*b:c<d>e%f(g)h+i_0.txt"
    try:
        pathvalidate.validate_filename(filename)
    except ValueError:
        print("invalid filename!")

.. code-block:: none
    :caption: Output
    
    invalid filename!
