How to compile fortran code to use it in Python
===============================================
.. code-block:: shell

    f2py -c -m mc ziggurat.f90 mc.f90

Docker build
============
.. code-block:: shell

    docker build -t probe-mc-analytic-er:0.0.0 .



Na novym virtualu
=================
.. code-block:: shell

    apt-get update && apt-get -y install tmux htop
    docker pull ziky5/probe-mc-analytic-er:0.0.0
    cd /root
    tmux
    docker run --rm -it -v ${PWD}:/data ziky5/probe-mc-analytic-er:0.0.0 bash
    cd /data && mc.py 2 100 1000 2>&1 | tee _log