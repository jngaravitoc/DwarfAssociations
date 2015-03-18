all: a.out
a.out: TullyMethod.o BH.o 
	cc TullyMethod.o BH.o -lm
TullyMethod.o: TullyMethod.c
	gcc -c TullyMethod.c -lm 
BH.o: BH.c
	gcc -c BH.c -lm
clean:
	rm -f *.o
