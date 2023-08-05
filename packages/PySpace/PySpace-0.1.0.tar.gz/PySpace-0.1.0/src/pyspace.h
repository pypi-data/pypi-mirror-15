#ifndef PYSPACE_H
#define PYSPACE_H

void brute_force_update(double* x, double* y, double* z, 
        double* v_x, double* v_y, double* v_z,
        double* a_x, double* a_y, double* a_z,
        double* m, double G, double dt, int num_planets, double eps);

void barnes_update(double *x, double *y, double *z, 
        double *v_x, double *v_y, double *v_z,
        double *a_x, double *a_y, double *a_z,
        double *m, double G, double dt, int num_planets,
        double theta, double eps);

void brute_force_gpu_update(double* x, double* y, double* z, 
        double* v_x, double* v_y, double* v_z,
        double* a_x, double* a_y, double* a_z,
        double* m, double G, double dt, int num_planets, double eps);

void calculate_force(double* x_old, double* y_old, double* z_old, double* m,
        double x_i, double y_i, double z_i,
        double& a_x, double& a_y, double& a_z,
        int num_planets, double eps2, double G);

#endif
