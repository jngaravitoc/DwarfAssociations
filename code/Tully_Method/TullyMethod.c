/*

This code was written by J. N. Garavito-Camargo in February of 2015.

TO DO:
1- Check Cm and F results from center_mass Fucking problem with distances
2- Write merging function

*/


#include <stdio.h>
#include <math.h>
#include <stdlib.h>


// ##########################         Defining functions            #######################

void *center_mass(float *m,  float * D, float *x, float *y, float *z, int n_points, float * mt, double * cm, float *F);
void *distances(float * x, float * y, float * z, float *D, int n_points);
void *load_data(char *filename, int n_col, float *x,  float * y, float * z, float * vx, float * vy, float * vz, float * m);

// ##########################         Function that calls the data  #######################


void *load_data(char *filename, int n_points, float * x, float * y, float * z, float * vx, float * vy, float * vz, float * m ){
        FILE *in;
	float X;
  	float Y;
	float Z;
	float Vx;
	float Vy;
	float Vz;
	float M;
	int i;

	in = fopen(filename, "r");
	if(!in){
	printf("Problem opening file %s\n",filename);
	exit(1);
		}

	for(i=0;i<=n_points;i++){
	fscanf(in, "%f %f %f %f %f %f %f \n",&X, &Y, &Z, &Vx, &Vy, &Vz, &M);
	x[i] = X; 
        y[i] = Y;
        z[i] = Z;
        vx[i] = Vx;
        vy[i] = Vy;
        vz[i] = Vz;
        m[i] = M;
	}
	fclose(in);
	
	}

// ######################## Main function ################################
int main(){
 float *x;
 float *y;
 float *z;
 float *vx;
 float *vy;
 float *vz;
 float *m;
 
 int i;
 int n_points = 10;
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
 D = malloc(n_points*n_points*sizeof(double));
 cm = malloc(n_points*n_points*(n_points-1)*sizeof(double));
 F = malloc(n_points*n_points*(n_points-1)*sizeof(double));

 load_data("test.txt", n_points, x, y, z, vx, vy, vz, m);


 distances(x, y, z, D, n_points);
 center_mass(m, D, x, y, z,  n_points, mt, cm, F);

 return 0;

}

void  * distances(float *x, float *y, float *z, float *D, int n_points){

  int i;
  int j;
  int k = 0;

  for(i=0;i<n_points;i++){
     for(j = 0; j<n_points;j++){
       D[k] = pow(pow(x[i]-x[j],2) + pow(y[i]-y[j],2) + pow(z[i]-z[j],2), 0.5);
       k++;
      }
    }

}


void * center_mass(float *m, float *D, float *x, float *y, float *z, int n_points, float * mt, double * cm, float *F){

  int p;
  int q;
  int j;
  int i;
  int n;
  int k=0;
 // for(i=0;i<100;i++){
 // printf("%f \n", D[i]);
//}
  for(p=0;p<n_points;p++){
    for(q=0;q<n_points;q++){
      if(p!=q){
	n=0;
        for(j=0;j<n_points;j++){
            if(j!=q & j!=p){
	      n++;
              mt[k] = m[q] + m[p];
              cm[k] = m[p]*pow(D[j+p*n_points],2) / mt[k] + m[q]*pow(D[j+q*n_points],2) / mt[k] - m[q]*m[p]*pow(D[q+p*n_points],2) / pow(mt[k],2);
              //printf("%f \t %d \t %d\n", cm[k], p, q);
              
              if(mt[k] > m[k]){
              F[k] = mt[k]/pow(cm[k],2);
                }
              else{
              F[k] = m[k]/pow(cm[k],2);
	      
                }
	     printf("%3f \t %d \t %d \t %d \t %3f  \n", F[k], p, q, k, cm[k]);
	     k++;
 /*if(n>0){
              // this is to print just the minimum values of F and to ignore distances of the same particle
	      if(F[j]<F[j-1] & (D[j+p*n_points] !=0) & (D[j+q*n_points] != 0)){
              printf("%f \t %d \t %d \t %d \t %f \t %f \t %f \t %f \t %f \t %f \n", F[j], p, q, j, m[p], m[q], mt[j], pow(D[j+p*n_points], 2), pow(D[j+q*n_points], 2), pow(D[q+p*n_points], 2) );

			}			
	              }*/
}


            }
          }
        }
      }
}
