============
Installation
============

------------
Dependencies
------------

- Numpy
- PyEVTK (``pip install pyevtk``)
- gcc compiler
- OpenMP (optional)
- ParaView / MayaVi or any other vtk rendering tool (optional)

-------------
Linux and OSX
-------------

To install the latest stable version, run::
    
    $ pip install pyspace

To install development version, clone this repository by:: 

    $ git clone https://github.com/adityapb/pyspace.git

To install, run::

    $ python setup.py install

To install without OpenMP, set ``USE_OPENMP`` environment variable
to 0 and then install::

    $ export USE_OPENMP=0 
    $ python setup.py install

To install without GPU support, set ``USE_CUDA`` environment variable
to 0 and then install::

    $ export USE_CUDA=0
    $ python setup.py install
 
Troubleshooting
---------------

If you run into any issues regarding installation or otherwise, please report
`here <https://github.com/adityapb/pyspace/issues>`_.

Some common issues are addressed below

CUDA not found
~~~~~~~~~~~~~~

Make sure if the CUDA toolkit is installed. If you still get this message after installation,
follow the instructions given below.

Add CUDA it to ``PATH`` environmental variable and try again

Or, set ``CUDAHOME`` environmental variable to path of the CUDA installation by::

    $ export CUDAHOME=/usr/local/cuda

Image not found
~~~~~~~~~~~~~~~

If your code compiles and you get this error at runtime, make sure you have a CUDA
compatible device installed.

If you don't, install without GPU support (see Installation)
 
**PySpace doesn't support Windows currently**

-----------------
Running the tests
-----------------

For running the tests you will need to install ``nose``, install using::

    $ pip install nose

To run the tests, from project's root directory run::
    
    $ make test

----------------------
Running the benchmarks
----------------------

For running benchmarks you will need to install ``pandas``, install using::

    $ pip install pandas

To run the benchmarks, cd to benchmarks directory and run::

    $ python run_benchmarks.py

