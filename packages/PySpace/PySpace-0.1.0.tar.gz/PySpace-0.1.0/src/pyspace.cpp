#include "pyspace.h"
#include <cmath>
#include <cstddef>
#include <omp.h>
#include <list>

#define NORM2(X, Y, Z) X*X + Y*Y + Z*Z
#define MIN(X,Y) ((X) < (Y)) ? (X) : (Y)
#define MAX(X,Y) ((X) < (Y)) ? (Y) : (X)
#define ERR 1e-5

using namespace std;

struct BarnesNode
{
    double mass;
    double x;
    double y;
    double z;
    double width;
    bool is_child;
    BarnesNode *children[2][2][2];
    
    BarnesNode()
    {
        mass = x = y = z = width = 0;
        is_child = true;
        for(int i=0;i<2;i++)
            for(int j=0;j<2;j++)
                for(int k=0;k<2;k++)
                    children[i][j][k] = NULL;
    }
    
    ~BarnesNode()
    {
        for(int i=0;i<2;i++)
            for(int j=0;j<2;j++)
                for(int k=0;k<2;k++)
                    if(children[i][j][k]!=NULL)
                        delete children[i][j][k];
    }
 
};

struct BarnesPlanet
{
    double x;
    double y;
    double z;
    double mass;
    
    BarnesPlanet()
    {
        x = y = z = 0;
    }

    BarnesPlanet(double x, double y, double z, double mass)
    {
        this->x = x;
        this->y = y;
        this->z = z;
        this->mass = mass;
    }
};

BarnesPlanet build_barnes_tree(BarnesNode *node, list<BarnesPlanet> &planets,
                                 double x0, double y0, double z0, double width)
{
    if(planets.size() == 1)
    {
        node->x = planets.front().x;
        node->y = planets.front().y;
        node->z = planets.front().z;
        node->mass = planets.front().mass;
        node->width = width;
        node->is_child = true;
        return BarnesPlanet(planets.front().x, planets.front().y, 
                planets.front().z, planets.front().mass);
    }


    BarnesPlanet com(0,0,0,0);

    for(int octant=0;octant<8;octant++)
    {
        list<BarnesPlanet> temp;
        int i=(octant&1);
        int j=((octant&2)>>1);
        int k=((octant&4)>>2);
        
        double x1 = x0 + i*width/2 - ((i+1)&1)*ERR;
        double x2 = x0 + (i+1)*width/2 + i*ERR;
        double y1 = y0 + j*width/2 - ((j+1)&1)*ERR;
        double y2 = y0 + (j+1)*width/2 + j*ERR;
        double z1 = z0 + k*width/2 - ((k+1)&1)*ERR;
        double z2 = z0 + (k+1)*width/2 + k*ERR;
                                      
        for(list<BarnesPlanet>::iterator it = planets.begin();it != planets.end();)
        {
            list<BarnesPlanet>::iterator next_it = it;
            ++next_it;

            if((it->x)>= x1 && (it->x)<x2 &&
               (it->y)>= y1 && (it->y)<y2 &&
               (it->z)>= z1 && (it->z)<z2)
            {
                temp.push_back(BarnesPlanet(it->x, it->y, it->z, it->mass));
                planets.erase(it);
            }
            
            it=next_it;
        }
        
        if(temp.size()==0)
            continue;

        node->children[i][j][k] = new BarnesNode;
        BarnesPlanet octant_com = build_barnes_tree(node->children[i][j][k], temp,
                          x1, y1, z1, width/2+ERR);

        com.x += octant_com.mass*octant_com.x;
        com.y += octant_com.mass*octant_com.y;
        com.z += octant_com.mass*octant_com.z;
        com.mass += octant_com.mass;
    }
    
    com.x /= com.mass;
    com.y /= com.mass;
    com.z /= com.mass;

    node->x = com.x;
    node->y = com.y;
    node->z = com.z;
    node->mass = com.mass;
    node->width = width;
    node->is_child = false;
 
    return com;
}

void get_barnes_acceleration(BarnesNode *node, 
                             double x, double y, double z,
                             double &a_x, double &a_y, double &a_z,
                             double G, double theta, double eps2)
{
    double r_x = node->x - x;
    double r_y = node->y - y;
    double r_z = node->z - z;
    double dist = sqrt(eps2 + NORM2(r_x, r_y, r_z));
    
    if(dist < ERR)
        return;
    
    if(node->is_child || (node->width)/dist < theta)
    {      

        double cnst = G*(node->mass)/(dist*dist*dist);
        a_x += cnst*r_x;
        a_y += cnst*r_y;
        a_z += cnst*r_z;
    }
    else
    {
        for(int i=0;i<2;i++)
            for(int j=0;j<2;j++)
                for(int k=0;k<2;k++)
                {
                    BarnesNode *child = node->children[i][j][k];
                    if(child!=NULL)
                    {
                        get_barnes_acceleration(child, x, y, z, a_x, a_y, a_z,
                                G, theta, eps2);
                    }
                }
      
    }
}

void barnes_update(double *x, double *y, double *z,
                   double *v_x, double *v_y, double *v_z,
                   double *a_x, double *a_y, double *a_z,
                   double *m, double G, double dt, int num_planets,
                   double theta, double eps)
{
    list<BarnesPlanet> planets;
    double min_x, max_x, min_y, max_y, min_z, max_z;
    min_x = min_y = min_z = INFINITY;
    max_x = max_y = max_z = -INFINITY;

    double eps2 = eps*eps;

    for(int i=0;i<num_planets;i++)
    {
        planets.push_back(BarnesPlanet(x[i], y[i], z[i],m[i]));

        min_x = MIN(min_x, x[i]); 
        max_x = MAX(max_x, x[i]);
        min_y = MIN(min_y, y[i]);
        max_y = MAX(max_y, y[i]);
        min_z = MIN(min_z, z[i]);
        max_z = MAX(max_z, z[i]);
    }
    
    double width = MAX(max_x - min_x, MAX(max_y - min_y, max_z - min_z)) + ERR;

    BarnesNode *root = new BarnesNode;
    build_barnes_tree(root, planets, min_x, min_y, min_z, width);
                                 
    double a_x_temp = 0;
    double a_y_temp = 0;
    double a_z_temp = 0;
   
    #pragma omp parallel for shared(root, x, y, z, v_x, v_y, v_z, a_x, a_y, a_z) \
    private(a_x_temp, a_y_temp, a_z_temp)
    for(int i=0;i<num_planets;i++)
    {
        a_x_temp = 0;
        a_y_temp = 0;
        a_z_temp = 0;
        
        get_barnes_acceleration(root, x[i], y[i], z[i], 
                a_x_temp, a_y_temp, a_z_temp, G, theta, eps2);
        
        x[i] += v_x[i]*dt + a_x[i]*0.5*dt*dt;
        y[i] += v_y[i]*dt + a_y[i]*0.5*dt*dt;
        z[i] += v_z[i]*dt + a_z[i]*0.5*dt*dt;

        v_x[i] += (a_x[i] + a_x_temp)*0.5*dt;
        v_y[i] += (a_y[i] + a_y_temp)*0.5*dt;
        v_z[i] += (a_z[i] + a_z_temp)*0.5*dt;
        
        a_x[i] = a_x_temp;
        a_y[i] = a_y_temp;
        a_z[i] = a_z_temp;
    }
    
    delete root;
}

void calculate_force(double* x_old, double* y_old, double* z_old, double* m,
        double x_i, double y_i, double z_i,
        double& a_x, double& a_y, double& a_z,
        int num_planets, double eps2, double G)
{
    double r_x_j, r_y_j, r_z_j;
    double x_ji, y_ji, z_ji;
    double m_j;

    double cnst;
    double dist_ij;

    for(int j=0; j<num_planets; j++)
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

void brute_force_update(double* x, double* y, double* z,
        double* v_x, double* v_y, double* v_z,
        double* a_x, double* a_y, double* a_z,
        double* m, double G, double dt, int num_planets, double eps)
{
    //Calculate and update all pointers
    double a_x_i, a_y_i, a_z_i;
    double v_x_i, v_y_i, v_z_i;
    double temp_a_x = 0, temp_a_y = 0, temp_a_z = 0;
    double eps2 = eps*eps;

    double* x_old = new double[num_planets];
    double* y_old = new double[num_planets];
    double* z_old = new double[num_planets];

    #pragma omp parallel for shared(x_old, y_old, z_old, x, y, z)
    for(int i=0; i<num_planets; i++)
    {
        x_old[i] = x[i];
        y_old[i] = y[i];
        z_old[i] = z[i];
    }

    #pragma omp parallel for shared(x, y, z, x_old, y_old, z_old, v_x, v_y, v_z, \
            a_x, a_y, a_z, m, G, dt) \
    private(a_x_i, a_y_i, a_z_i, v_x_i, v_y_i, v_z_i, temp_a_x, temp_a_y, temp_a_z)
    for(int i=0; i<num_planets; i++)
    {
        a_x_i = a_x[i];
        a_y_i = a_y[i];
        a_z_i = a_z[i];

        v_x_i = v_x[i];
        v_y_i = v_y[i];
        v_z_i = v_z[i];

        calculate_force(x_old, y_old, z_old, m,
                x_old[i], y_old[i], z_old[i],
                temp_a_x, temp_a_y, temp_a_z,
                num_planets, eps2, G);
        
        a_x[i] = temp_a_x;
        a_y[i] = temp_a_y;
        a_z[i] = temp_a_z;

        temp_a_x = 0;
        temp_a_y = 0;
        temp_a_z = 0;

        x[i] += v_x_i*dt + a_x_i*0.5*dt*dt;
        y[i] += v_y_i*dt + a_y_i*0.5*dt*dt;
        z[i] += v_z_i*dt + a_z_i*0.5*dt*dt;

        v_x[i] += (a_x_i + a_x[i])*0.5*dt;
        v_y[i] += (a_y_i + a_y[i])*0.5*dt;
        v_z[i] += (a_z_i + a_z[i])*0.5*dt;

    }

    delete[] x_old;
    delete[] y_old;
    delete[] z_old;
}


