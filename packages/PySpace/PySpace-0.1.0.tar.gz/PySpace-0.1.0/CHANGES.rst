0.1.0
-----

- Release date: Not released yet
- Add GPU support through CUDA for ``BruteForceSimulator``
- Add OpenMP support to ``BarnesSimulator``. More than 2x speed up with 4 threads.
- Re-organized the C++ brute_force_update method. Gives a 2x speedup for benchmarks.
- Update private API for ``PlanetArray`` and ``Simulator`` that now allows users to change
  the underlying numpy arrays in a ``PlanetArray`` without having to make new ones.
- Print progress percentage for simulations
- Added a Makefile for easier building of extension modules.

0.0.2
-----

- Release date: 23rd March, 2016
- First public release
- A python interface for high performance C++ implementation of 
  N-body simulation algorithms.
- A numpy friendly API
- Parallel support using OpenMP
- vtk for visualization

