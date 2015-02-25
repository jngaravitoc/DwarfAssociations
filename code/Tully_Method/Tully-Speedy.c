/*

This code was written by J. N. Garavito-Camargo in February of 2015.


*/


#include <stdio.h>
#include <math.h>
#include <stdlib.h>


// ##########################         Defining functions            #######################

void center_mass(double *m, double *D, int n_points, double cm, double *F, double *Q, double *P, double *M);
void distances(double * x, double * y, double * z, double *D, int n_points); 
void load_data(char *filename, int n_points, double * x, double * y, double * z, double * vx, double * vy, double * vz, double * m );


// ######################## Main function ################################
int main(int argc, char **argv){
 
int n_points = atoi(argv[1]);

int i;
int q;
int p;

double *D = NULL;
double *F = NULL;
double *m=NULL;
double *Q=NULL;
double *P=NULL;
double *M=NULL;

double xt;
double yt;
double zt;

double cm;

double *x=NULL;
double *y=NULL;
double *z=NULL;

double vxt;
double vyt;
double vzt;

double *vx=NULL;
double *vy=NULL;
double *vz=NULL;



F = malloc(sizeof(double));
Q = malloc(sizeof(double));
P = malloc(sizeof(double));
M = malloc(sizeof(double));
x = malloc(n_points*sizeof(double));
y = malloc(n_points*sizeof(double));
z = malloc(n_points*sizeof(double));
vx = malloc(n_points*sizeof(double));
vy = malloc(n_points*sizeof(double));
vz = malloc(n_points*sizeof(double));
m = malloc(n_points*sizeof(double));

if(!( D = malloc(n_points*n_points*sizeof(double)))){
   fprintf(stderr, "problem in allocation 1\n");
   exit(1);
 }

do{
 FILE *in;
 char filename[100];
 
//uble *vx;
//double *vy;
//double *vz;

 sprintf(filename, "test%05d.txt", n_points);
 printf("%s \n",filename);
 
 load_data(filename, n_points, x, y, z, vx, vy, vz, m);
 printf("Done loading data \n");

 distances(x, y, z, D, n_points);
 printf("Done computing distances \n");
 

 center_mass(m, D, n_points, cm, F, Q, P, M);
 printf("Donde computing center of mass \n");
 
 p = P[0];
 q = Q[0];

 xt = (1 / (m[p] + m[q])) * (m[p]*x[p] + m[q]*x[q]);
 yt = (1 / (m[p] + m[q])) * (m[p]*y[p] + m[q]*y[q]);
 zt = (1 / (m[p] + m[q])) * (m[p]*z[p] + m[q]*z[q]);
 
 vxt = (1 / (m[p] + m[q])) * (m[p]*vx[p] + m[q]*vx[q]);;
 vyt = (1 / (m[p] + m[q])) * (m[p]*vy[p] + m[q]*vy[q]);;
 vzt = (1 / (m[p] + m[q])) * (m[p]*vz[p] + m[q]*vz[q]);

 sprintf(filename, "test%05d.txt", n_points-1);
 
 
 in = fopen(filename,"w");
 printf("Writting new data \n");
 if(!in){
 printf("problems opening the file %s\n", filename);
 exit(1);
 } 

 for(i=0;i<n_points;i++){
 if((i!=P[0]) && (i!=Q[0])){ // Aca evito que escriba los halos que ya fusione
 fprintf(in, "%lf \t %lf \t %lf \t %lf \t %lf \t %lf \t %lf\n",x[i], y[i], z[i], vx[i], vy[i], vz[i], m[i]);
 }
 }

 fprintf(in, "%lf \t %lf \t %lf \t %lf \t %lf \t %lf \t %lf \n", xt, yt, zt, vxt, vyt, vzt,  m[q]+m[p]); //check this mass
 fclose(in);
 n_points--;
 
 }while(n_points>2);


 return 0;
}



void load_data(char *filename, int n_points, double * x, double * y, double * z, double * vx, double * vy, double * vz,  double * m ){
        FILE *in;
	double X;
  	double Y;
	double Z;
	double M;
        double VX;
        double VY;
        double VZ;
	int i;

	in = fopen(filename, "r");
	if(!in){
	  printf("Problem opening file %s\n",filename);
	  exit(1);
	}
	
	for(i=0;i<n_points;i++){
	  fscanf(in, "%lf %lf %lf %lf %lf %lf %lf \n",&X, &Y, &Z, &VX, &VY, &VZ, &M);
	  x[i] = X; 
	  y[i] = Y;
	  z[i] = Z;
	  m[i] = M;
          vx[i] = VX;
          vy[i] = VZ; 
          vz[i] = VZ;        
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



void center_mass(double *m, double *D,  int n_points,  double cm, double *F, double *Q, double *P, double *M){

  int p;
  int q;
  int j;
  int k=0;
  int a=0;
  int b=0;
  int c=0;
  double mt;
  double max;
  

  for(p=0;p<n_points;p++){
    for(q=0;q<n_points;q++){
      if((p!=q) && (D[p + (q*n_points)]>9.4) && ((m[q] - m[p]) < 96891000.0)){	
        for(j=0;j<n_points;j++){
	  if((j!=q) && (j!=p)){
            if(((D[j+(p*n_points)]<4)) && (D[j + q*n_points]<4) ){
	    fflush(stdout);

	    
              a = j + (p*n_points);
              b = j + (q*n_points);
              c = p + (q*n_points);

	      	      
	      mt = m[p] + m[q];
	      cm = (m[p]*pow(D[a],2) / mt) + (m[q]*pow(D[b],2) / mt) - (m[q]*m[p]*pow(D[c],2) / pow(mt,2));

	      
              
              if(mt > m[j]){
		F[0] = mt/pow(cm,2);
	      }else{
		F[0] = m[j]/pow(cm,2);		
	      }
	     
	     if(k==0){
              // this is to print just the minimum values of F and to ignore distances of the same particle
	      max = F[0];}
	     else{  
	      if(F[0]>max){
	       max=F[0];
		Q[0] = q;
                P[0] = p;             		  
		}
   		}
	     F[0] = 0;
            
            
            k++;				      
	    }
  	  }	 	  
	}
      }
    }
  }
}


