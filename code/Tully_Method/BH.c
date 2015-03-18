/*

Implementation of the Barnes Hut algorithm.



*/


#include <stdlib.h>
#include <stdio.h>
#include <math.h>


void BarnesHut(double *x, double *y, double *z, int n_points){

double min_x;
double max_x;
double min_y;
double max_y;
double min_z;
double max_z;
int i;

printf("Hello Barnes Hut algorithm \n");

min_x = x[0];
max_x = x[0];

for(i=0;i<n_points;i++){

if(x[i]<min_x){
min_x = x[i];
}

if(x[i]>max_x){
max_x = x[i];
}

}

printf("El minimo de x es: %lf \n", min_x);
printf("El maximo de x es: %lf \n", max_x);

}


