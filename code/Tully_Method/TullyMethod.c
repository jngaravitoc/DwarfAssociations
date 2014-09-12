#include <stdio.h>
#include <math.h>
#include <stdlib.h>

float *load_data(char *filename, int n_col);

float *load_data(char *filename, int n_col){
//	float *data;
	FILE *in;
	float *x;
	float *y;
	float z;
	float vx;
	float vy;
	float vz;
	float M;
	float Rvir;
	int i;	
	

	x = malloc(n_col * sizeof(double));
	y = malloc(n_col * sizeof(double));
	
	in = fopen(filename, "r");	
	if(!in){	
	printf("Problem opening file %s\n",filename);
	exit(1);

}	for(i=0;i<=n_col;i++){
	fscanf(in, "%f %f %f %f %f %f %f %f \n", x, y, &z, &vx, &vy, &vz, &M, &Rvir);
	
	//printf("%f %f %f %f %f %f %f %f \n", *x, y, z, vx, vy, vz, M, Rvir);
}	
	fclose(in);
//	for(i=0;i<10;i++){
//	printf("%f",*x);}
	return x, y;
}

int main(){
float *x;
float *y;


x = malloc(100*sizeof(double));
y = malloc(100*sizeof(double));
x, y = load_data("/home/nicolas/Dropbox/github/DwarfAssociations/data/B64_WM5_10909_LG_7Mpc_2048/HR-data.txt", 14217);

printf("%f %f", *x, *y);
return 0;

}
