How to compile fortran code to use it in Python
===============================================
.. code-block:: shell

    f2py -c -m mc ziggurat.f90 mc.f90
    
    docker build -t probe-mc-analytic-er:0.0.0 .
