#include <stdio.h>
#include <stdlib.h>
#include <stddef.h>
#include <sys/types.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>


typedef struct GuessState {
	char name[20];
	int seed;
} GuessState;

GuessState gs;


char g_line[1000];
char* nextLine(void) {
	if(!fgets(g_line, sizeof(g_line), stdin)) {
		return NULL;
	}
	
	char* p = strchr(g_line, '\n');
	if(p != NULL) {
		*p = '\0';
	}
	
	return g_line;
}


int main(void) {
	int fd = open("/dev/urandom", O_RDONLY);
	if(fd < 0 || read(fd, &gs.seed, sizeof(gs.seed)) != sizeof(gs.seed)) {
		printf("Fatal error!\n");
		exit(EXIT_FAILURE);
	}
	close(fd);
	srand(gs.seed);
	
	printf("||| CTF Simulator 2022 |||\n");
	printf("This CTF training simulator will hone your guessing skills so you can be more competitive in CTF competitions!\n");
	
	printf("What's the name of your CTF team?\n[>] ");
	fflush(stdout);
	
	char* line = nextLine();
	if(!line) {
		printf("Invalid team name!\n");
		exit(EXIT_FAILURE);
	}
	strncpy(gs.name, line, sizeof(gs.name));
	
	int upper;
	for(upper = 10; upper < 1000000000; upper *= 10) {
		printf("Okay %s, I'm thinking of a number between 1 and %d. What is it?\n[>] ", gs.name, upper);
		fflush(stdout);
		
		int actual = rand() % upper + 1;
		int guess = 0;
		
		line = nextLine();
		if(sscanf(line, "%d", &guess) != 1) {
			printf("Bad guess!\n");
			exit(EXIT_FAILURE);
		}
		
		if(guess < actual) {
			printf("Too low!\n");
			exit(EXIT_FAILURE);
		}
		else if(guess > actual) {
			printf("Too high!\n");
			exit(EXIT_FAILURE);
		}
		else {
			printf("That's it!\n");
		}
	}
	
	printf("Wow, did you hack into my brain? Great guessing! You'll be a CTF star in no time!\n");
	
	FILE* fp = fopen("flag.txt", "r");
	if(!fp) {
		printf("Flag file is missing!\n");
		exit(EXIT_FAILURE);
	}
	
	char flag[100];
	if(!fgets(flag, sizeof(flag), fp)) {
		printf("Error reading from flag file!\n");
		exit(EXIT_FAILURE);
	}
	fclose(fp);
	
	char* p = strchr(flag, '\n');
	if(p) {
		*p = '\0';
	}
	
	printf("Here's a reward for you: %s\n", flag);
	return 0;
}
