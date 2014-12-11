/*
TO DO:
1- Fixed difference in codes in the cm distance
2- Write merging function
3- Review Tully Method.

*/


#include <stdio.h>
#include <math.h>
#include <stdlib.h>


void *center_mass(float *m, float *D, float *x, float *y, float *z, int n_points, float * mt, double * cm, float *F);
void *distances(float * x, float * y, float * z, float *D, int n_points);
void *load_data(char *filename, int n_col, float * x, float * y, float * z, float * vx, float * vy, float * vz, float * m);

void *load_data(char *filename, int n_col, float * x, float * y, float * z, float * vx, float * vy, float * vz, float * m ){
//	float *data;
  FILE *in;
	float X;
  float Y;
	float Z;
	float Vx;
	float Vy;
	float Vz;
	float M;
	float RVir;
	int i;



	in = fopen(filename, "r");
	if(!in){
	printf("Problem opening file %s\n",filename);
	exit(1);

}	for(i=0;i<=n_col;i++){
	  fscanf(in, "%f %f %f %f %f %f %f \n",&X, &Y, &Z, &Vx, &Vy, &Vz, &M);
	  x[i]=X;
	  y[i]=Y;
	  z[i]=Z;
	  vx[i] = Vx;
	  vy[i] = Vy;
	  vz[i] = Vz;
	  m[i] = M;
	  //Rvir[i] = RVir;
	}
	fclose(in);
	//return x, y, z, vx, vy, vz, M;
}

int main(){
 float *x;
 float *y;
 float *z;
 float *vx;
 float *vy;
 float *vz;
 float *m;
 float *Rvir;
 int i=11;
 int n_points = 100;
 float *D;
 double *cm;
 float *mt;
 float *F;

 x = malloc(n_points*sizeof(double));
 y = malloc(n_points*sizeof(double));
 z = malloc(n_points*sizeof(double));
 vx = malloc(n_points*sizeof(double));
 vy = malloc(n_points*sizeof(double));
 vz = malloc(n_points*sizeof(double));
 m = malloc(n_points*sizeof(double));
 mt = malloc(n_points*sizeof(double));
 Rvir = malloc(n_points*sizeof(double));
 D = malloc(n_points*n_points*sizeof(double));
 cm = malloc(n_points*n_points*(n_points-1)*sizeof(double));
 F = malloc(n_points*n_points*(n_points-1)*sizeof(double));

 load_data("data.dat", 100, x, y, z, vx, vy, vz, m);



 distances(x, y, z, D, n_points);
 center_mass(m, D, x, y, z,  n_points, mt, cm, F);
//for(i=0;i<n_points;i++){
 //printf("%f  \t %f \t %f \n", D[i], cm[i], mt[i]);
//}
 return 0;

}

void  * distances(float *x, float *y, float *z, float *D, int n_points){

  int i;
  int j;
   for(i=0;i<n_points;i++){
     for(j = 0; j<n_points;j++){
       D[i] = pow(pow(x[i]-x[j],2) + pow(y[i]-y[j],2) + pow(z[i]-z[j],2), 0.5);
      }
    }

}


void * center_mass(float *m, float *D, float *x, float *y, float *z, int n_points, float * mt, double * cm, float *F){

  int p;
  int q;
  int j;
  //float M;
  int i;
  for(p=0;p<n_points;p++){
    for(q=0;q<n_points;q++){
      if(p!=q){
        for(j=0;j<n_points;j++){
            if(j!=q & j!=p){
              mt[j] = m[q] + m[p];
              cm[j]=m[p]*pow(D[j+p*n_points],2) / mt[j] + m[q]*pow(D[j+q*n_points],2) / mt[j] - m[q]*m[p]*pow(D[q+p*n_points],2) / pow(mt[j],2);
              printf("%f \n", cm[j]);
              if(mt[j] > m[j]){
              F[j] = mt[j]/pow(cm[j],2);
                }
              else{
              F[j] = m[j]/pow(cm[j],2);

                }
              }

            }
          }
        }
      }
}
