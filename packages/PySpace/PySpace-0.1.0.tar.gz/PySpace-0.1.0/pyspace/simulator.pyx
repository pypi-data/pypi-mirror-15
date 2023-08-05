cimport cython
import os
import sys
from pyspace.utils import dump_vtk

cdef class Simulator:
    """Base class for all simulators"""
    def __init__(self, PlanetArray pa, double G, double dt, str sim_name = "pyspace"):
        self.planets = pa
        self.G = G
        self.dt = dt
        self.curr_time_step = 0
        self.sim_name = sim_name
        self._custom_data = False

        self.x_ptr = <double*> self.planets.x.data
        self.y_ptr = <double*> self.planets.y.data
        self.z_ptr = <double*> self.planets.z.data

        self.v_x_ptr = <double*> self.planets.v_x.data
        self.v_y_ptr = <double*> self.planets.v_y.data
        self.v_z_ptr = <double*> self.planets.v_z.data

        self.a_x_ptr = <double*> self.planets.a_x.data
        self.a_y_ptr = <double*> self.planets.a_y.data
        self.a_z_ptr = <double*> self.planets.a_z.data

        self.m_ptr = <double*> self.planets.m.data
        self.r_ptr = <double*> self.planets.r.data

        self.num_planets = pa.get_number_of_planets()

    def set_data(self, **kwargs):
        """Sets what data has to be dumped to the vtk output

        Parameters:

        **kwargs: {property name = attribute name}

        """
        self._custom_data = True
        self._data = kwargs

    cdef dict get_data(self):
        """Gets data for vtk dumps"""
        cdef dict data = {}
        if not self._custom_data:
            return data
        cdef str property_name, attribute_name
        for property_name, attribute_name in self._data.iteritems():
            data[property_name] = getattr(self.planets, attribute_name)
        return data

    cpdef reset(self):
        """Deletes all existing simulations of the same name"""
        self.curr_time_step = 0
        if os.path.isdir(self.sim_name):
            for filename in os.listdir(self.sim_name):
                if filename.endswith(".vtu"):
                    os.remove(self.sim_name + "/" + filename)

    cdef void _simulate(self, double total_time, bint dump_output = False):
        raise NotImplementedError("Simulator::_simulate called!")

    cpdef simulate(self, double total_time, bint dump_output = False):
        """Calculates position and velocity of all particles
        after time 'total_time'

        Parameters:

        total_time: double
            Total time for simulation

        dump_output: bool
            Set True if vtk dump is required

        """
        if dump_output and (not os.path.isdir(self.sim_name)):
            os.mkdir(self.sim_name)

        self._simulate(total_time, dump_output)


cdef class BarnesSimulator(Simulator):
    """Simulator using Barnes Hut algorithm"""
    def __init__(self, PlanetArray pa, double G, double dt, double theta = 1.0,
            double epsilon = 0, str sim_name = "pyspace"):
        self.theta = theta
        self.epsilon = epsilon
        Simulator.__init__(self, pa, G, dt, sim_name)

    @cython.cdivision(True)
    cdef void _simulate(self, double total_time, bint dump_output = False):

        cdef double G = self.G
        cdef double dt = self.dt

        cdef int n_steps = <int> floor(total_time/dt)
        cdef int i

        if dump_output:
            dump_vtk(self.planets, self.sim_name + str(self.curr_time_step),
                    base = self.sim_name, **self.get_data())
            self.curr_time_step += 1

        for i from 0<=i<n_steps:
            barnes_update(self.x_ptr, self.y_ptr, self.z_ptr,
                    self.v_x_ptr, self.v_y_ptr, self.v_z_ptr,
                    self.a_x_ptr, self.a_y_ptr, self.a_z_ptr,
                    self.m_ptr, G, dt, self.num_planets,
                    self.theta, self.epsilon)

            if dump_output:
                dump_vtk(self.planets, self.sim_name + str(self.curr_time_step),
                        base = self.sim_name, **self.get_data())

                self.curr_time_step += 1

            sys.stdout.write("\r%d%%" % ((i+1)*100/n_steps))
            sys.stdout.flush()


cdef class BruteForceSimulator(Simulator):
    """Simulator using Brute Force algorithm"""
    def __init__(self, PlanetArray pa, double G, double dt, double epsilon = 0,
            str sim_name = "pyspace"):
        """Constructor for BruteForceSimulator

        Parameters:

        pa: PlanetArray
            Planet array for simulation

        G: double
            Universal Gravitational constant

        dt: double
            Time step for simulation

        Notes:

        Uses brute force for simulation

        """
        Simulator.__init__(self, pa, G, dt, sim_name)
        self.epsilon = epsilon

    @cython.cdivision(True)
    cdef void _simulate(self, double total_time, bint dump_output = False):

        cdef double G = self.G
        cdef double dt = self.dt

        cdef int n_steps = <int> floor(total_time/dt)
        cdef int i

        if dump_output:
            dump_vtk(self.planets, self.sim_name + str(self.curr_time_step),
                    base = self.sim_name, **self.get_data())
            self.curr_time_step += 1

        for i from 0<=i<n_steps:
            IF USE_CUDA:
                brute_force_gpu_update(self.x_ptr, self.y_ptr, self.z_ptr,
                        self.v_x_ptr, self.v_y_ptr, self.v_z_ptr,
                        self.a_x_ptr, self.a_y_ptr, self.a_z_ptr,
                        self.m_ptr, G, dt, self.num_planets, self.epsilon)

            ELSE:
                brute_force_update(self.x_ptr, self.y_ptr, self.z_ptr,
                        self.v_x_ptr, self.v_y_ptr, self.v_z_ptr,
                        self.a_x_ptr, self.a_y_ptr, self.a_z_ptr,
                        self.m_ptr, G, dt, self.num_planets, self.epsilon)

            if dump_output:
                dump_vtk(self.planets, self.sim_name + str(self.curr_time_step),
                        base = self.sim_name, **self.get_data())

                self.curr_time_step += 1

            sys.stdout.write("\r%d%%" % ((i+1)*100/n_steps))
            sys.stdout.flush()


