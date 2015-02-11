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

void center_mass(double *m, double *D, double *x, double *y, double *z, int n_points, double * mt, double * cm, double *F);
void distances(double * x, double * y, double * z, double *D, int n_points);
void load_data(char *filename, int n_points, double * x, double * y, double * z, double * vx, double * vy, double * vz, double * m );
void test(double *D, int n_points);

// ##########################         Function that calls the data  #######################


// ######################## Main function ################################
int main(){
 double *x;
 double *y;
 double *z;
 double *vx;
 double *vy;
 double *vz;
 double *m;
 

 int n_points = 10;
 double *D = NULL;
 double *cm = NULL;
 double *mt = NULL;
 double *F = NULL;
 

 x = malloc(n_points*sizeof(double));
 y = malloc(n_points*sizeof(double));
 z = malloc(n_points*sizeof(double));
 vx = malloc(n_points*sizeof(double));
 vy = malloc(n_points*sizeof(double));
 vz = malloc(n_points*sizeof(double));
 m = malloc(n_points*sizeof(double));
 mt = malloc(n_points*n_points*n_points*sizeof(double));

 

 if(!( D = malloc(n_points*n_points*sizeof(double)))){
   fprintf(stderr, "problem in allocation\n");
   exit(1);
 }

 if(!(cm = malloc(n_points*n_points*(n_points)*sizeof(double)))){
   fprintf(stderr, "problem in allocation\n");
   exit(1);
 }
 if(!(F = malloc(n_points*n_points*(n_points)*sizeof(double)))){
   fprintf(stderr, "problem in allocation\n");
   exit(1); 
 }

 load_data("test.txt", n_points, x, y, z, vx, vy, vz, m);


 distances(x, y, z, D, n_points);

 test(D, n_points);
 center_mass(m, D, x, y, z,  n_points, mt, cm, F);
 


 return 0;
}



void load_data(char *filename, int n_points, double * x, double * y, double * z, double * vx, double * vy, double * vz, double * m ){
        FILE *in;
	double X;
  	double Y;
	double Z;
	double Vx;
	double Vy;
	double Vz;
	double M;
	int i;

	in = fopen(filename, "r");
	if(!in){
	  printf("Problem opening file %s\n",filename);
	  exit(1);
	}
	
	for(i=0;i<n_points;i++){
	  fscanf(in, "%lf %lf %lf %lf %lf %lf %lf \n",&X, &Y, &Z, &Vx, &Vy, &Vz, &M);
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

void  distances(double *x, double *y, double *z, double *D, int n_points){

  int i;
  int j;
  int k = 0;

  for(i=0;i<n_points;i++){
     for(j = 0; j<n_points;j++){
       D[k] = sqrt(pow(x[i]-x[j],2) + pow(y[i]-y[j],2) + pow(z[i]-z[j],2));
       k++;
      }
    }
}

void test(double *D, int n_points){
  int p, a, b;
  int q;
  int j;
  int k=0;
  for(p=0;p<n_points;p++){
    for(q=0;q<n_points;q++){
      if(p!=q){	
        for(j=0;j<n_points;j++){
	  if((j!=q) && (j!=p)){
              a = j + (p*n_points);
              b = j + (q*n_points);
	      fprintf(stdout, "%lf %lf %d \t %d %d\n", D[a], D[b], a, b, n_points);	      
	    
	  }}}}}
}

void center_mass(double *m, double *D, double *x, double *y, double *z, int n_points, double * mt, double * cm, double *F){

  int p;
  int q;
  int j;
  int k=0;
  int a=0;
  int b=0;
  int c=0;
  

  for(p=0;p<n_points;p++){
    for(q=0;q<n_points;q++){
      if(p!=q){	
        for(j=0;j<n_points;j++){
	  if((j!=q) && (j!=p)){
	    fflush(stdout);

	    
              a = j + (p*n_points);
              b = j + (q*n_points);
              c = p + (q*n_points);

	      fprintf(stdout, "%lf %lf %d \t %d %d\n", D[a], D[b], a, b, k);	      
	      mt[k] = m[p] + m[q];

	      //	      cm[k] = (m[p]*pow(D[a],2) / mt[k]) + (m[q]*pow(D[b],2) / mt[k]) - (m[q]*m[p]*pow(D[c],2) / pow(mt[k],2));
              //printf("%f \t %d \t %d\n", cm[k], p, q);
              /*
              if(mt[k] > m[k]){
		F[k] = mt[k]/pow(cm[k],2);
	      }else{
		F[k] = m[k]/pow(cm[k],2);		
	      }
	      */

	      //printf("%3f \t %d \t %d \t %d \t %3f \t %d \t %d \t %f \t %f \t %f \t %f \t %f \n", F[k], p, q, k, cm[k], j+p*n_points, j+q*n_points, D[j+p*n_points], D[j+q*n_points], m[q], m[p], mt[k]);
	      k++;
	      //	      if(k>0){
		// this is to print just the minimum values of F and to ignore distances of the same particle
	      //		if(F[k]<F[k-1]){
		  //printf("%f \t %d \t %d \t %f \t %f \t %f \t  \n", F[k], p, q, m[p], m[q], mt[k] );		  
	      //		}
	      //	      }				      
	  }		  	  
	}
      }
    }
  }
}
