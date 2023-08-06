Sanitize a variable name
----------------------------

The :py:func:`.sanitize_python_var_name()` function replace invalid character(s) 
for a python variable.

.. code-block:: python
    :caption: Sample code
    
    import pathvalidate

    print(pathvalidate.sanitize_python_var_name("a*b:c<d>e%f(g)h+i_0.txt"))

.. code-block:: none
    :caption: Output
    
    abcdefghi_0txt
