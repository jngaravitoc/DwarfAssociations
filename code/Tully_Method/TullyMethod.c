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

void center_mass(double *m, double *D, double *x, double *y, double *z, int n_points, double * mt, double * cm, double *F, double *Q, double *P, double *M);
void distances(double * x, double * y, double * z, double *D, int n_points); 
void load_data(char *filename, int n_points, double * x, double * y, double * z, double * m );


// ##########################         Function that calls the data  #######################


// ######################## Main function ################################
int main(){
 double *x;
 double *y;
 double *z;
 //double *vx;
 //double *vy;
 //double *vz;
 double *m;
 double *Q;
 double *P;
 double *M;
 double xt;
 double yt;
 double zt;

 int n_points = 500;
 double *D = NULL;
 double *cm = NULL;
 double *mt = NULL;
 double *F = NULL;
 
 int i;
 int q;
 int p; 
 Q = malloc(sizeof(double));
 P = malloc(sizeof(double));
 M = malloc(sizeof(double));
 x = malloc(n_points*sizeof(double));
 y = malloc(n_points*sizeof(double));
 z = malloc(n_points*sizeof(double));
// vx = malloc(n_points*sizeof(double));
// vy = malloc(n_points*sizeof(double));
// vz = malloc(n_points*sizeof(double));
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

 load_data("test.txt", n_points, x, y, z, m);


 distances(x, y, z, D, n_points);

 center_mass(m, D, x, y, z,  n_points, mt, cm, F, Q, P, M);
 
 printf("out %lf \t %lf \n", P[0], Q[0]);
 
 p = P[0];
 q = Q[0];

 xt = (1 / (m[p] + m[q])) * (m[p]*x[p] + m[q]*x[q]);
 yt = (1 / (m[p] + m[q])) * (m[p]*y[p] + m[q]*y[q]);
 zt = (1 / (m[p] + m[q])) * (m[p]*z[p] + m[q]*z[q]);


 for(i=0;i<500;i++){
 if((i!=P[0]) && (i!=Q[0])){
 printf("%lf \t %lf \t %lf \t %lf\n",x[i], y[i], z[i], m[i]);
 }
}
 printf("%lf \t %lf \t %lf \t %lf \n", xt, yt, zt, m[q]+m[p]);
 return 0;
}



void load_data(char *filename, int n_points, double * x, double * y, double * z,  double * m ){
        FILE *in;
	double X;
  	double Y;
	double Z;
	double M;
	int i;

	in = fopen(filename, "r");
	if(!in){
	  printf("Problem opening file %s\n",filename);
	  exit(1);
	}
	
	for(i=0;i<n_points;i++){
	  fscanf(in, "%lf %lf %lf %lf \n",&X, &Y, &Z, &M);
	  x[i] = X; 
	  y[i] = Y;
	  z[i] = Z;
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



void center_mass(double *m, double *D, double *x, double *y, double *z, int n_points, double * mt, double * cm, double *F, double *Q, double *P, double *M){

  int p;
  int q;
  int j;
  int k=0;
  int a=0;
  int b=0;
  int c=0;
  double min;

  for(p=0;p<n_points;p++){
    for(q=0;q<n_points;q++){
      if(p!=q){	
        for(j=0;j<n_points;j++){
	  if((j!=q) && (j!=p)){
	    fflush(stdout);

	    
              a = j + (p*n_points);
              b = j + (q*n_points);
              c = p + (q*n_points);

	      //fprintf(stdout, "%lf %lf %d \t %d %d\n", D[a], D[b], a, b, k);	      
	      mt[k] = m[p] + m[q];
	      cm[k] = (m[p]*pow(D[a],2) / mt[k]) + (m[q]*pow(D[b],2) / mt[k]) - (m[q]*m[p]*pow(D[c],2) / pow(mt[k],2));

	       //printf("%lf \n", mt[k]);
              
              if(mt[k] > m[j]){
		F[k] = mt[k]/pow(cm[k],2);
	      }else{
		F[k] = m[j]/pow(cm[k],2);		
	      }
	     
	     //printf("%lf \t %d \t %d \t %lf \t %lf \t %lf \n ", F[k], p, q, m[p], m[q], mt[k]);
	      
	      if(k==0){
              // this is to print just the minimum values of F and to ignore distances of the same particle
	      min = F[0];}
	     else{  
	      if(F[k]<min){
	       min=F[k];
		Q[0] = q;
                P[0] = p;
             //printf("%lf \t %d \t %d \t %lf \t %lf \t %lf \n", F[k], p, q, m[p], m[q], mt[k]);
              		  
		}
	      
		}
	     
	     //printf("%lf \n", min);	     
             
	     k++;				      
	  }		  	  
	}
      }
    }
  }
}


