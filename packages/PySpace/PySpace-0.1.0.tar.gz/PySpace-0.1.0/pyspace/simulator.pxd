from libcpp.vector cimport vector
from libc.math cimport floor
from pyspace.planet cimport PlanetArray

cdef extern from "numpy/arrayobject.h":
    ctypedef int intp
    ctypedef extern class numpy.ndarray [object PyArrayObject]:
        cdef char *data
        cdef int nd
        cdef intp *dimensions
        cdef intp *strides
        cdef int flags

cdef extern from "pyspace.h":
    cdef void brute_force_update(double*, double*, double*,
            double*, double*, double*,
            double*, double*, double*,
            double*, double, double, int, double) nogil

    cdef void brute_force_gpu_update(double*, double*, double*,
            double*, double*, double*,
            double*, double*, double*,
            double*, double, double, int, double) nogil

    cdef void barnes_update(double*, double*, double*,
            double*, double*, double*,
            double*, double*, double*,
            double*, double, double, int,
            double, double) nogil

cdef class Simulator:
    cdef PlanetArray planets

    cdef double G
    cdef double dt
    cdef str sim_name
    cdef int num_planets
    cdef int curr_time_step

    cdef bint _custom_data
    cdef dict _data

    cdef double* x_ptr
    cdef double* y_ptr
    cdef double* z_ptr

    cdef double* v_x_ptr
    cdef double* v_y_ptr
    cdef double* v_z_ptr

    cdef double* a_x_ptr
    cdef double* a_y_ptr
    cdef double* a_z_ptr

    cdef double* m_ptr
    cdef double* r_ptr

    cpdef simulate(self, double total_time, bint dump_output = *)
    cdef dict get_data(self)

    cdef void _simulate(self, double total_time, bint dump_output = *)

    cpdef simulate(self, double total_time, bint dump_output = *)
    cpdef reset(self)

cdef class BruteForceSimulator(Simulator):
    cdef double epsilon

    cdef void _simulate(self, double total_time, bint dump_output = *)

cdef class BarnesSimulator(Simulator):
    cdef double theta
    cdef double epsilon

    cdef void _simulate(self, double total_time, bint dump_output = *)

