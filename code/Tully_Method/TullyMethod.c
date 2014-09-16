#include <stdio.h>
#include <math.h>
#include <stdlib.h>

float  distances(float * x, float * y, float * z);
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
	  fscanf(in, "%f %f  \n",&X, &Y);
	  x[i]=X;
	  y[i]=Y;
	  z[i]=Z;
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
 
 x = malloc(n_points*sizeof(double));
 y = malloc(n_points*sizeof(double));
 z = malloc(n_points*sizeof(double));
 vx = malloc(n_points*sizeof(double));
 vy = malloc(n_points*sizeof(double));
 vz = malloc(n_points*sizeof(double));
 m = malloc(n_points*sizeof(double));
 Rvir = malloc(n_points*sizeof(double));
 D = malloc(n_points*sizeof(double));


 x, y, z = load_data("/home/nicolas/Dropbox/github/DwarfAssociations/data/B64_WM5_10909_LG_7Mpc_2048/HR-data.txt", 100, x, y, z, vx, vy, vz, m, Rvir);
  
 D = distances(x, y, z);
 
 printf("%f \n", D[1]);

 //intf("%f %f\n",  x[1], y[1]);
 return 0;

}

float distances(float *x, float *y, float *z){

  float d;
  int i; 

  for(i=0;i<10;i++){
  d[i] = pow(x[i],2) + pow(y[i],2) + pow(z[i],2);
  }
  return d;

}
