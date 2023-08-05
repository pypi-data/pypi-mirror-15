#include "pyspace.h"
#include <math.h>
#include <stdlib.h>
#include <stdio.h>

#define NORM2(X, Y, Z) X*X + Y*Y + Z*Z

__device__
void calculate_force_device(double* x_old, double* y_old, double* z_old, double* m,
        double x_i, double y_i, double z_i,
        double& a_x, double& a_y, double& a_z,
        int num_planets, double eps2, double G)
{
    double r_x_j, r_y_j, r_z_j;
    double x_ji, y_ji, z_ji;
    double m_j;

    double cnst;
    double dist_ij;

    int j;
    for(j=0; j<num_planets; j++)
    {
        r_x_j = x_old[j];
        r_y_j = y_old[j];
        r_z_j = z_old[j];

        m_j = m[j];

        x_ji = r_x_j - x_i;
        y_ji = r_y_j - y_i;
        z_ji = r_z_j - z_i;

        dist_ij = sqrt(eps2 + NORM2(x_ji, y_ji, z_ji));

        if(dist_ij == 0)
            return;

        cnst = (G*m_j/(dist_ij*dist_ij*dist_ij));

        a_x += x_ji*cnst;
        a_y += y_ji*cnst;
        a_z += z_ji*cnst;
    }

}


__global__
void brute_force_kernel(double* x, double* y, double* z,
        double* x_old, double* y_old, double* z_old,
        double* v_x, double* v_y, double* v_z,
        double* a_x, double* a_y, double* a_z,
        double* m, double G, double dt, int num_planets, double eps)
{
    double eps2 = eps*eps;

    int id = blockIdx.x*blockDim.x + threadIdx.x;

    if(id >= num_planets)
        return;
    
    //Update id'th planet

    double a_x_i = a_x[id];
    double a_y_i = a_y[id];
    double a_z_i = a_z[id];

    calculate_force_device(x_old, y_old, z_old, m,
            x_old[id], y_old[id], z_old[id],
            a_x[id], a_y[id], a_z[id],
            num_planets, eps2, G);

    x[id] += v_x[id]*dt + a_x_i*0.5*dt*dt;
    y[id] += v_y[id]*dt + a_y_i*0.5*dt*dt;
    z[id] += v_z[id]*dt + a_z_i*0.5*dt*dt;

    v_x[id] += (a_x_i + a_x[id])*0.5*dt;
    v_y[id] += (a_y_i + a_y[id])*0.5*dt;
    v_z[id] += (a_z_i + a_z[id])*0.5*dt;
}


__host__
void brute_force_gpu_update(double* x, double* y, double* z,
        double* v_x, double* v_y, double* v_z,
        double* a_x, double* a_y, double* a_z,
        double* m, double G, double dt, int num_planets, double eps)
{
    double* x_old = (double*) malloc(num_planets*sizeof(double));
    double* y_old = (double*) malloc(num_planets*sizeof(double));
    double* z_old = (double*) malloc(num_planets*sizeof(double));

    int i;
    for(i=0; i<num_planets; i++)
    {
        x_old[i] = x[i];
        y_old[i] = y[i];
        z_old[i] = z[i];
    }

    double *dev_x, *dev_y, *dev_z, *dev_x_old, *dev_y_old, *dev_z_old;
    double *dev_v_x, *dev_v_y, *dev_v_z, *dev_a_x, *dev_a_y, *dev_a_z;
    double *dev_m;

    if( cudaMalloc((void**)&dev_x, num_planets*sizeof(double)) != cudaSuccess ||
        cudaMalloc((void**)&dev_y, num_planets*sizeof(double)) != cudaSuccess ||
        cudaMalloc((void**)&dev_z, num_planets*sizeof(double)) != cudaSuccess ||
        cudaMalloc((void**)&dev_x_old, num_planets*sizeof(double)) != cudaSuccess ||
        cudaMalloc((void**)&dev_y_old, num_planets*sizeof(double)) != cudaSuccess ||
        cudaMalloc((void**)&dev_z_old, num_planets*sizeof(double)) != cudaSuccess ||
        cudaMalloc((void**)&dev_v_x, num_planets*sizeof(double)) != cudaSuccess ||
        cudaMalloc((void**)&dev_v_y, num_planets*sizeof(double)) != cudaSuccess ||
        cudaMalloc((void**)&dev_v_z, num_planets*sizeof(double)) != cudaSuccess ||
        cudaMalloc((void**)&dev_a_x, num_planets*sizeof(double)) != cudaSuccess ||
        cudaMalloc((void**)&dev_a_y, num_planets*sizeof(double)) != cudaSuccess ||
        cudaMalloc((void**)&dev_a_z, num_planets*sizeof(double)) != cudaSuccess ||
        cudaMalloc((void**)&dev_m, num_planets*sizeof(double)) != cudaSuccess   )
    {
        fprintf(stderr, "ERROR: cudaMalloc failed!");
        exit(0);
    }

    if( cudaMemcpy(dev_x, x, num_planets*sizeof(double), cudaMemcpyHostToDevice) != cudaSuccess ||
        cudaMemcpy(dev_y, y, num_planets*sizeof(double), cudaMemcpyHostToDevice) != cudaSuccess ||
        cudaMemcpy(dev_z, z, num_planets*sizeof(double), cudaMemcpyHostToDevice) != cudaSuccess ||
        cudaMemcpy(dev_x_old, x_old, num_planets*sizeof(double), cudaMemcpyHostToDevice) != cudaSuccess ||
        cudaMemcpy(dev_y_old, y_old, num_planets*sizeof(double), cudaMemcpyHostToDevice) != cudaSuccess ||
        cudaMemcpy(dev_z_old, z_old, num_planets*sizeof(double), cudaMemcpyHostToDevice) != cudaSuccess ||
        cudaMemcpy(dev_v_x, v_x, num_planets*sizeof(double), cudaMemcpyHostToDevice) != cudaSuccess ||
        cudaMemcpy(dev_v_y, v_y, num_planets*sizeof(double), cudaMemcpyHostToDevice) != cudaSuccess ||
        cudaMemcpy(dev_v_z, v_z, num_planets*sizeof(double), cudaMemcpyHostToDevice) != cudaSuccess ||
        cudaMemcpy(dev_a_x, a_x, num_planets*sizeof(double), cudaMemcpyHostToDevice) != cudaSuccess ||
        cudaMemcpy(dev_a_y, a_y, num_planets*sizeof(double), cudaMemcpyHostToDevice) != cudaSuccess ||
        cudaMemcpy(dev_a_z, a_z, num_planets*sizeof(double), cudaMemcpyHostToDevice) != cudaSuccess ||
        cudaMemcpy(dev_m, m, num_planets*sizeof(double), cudaMemcpyHostToDevice) != cudaSuccess )
    {
        fprintf(stderr, "ERROR: cudaMemcpy from host to device failed!");
        exit(0);
    }

    brute_force_kernel<<<ceil(num_planets/1024), 1024>>>(dev_x, dev_y, dev_z,
            dev_x_old, dev_y_old, dev_z_old,
            dev_v_x, dev_v_y, dev_v_z,
            dev_a_x, dev_a_y, dev_a_z,
            dev_m, G, dt, num_planets, eps);

    if( cudaMemcpy(x, dev_x, num_planets*sizeof(double), cudaMemcpyDeviceToHost) != cudaSuccess ||
        cudaMemcpy(y, dev_y, num_planets*sizeof(double), cudaMemcpyDeviceToHost) != cudaSuccess ||
        cudaMemcpy(z, dev_z, num_planets*sizeof(double), cudaMemcpyDeviceToHost) != cudaSuccess || 
        cudaMemcpy(v_x, dev_v_x, num_planets*sizeof(double), cudaMemcpyDeviceToHost) != cudaSuccess ||
        cudaMemcpy(v_y, dev_v_y, num_planets*sizeof(double), cudaMemcpyDeviceToHost) != cudaSuccess ||
        cudaMemcpy(v_z, dev_v_z, num_planets*sizeof(double), cudaMemcpyDeviceToHost) != cudaSuccess ||
        cudaMemcpy(a_x, dev_a_x, num_planets*sizeof(double), cudaMemcpyDeviceToHost) != cudaSuccess ||
        cudaMemcpy(a_y, dev_a_y, num_planets*sizeof(double), cudaMemcpyDeviceToHost) != cudaSuccess ||
        cudaMemcpy(a_z, dev_a_z, num_planets*sizeof(double), cudaMemcpyDeviceToHost) != cudaSuccess )
    {
        fprintf(stderr, "ERROR: cudaMemcpy from device to host failed!\n");
        cudaError_t error = cudaMemcpy(x, dev_x, num_planets*sizeof(double), cudaMemcpyDeviceToHost);
        fprintf(stderr, cudaGetErrorString(error));
        fprintf(stderr, "\n");
        exit(0);
    }

    //CUDA free

    if( cudaFree(dev_x) != cudaSuccess ||
        cudaFree(dev_y) != cudaSuccess ||
        cudaFree(dev_z) != cudaSuccess ||
        cudaFree(dev_x_old) != cudaSuccess ||
        cudaFree(dev_y_old) != cudaSuccess ||
        cudaFree(dev_z_old) != cudaSuccess ||
        cudaFree(dev_v_x) != cudaSuccess ||
        cudaFree(dev_v_y) != cudaSuccess ||
        cudaFree(dev_v_z) != cudaSuccess ||
        cudaFree(dev_a_x) != cudaSuccess ||
        cudaFree(dev_a_y) != cudaSuccess ||
        cudaFree(dev_a_z) != cudaSuccess ||
        cudaFree(dev_m) != cudaSuccess  )
    {
        fprintf(stderr, "ERROR: cudaFree failed!");
        exit(0);
    }

    free(x_old);
    free(y_old);
    free(z_old);
}

