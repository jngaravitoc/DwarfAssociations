#include <stdio.h>
#include <math.h>
#include <stdlib.h>


float *center_mass(float * m, float *D, float *cm, int n_points );
float *distances(float * x, float * y, float * z, float *D);
float *load_data(char *filename, int n_col, float *x, float  * y, float * z, float * vx, float * vy, float * vz, float * m, float *Rvir );

float *load_data(char *filename, int n_col, float * x, float * y, float * z, float * vx, float * vy, float * vz, float * m, float *Rvir ){
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
	  fscanf(in, "%f %f %f %f %f %f %f %f \n",&X, &Y, &Z, &Vx, &Vy, &Vz, &M, &RVir);
	  x[i]=X;
	  y[i]=Y;
	  z[i]=Z;
	  vx[i] = Vx;
	  vy[i] = Vy;
	  vz[i] = Vz;
	  m[i] = M;
	  Rvir[i] = RVir;
	}	
	fclose(in);
	return x, y, z;
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
 float *cm; 

 x = malloc(n_points*sizeof(double));
 y = malloc(n_points*sizeof(double));
 z = malloc(n_points*sizeof(double));
 vx = malloc(n_points*sizeof(double));
 vy = malloc(n_points*sizeof(double));
 vz = malloc(n_points*sizeof(double));
 m = malloc(n_points*sizeof(double));
 Rvir = malloc(n_points*sizeof(double));
 D = malloc(n_points*sizeof(double));
 cm = malloc(n_points*(n_points-1)*sizeof(double));

 x, y, z = load_data("/home/nicolas/Dropbox/github/DwarfAssociations/data/B64_WM5_10909_LG_7Mpc_2048/HR-data.txt", 100, x, y, z, vx, vy, vz, m, Rvir);
 


 distances(x, y, z, D);
 center_mass(m, D, cm, n_points);
for(i=0;i<n_points;i++){
 printf("esto es cm en el main %f \t %f  \n", cm[i], D[i]);
}
 return 0;

}

float  * distances(float *x, float *y, float *z, float *D){

  int i; 
   for(i=0;i<99;i++){
   D[i] = pow(x[i],2) + pow(y[i],2) + pow(z[i],2);
   // printf("DDD %f \n", D[i]);
    }
  return D;
}


float *  center_mass(float *m, float *D, float *cm, int n_points){
  
  int i;
  int j;
  //printf("cm inicial %f ", cm[0]);
  for(i=0;i<n_points;i++){
    for(j=0;j<n_points;j++){
      if(j!=i){
	cm[i]=m[i]*pow(D[i],2) /(m[j]+m[i]) + (m[j]*pow(D[j],2)/(m[i] + m[j])) - (m[i]*m[j]*pow(D[i]-D[j],2)/(pow((m[i]+m[j]),2)));
	//printf("Cm \t  %f \n", cm[i]);
      }
  }
  }
  //for(i=0;i<n_points;i++){
    //printf("Cm \t  %f \n", cm[i]);
  //  } 
 return cm;
}
