#include<stdlib.h>
#include<stdio.h>


int main(){

int FILE_N=10;
//LE *in[FILE_N];
int i;
int j;

for(i = 0; i < FILE_N; i++){

char filename[50];
FILE *in;

sprintf(filename, "data%03d.txt", i);
printf("%s \n",filename);

in = fopen(filename, "w");
 if(!in){
 printf("problems opening the file");
 exit(1);
 }
 for(j=0;j<10;j++){
 fprintf(in, "%d \n",j);
 }
 
 fclose(in);
}



}

