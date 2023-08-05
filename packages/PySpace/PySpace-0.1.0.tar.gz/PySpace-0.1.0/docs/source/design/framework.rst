=====================
The PySpace Framework
=====================

This document is an introduction to the design of PySpace. This provides high level details
on the functionality of PySpace. This should allow the user to use the module and extend it
effectively.

To understand the framework, we will work through a general N-body problem.

Here we will be using the ``BruteForceSimulator``, however the framework
is essentially the same for any ``Simulator``.

--------------
N-body problem
--------------

Consider a problem of :math:`n` bodies with mass :math:`m_i` for the :math:`i^{th}` planet. 

Equations
---------

.. math::
    :label: force    

    \vec{a_i} = \sum_{\substack{j=1 \\ j\neq i}}^{n} G \frac{m_j}{r_{ij}^3} (\vec{r_j} - \vec{r_i})


Handling collisions
~~~~~~~~~~~~~~~~~~~

From the above equation, it is clear that force will become infinite when
:math:`r_{ij} = 0`

To solve this problem we use a gravity softening method proposed by Aarseth in 1963.
Thus we change our force equation to

.. math::
    :label: softening

    \vec{a_i} = \sum_{\substack{j=1 \\ j\neq i}}^{n} G \
    \frac{m_j}{(\epsilon^2 + r_{ij}^2)^{3/2}} (\vec{r_j} - \vec{r_i})

where :math:`\epsilon` is the softening factor. By default, 
:math:`\epsilon = 0`


Numerical Integration
---------------------

``BruteForceSimulator`` uses leap frog integrator for updating velocity and positions of planets.

.. math::
    :label: position

    x_{i+1} = x_i + v_i\Delta t + \frac{1}{2}a_i\Delta t^2

.. math::
    :label: velocity

    v_{i+1} = v_i + \frac{1}{2}(a_i + a_{i+1})\Delta t


Understanding the framework
---------------------------

PySpace uses ``pyspace.planet.PlanetArray`` for storing planets.

``pyspace.planet.PlanetArray`` stores numpy arrays for :math:`x, y, z, v_x, v_y, v_z, a_x, a_y, a_z, m, r`.

.. code-block:: cython

    cdef public ndarray x
    cdef public ndarray y
    cdef public ndarray z
    cdef public ndarray v_x
    cdef public ndarray v_y
    cdef public ndarray v_z
    cdef public ndarray a_x
    cdef public ndarray a_y
    cdef public ndarray a_z
    cdef public ndarray m
    cdef public ndarray r

.. note::

    Currently ``r`` doesn't have any use per se. However, we plan to use it
    for better collision handling in the future.

``pyspace.simulator.Simulator`` stores pointers to these numpy arrays and then passes these raw pointers
to the C++ function, ``brute_force_update`` which then updates the pointers using the above numerical integration scheme.

----------
Algorithms
----------

A number of techniques for solving the N-body problem are available.
Following are currently implemented in PySpace.

Brute Force
-----------

This is implemented in ``pyspace.simulator.BruteForceSimulator`` which uses
the :math:`O(n^2)` brute force algorithm for calculating forces in a planet.

Barnes Hut
----------

This is implemented in ``pyspace.simulator.BarnesSimulator`` which uses
the :math:`O(nlogn)` barnes hut algorithm for calculating forces in a planet.

For details see `this <https://en.wikipedia.org/wiki/Barnes%E2%80%93Hut_simulation>`_ 
wikipedia article.

-------------
Visualization
-------------

PySpace dumps a vtk output of the simulations. These can then be visualized using tools such as 
Paraview, MayaVi, etc.

The vtk dump is controlled by the ``dump_output`` flag in ``Simulator::simulate``.
The vtk dump by default only dumps :math:`v_x, v_y, v_z` ie. velocities
of the planets.
For dumping custom data, use ``set_data`` in ``pyspace.simulator.Simulator``.

