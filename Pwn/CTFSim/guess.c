#include <stdio.h>
#include <stdlib.h>

int main(int argc, char** argv) {
	if(argc != 2) {
		printf("Usage: %s <seed>\n", argv[0]);
		exit(EXIT_FAILURE);
	}
	
	int seed = atoi(argv[1]);
	srand(seed);
	
	int upper;
	for(upper = 10; upper < 1000000000; upper *= 10) {
		int actual = rand() % upper + 1;
		printf("%d\n", actual);
	}
	
	return 0;
}
