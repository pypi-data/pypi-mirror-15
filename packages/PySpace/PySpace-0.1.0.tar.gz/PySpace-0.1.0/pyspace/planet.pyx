import numpy as np
cimport numpy as np
cimport cython
from libc.math cimport sqrt

cdef class PlanetArray:
    """PlanetArray for storing planets"""
    def __init__(self, ndarray x, ndarray y, ndarray z,
            ndarray v_x = None, ndarray v_y = None,  ndarray v_z = None,
            ndarray m = None, ndarray r = None):
        """Constructor for PlanetArray

        Parameters:

        x: np.ndarray
            'x' coordinates of planets

        y: np.ndarray
            'y' coordinates of planets

        z: np.ndarray
            'z' coordinates of planets

        v_x: np.ndarray
            'x' components of initial velocity
            Default value: 0

        v_y: np.ndarray
            'y' components of initial velocity
            Default value: 0

        v_z: np.ndarray
            'z' components of initial velocity
            Default value: 0

        m: np.ndarray
            Mass of planets
            Default value: 1

        r: np.ndarray
            Radius of planets
            Default value: 1

        """
        self.x = x.astype(np.float64)
        self.y = y.astype(np.float64)
        self.z = z.astype(np.float64)

        cdef int num_planets = self.get_number_of_planets()

        if v_x is None:
            self.v_x = np.zeros(num_planets)
        else:
            self.v_x = v_x.astype(np.float64)

        if v_y is None:
            self.v_y = np.zeros(num_planets)
        else:
            self.v_y = v_y.astype(np.float64)

        if v_z is None:
            self.v_z = np.zeros(num_planets)
        else:
            self.v_y = v_y.astype(np.float64)

        if m is None:
            self.m = np.ones(num_planets)
        else:
            self.m = m.astype(np.float64)

        if r is None:
            self.r = np.ones(num_planets)
        else:
            self.r = r.astype(np.float64)

        self.a_x = np.zeros(num_planets)
        self.a_y = np.zeros(num_planets)
        self.a_z = np.zeros(num_planets)

    cpdef concatenate(self, PlanetArray other):
        """Concatenates 'other' PlanetArray to self"""
        self.x = np.concatenate([self.x, other.x])
        self.y = np.concatenate([self.y, other.y])
        self.z = np.concatenate([self.z, other.z])

        self.v_x = np.concatenate([self.v_x, other.v_x])
        self.v_y = np.concatenate([self.v_y, other.v_y])
        self.v_z = np.concatenate([self.v_z, other.v_z])

        self.a_x = np.concatenate([self.a_x, other.a_x])
        self.a_y = np.concatenate([self.a_y, other.a_y])
        self.a_z = np.concatenate([self.a_z, other.a_z])

        self.m = np.concatenate([self.m, other.m])
        self.r = np.concatenate([self.r, other.r])

    cpdef int get_number_of_planets(self):
        """Returns number of planets in the PlanetArray

        Parameters:

        None

        Returns:

        int: Number of planets in PlanetArray

        """
        return self.x.size

    cpdef double dist(self, int i, int j):
        """Distance between planet 'i' and planet 'j'

        Parameters:

        i, j: int
            Indices of planets whose distance is sought.

        """
        cdef double* x_ptr = <double*> self.x.data
        cdef double* y_ptr = <double*> self.y.data
        cdef double* z_ptr = <double*> self.z.data

        return sqrt(
                (x_ptr[i] - x_ptr[j])**2 + \
                (y_ptr[i] - y_ptr[j])**2 + \
                (z_ptr[i] - z_ptr[j])**2
                )

    @cython.cdivision(True)
    cpdef double potential_energy_planet(self, double G, int i):
        """Returns potential energy of planet 'i'

        Parameters:

        G: double
            Universal Gravitational constant

        i: int
            Index of the particle whose potential energy is sought

        """
        cdef double* m_ptr = <double*> self.m.data

        cdef double pot_energy = 0
        cdef int num_planets = self.get_number_of_planets()
        cdef int j

        for j from 0<=j<num_planets:
            if i!=j:
                pot_energy += -G*m_ptr[i]*m_ptr[j]/self.dist(i,j)

        return pot_energy

    cpdef double kinetic_energy_planet(self, int i):
        """Returns kinetic energy of planet 'j'"""
        cdef double* m_ptr = <double*> self.m.data
        cdef double* v_x_ptr = <double*> self.v_x.data
        cdef double* v_y_ptr = <double*> self.v_y.data
        cdef double* v_z_ptr = <double*> self.v_z.data

        return 0.5*m_ptr[i]*(v_x_ptr[i]**2 + v_y_ptr[i]**2 + v_z_ptr[i]**2)

    @cython.cdivision(True)
    cpdef double potential_energy(self, double G):
        """Returns total potential energy of PlanetArray"""
        cdef double tot_pot_energy = 0
        cdef int num_planets = self.get_number_of_planets()
        cdef int i

        for i from 0<=i<num_planets:
            tot_pot_energy += self.potential_energy_planet(G,i)

        return tot_pot_energy/2

    cpdef double kinetic_energy(self):
        """Returns total kinetic energy of PlanetArray"""
        cdef double tot_kin_energy = 0
        cdef int num_planets = self.get_number_of_planets()
        cdef int i

        for i from 0<=i<num_planets:
            tot_kin_energy += self.kinetic_energy_planet(i)

        return tot_kin_energy

    cpdef double total_energy_planet(self, double G, int i):
        """Returns total energy of planet 'i'"""
        return self.potential_energy_planet(G,i) + self.kinetic_energy_planet(i)

    cpdef double total_energy(self, double G):
        """Returns total energy of PlanetArray"""
        return self.potential_energy(G) + self.kinetic_energy()

    @cython.cdivision(True)
    cpdef tuple com(self):
        """Return centre of mass of the system of planets"""
        cdef double* x_ptr = <double*> self.x.data
        cdef double* y_ptr = <double*> self.y.data
        cdef double* z_ptr = <double*> self.z.data
        cdef double* m_ptr = <double*> self.m.data

        cdef double com_x = 0
        cdef double com_y = 0
        cdef double com_z = 0
        cdef double m_tot = 0

        cdef int num_planets = self.get_number_of_planets()

        cdef int i
        for i from 0<=i<num_planets:
            com_x += x_ptr[i]*m_ptr[i]
            com_y += y_ptr[i]*m_ptr[i]
            com_z += z_ptr[i]*m_ptr[i]

        return com_x/m_tot, com_y/m_tot, com_z/m_tot

