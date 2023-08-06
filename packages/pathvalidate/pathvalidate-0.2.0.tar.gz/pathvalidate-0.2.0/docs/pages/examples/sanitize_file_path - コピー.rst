Sanitize a file path
----------------------------

The :py:func:`.sanitize_filename()` function replace invalid character(s) 
for a filename within a file name.

.. code-block:: python
    :caption: Sample code
    
    import pathvalidate

    filename = "a*b:c<d>e%f(g)h+i_0.txt"
    print(pathvalidate.sanitize_filename(filename))

.. code-block:: none
    :caption: Output
    
    abcde%f(g)h+i_0.txt

