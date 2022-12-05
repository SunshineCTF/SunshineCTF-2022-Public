//
//  main.grsf.c
//
//  Created by Kevin Colley on 10/3/21.
//

#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <dlfcn.h>
#include "randstr.h"
#include "grs.h"

static char answers[500];
static size_t answers_length;

void addAnswer(char** answer) {
	size_t length = strlen(*answer);
	if(answers_length + length < sizeof(answers)) {
		memcpy(&answers[answers_length], *answer, length);
		answers_length += length;
	}
	
	free(*answer);
	*answer = NULL;
}

void printFlag(void) {
#define PREPARE_ENCRYPTED_FLAG 0
#if PREPARE_ENCRYPTED_FLAG
	// Horrendous hack
	const char* flag = /*GRSFRAW:"+open(os.path.join(os.path.dirname(fin.name), "flag.txt")).read().strip()+"*/"a95050.6x74543d3f213el95092.1x3c`97488.4x3a39213ds97491.3x3a3f3cM99061.5x3d3b3e213ee99113.1x3cO99145.8x533a393e3b38213ea99158.1x3c[99165.8x5c3a393e3637213el99188.1x3c_99265.1x72"/*GRSFEND*/;
	char* flag_grsf = strdup(flag);
	size_t flag_length = strlen(flag_grsf);
	
	size_t i, j;
	size_t flag_pos = 0;
	for(i = 0; i < 42; i++) {
		for(j = 0; j < answers_length; j++) {
			flag_grsf[flag_pos++] ^= answers[j];
			if(flag_pos == flag_length) {
				flag_pos = 0;
			}
		}
	}
	
	printf("Encrypted flag: \"");
	for(i = 0; i < flag_length; i++) {
		printf("\\x%02x", flag_grsf[i]);
	}
	printf("\"\n");
	return;
	
#else /* PREPARE_ENCRYPTED_FLAG */
#if 0
	Answer 1: "supercalifragilisticexpialidocious"
	Answer 2: "Mister Sprinkles" (converted to "Njtufs!Tqsjolmft")
	Answer 3: "McCormick"
	Answer 4 decoded: "yBCHHEFOO^"
	/*GRSF:yBCHHEFOO^*/grsf("f20.9x4d4c47474a49404051")/*GRSFEND*/
	Full answers array: "supercalifragilisticexpialidociousNjtufs!TqsjolmftMcCormickyBCHHEFOO^"
#endif /* 0 */
	
	const char* encrypted_flag_grsf = /*GRSFRAW:\x1e\x3d\x45\x47\x21\x48\x44\x1e\x3f\x5e\x7e\x67\x51\x39\x0c\x58\x59\x59\x43\x4c\x1d\x1e\x18\x5e\x47\x1c\x5e\x7d\x6a\x21\x40\x7a\x06\x5c\x01\x4f\x40\x17\x6e\x49\x7a\x59\x1c\x39\x4f\x5f\x01\x50\x08\x08\x65\x47\x3a\x54\x50\x09\x55\x21\x6c\x34\x71\x72\x77\x3a\x4b\x62\x0e\x04\x0c\x2b\x58\x26\x6e\x4b\x75\x3f\x38\x15\x6b\x11\x0f\x3f\x1c\x79\x3b\x65\x3f\x3b\x3c\x3f\x22\x35\x31\x70\x05\x36\x03\x05\x18\x35\x79\x34\x69\x76\x2e\x38\x6f\x27\x35\x42\x65\x21\x04\x28\x33\x76\x1f\x3c\x5d\x52\x3b\x5a\x35\x37\x74\x31\x2a\x64\x2e\x69\x0a\x3b\x2f\x78\x33\x02\x1a\x02\x62\x43\x70\x25\x19\x22\x35\x69\x43\x3d\x15\x0d\x3b\x4b\x2d\x31\x39\x62\x33\x36\x20\x2b\x75\x2c\x22\x32\x3c\x59\x6b\x15\x39\x65\x3a\x24\x6d\x2c\x73\x39\x26*/"11x11324a482e474b11305171T20.16x5e36035756564c431211175148135172g56.2x2e4ff70.6x09530e404f18Z73.1x46a75.9x56133640500e5f0707W101.7x48355b5f065a2eU114.1x3bb21624.2x3544R21625.6x010b03245729T21702.1x44^21709.3x30371aW21732.4x1e003013r21733.1x34]21740.7x303433302d3a3eg21746.6x0a390c0a173aw21819.1x3b^22162.2x2137c22169.3x283a4dO22217.4x2e0b273cc22228.8x1033525d34553a38h22281.2x3e25P22292.1x21Y22326.3x053420i22373.4x3c0d150dM22403.1x4c[22414.4x2a162d3aZ22429.9x4c321a023444223e36R22508.4x3c392f24c22518.5x232d3d3356_22538.2x1a36R22541.2x352bX22552.1x23Y22697.2x3629"/*GRSFEND*/;
	size_t flag_length = 0;
	const char* encrypted_flag = grsf_decode(encrypted_flag_grsf, NULL, &flag_length);
	char* flag_buffer = malloc(flag_length);
	memcpy(flag_buffer, encrypted_flag, flag_length);
	
	size_t i, j;
	size_t flag_pos = 0;
	for(i = 0; i < 42; i++) {
		for(j = 0; j < answers_length; j++) {
			flag_buffer[flag_pos++] ^= answers[j];
			if(flag_pos == flag_length) {
				flag_pos = 0;
			}
		}
	}
	
	char* flag = strdup(grsf(flag_buffer));
	
	printf(/*GRSF:Here's your flag: %s\n*/grsf("1x47[73877.1x28_73911.1x2f_1150528.1x2f`1168741.3x352f2a^1168744.1x05")/*GRSFEND*/, flag);
	
	free(flag);
	free(flag_buffer);
#endif /* PREPARE_ENCRYPTED_FLAG */
}

char* nextLine(FILE* fp) {
	static char line[500];
	if(!fgets(line, sizeof(line), fp)) {
		return NULL;
	}
	
	char* newline = strchr(line, '\n');
	if(newline) {
		*newline = '\0';
	}
	return strdup(line);
}

struct grsfcmp_state {
	const char* pos;
	size_t length;
	int diff;
};

void grsfcmp_cb(void* cookie, const char* chunk, size_t length) {
	struct grsfcmp_state* state = cookie;
	
	if(state->diff != 0) {
		return;
	}
	
	size_t i;
	for(i = 0; i < length && state->pos[i] != '\0'; i++) {
		state->diff |= chunk[i] - state->pos[i];
	}
	
	size_t length_compared = length;
	if(state->length < length_compared) {
		length_compared = state->length;
	}
	
	state->pos += length_compared;
	state->length -= length_compared;
}

int grsfcmp(const char* randFmt, const char* str) {
	struct grsfcmp_state state;
	state.pos = str;
	state.length = strlen(str);
	state.diff = 0;
	
	decodeRandomString(randFmt, grsfcmp_cb, &state);
	
	return state.diff;
}

bool askPassword(void) {
	printf(/*GRSF:Enter password to enter:\n*/grsf("1x4a^455598.1x2f[6985829.a9568877.1x2fi9569304.1x2f]11540064.\\11540071.2x3505")/*GRSFEND*/);
	char* line = nextLine(stdin);
	if(strcmp(line, /*GRSF:supercalifragilisticexpialidocious*/grsf("c2180346.X4600062.`5968112.U7562723.]8991031.c10154738.W11591195.]11643407.o11644797.")/*GRSFEND*/) != 0) {
		printf(/*GRSF:Invalid password!\n*/grsf("1x46]7415794.R7416682.1x2fY9353381.a9568877.2x2e05")/*GRSFEND*/);
		free(line);
		return false;
	}
	addAnswer(&line); // "supercalifragilisticexpialidocious"
	
	printf(/*GRSF:Password accepted. Hello, Dr. Sherman!\n*/grsf("1x5f^119991.Z124862.1x2fQ193749.c1456520.3x212f47W1460729.3x232f4bY1460733.3x212f5cd1936860.Z1937127.2x2e05")/*GRSFEND*/);
	return true;
}

bool questionOne(void) {
	printf(/*GRSF:What is the name of your first pet?\n*/grsf("1x58_98740.1x2f\\99364.1x2fa133486.1x2f]1574398.1x2fc1574994.1x2fj2904142.1x2f_4674491.q4674518.1x2fa4698501.2x3005")/*GRSFEND*/);
	char* line = nextLine(stdin);
	
	// Name shifted up by 1 from: Mister Sprinkles
	const char* expected = /*GRSF:Njtufs!Tqsjolmft*/grsf("1x41c2548277.o2548327.2x2e5b_2590417.a4668950.")/*GRSFEND*/;
	char* p;
	for(p = line; *p != '\0'; p++) {
		*p += 1;
	}
	
	if(strcmp(line, expected) != 0) {
		free(line);
		return false;
	}
	addAnswer(&line); // "Njtufs!Tqsjolmft"
	
	return true;
}

bool questionTwo(void) {
	printf(/*GRSF:What is your mother's maiden name?\n*/grsf("1x58_98740.1x2f\\99364.1x2f_1150528.1x2fb1227614.]1229113.1x28j1229207.1x2f`2398213.Y2398281.1x2fY3814560.2x3005")/*GRSFEND*/);
	char* line = nextLine(stdin);
	
	// This is a horrible hack that exploits my laziness of using eval() in the Python
	// code to handle escape sequences. I'm literally performing Python code injection
	// here to double-encode the string lol. Sadly, due to the way the Python code parses
	// these GRSF annotations, this all must be in one long line.
	const char* doubleEncoded =
	/*GRSFRAW:"+grsf("encode", "McCormick").decode("utf8").translate(str.maketrans("0123456789abcdefghij", "abcdefghij0123456789"))+"*/"^4246137.1x5f_4246797.1x21^4330838.2x3d55W4499669.V4499847.2x2157Q4698411.X4698595.1x21"/*GRSFEND*/;
	
	char* transposedGrsf = strdup(grsf(doubleEncoded));
	char* p;
	for(p = transposedGrsf; *p != '\0'; p++) {
		char c = *p;
		if('a' <= c && c <= 'j') {
			*p = c - 'a' + '0';
		}
		else if('0' <= c && c <= '9') {
			*p = c - '0' + 'a';
		}
	}
	
	if(grsfcmp(transposedGrsf, line) != 0) {
		free(line);
		return false;
	}
	addAnswer(&line); // "McCormick"
	
	return true;
}

bool questionThree(void) {
	printf(/*GRSF:What is the master override code?\n*/grsf("1x58_98740.1x2f\\99364.1x2fa133486.1x2f\\1204672.d1204779.1x2f]2270913.]4264632.1x2fW6040850.2x3005")/*GRSFEND*/);
	const char* end = NULL;
	char* line = nextLine(stdin);
	char* decoded = strdup(grsf_decode(line, &end, NULL));
	free(line);
	line = NULL;
	size_t length = strlen(decoded);
	
	if(*end != '\0') {
		printf(/*GRSF:Incorrect format for master override code!\n*/grsf("1x46X633889.]4307727.1x2fZ4586507.[4590119.1x2f^4610952.1x2fZ6663062.]6664510.1x2fd8871679._9666241.1x2fa9671736.2x2e05")/*GRSFEND*/);
		free(decoded);
		return false;
	}
	
	// printf("Decoded: %s\n", decoded);
	
	void* strdup_addr = dlsym(RTLD_DEFAULT, /*GRSF:strdup*/grsf("a1557746.o1558123.")/*GRSFEND*/);
	char* (*strdup_fptr)(const char*);
	memcpy(&strdup_fptr, &strdup_addr, sizeof(strdup_fptr));
	
	void* memfrob_addr = dlsym(RTLD_DEFAULT, /*GRSF:memfrob*/grsf("X256080.a259477.")/*GRSFEND*/);
	void* (*memfrob_fptr)(void*, size_t);
	memcpy(&memfrob_fptr, &memfrob_addr, sizeof(memfrob_fptr));
	
	char* mutilation = strdup_fptr(decoded);
	
#if 0
	char* frobthis = strdup("Shibboleet");
	memfrob_fptr(frobthis, strlen(frobthis));
	
	printf("Frobbed: %s\n", frobthis);
	return false;
#endif /* 0 */
	
	memfrob_fptr(mutilation, length);
	// printf("Frobbed: %s\n", mutilation);
	
	if(strcmp(mutilation, /*GRSF:Shibboleet*/grsf("1x5c_736787.V914073.l914202.")/*GRSFEND*/) != 0) {
		free(mutilation);
		free(decoded);
		return false;
	}
	
	addAnswer(&decoded); // "yBCHHEFOO^"
	
	printf(/*GRSF:Master override code accepted!\n*/grsf("1x42[1869722.m1869725.1x2f]2270913.]4264632.1x2fW6040850.1x2f[6163786.c8429647.2x2e05")/*GRSFEND*/);
	return true;
}

int challenge_main(void) {
	int ret = EXIT_FAILURE;
	
	printf(/*GRSF:Welcome to the New Game Online admin panel! Accounts are secured using MILITARY-GRADE ENCRYPTION.\n*/grsf("1x58Y42099.[44933.1x2f[44942.1x2fa133486.2x2f41]137935.2x2f48T145940.2x2f40h605412.P605440.1x2f`3678008.X3678023.1x2f\\4193475.b4193565.3x2e2f4ea5633637.^5635028.1x2f`5654758.1x2fb6042514.Z6065710.1x2f[6448024.\\6448031.28x2f424643465b4e5d5622485d4e4b4a2f4a414c5d565f5b4640412105")/*GRSFEND*/);
	
	if(!askPassword()) {
		goto out;
	}
	
	printf(/*GRSF:Suspicious login behavior detected, challenge questions must be answered for access.\n*/grsf("1x5cc679902.b1937337.k1937422.1x2f\\2922542.\\2922579.1x2f]4662374.e4734455.1x2f\\5315285.b5344880.2x232f_6123844.Z6247510.T6247546.1x2fd7565671._8365159.Z8365230.1x2fg8548610.1x2f`8549418.1x2f_8890413.\\9704760.1x2fe9767723.1x2fW9811846.p9813894.2x2105")/*GRSFEND*/);
	
	if(!questionOne()) {
		goto fail;
	}
	
	if(!questionTwo()) {
		goto fail;
	}
	
	if(!questionThree()) {
		goto fail;
	}
	
	printFlag();
	
	ret = EXIT_SUCCESS;
	
	if(0) {
fail:
		printf(/*GRSF:Incorrect answer. Access denied.\n*/grsf("1x46X633889.]4307727.1x2f_8890413.c8891900.3x212f4eb13404015.j13404019.1x2f]17508508.O17508900.2x2105")/*GRSFEND*/);
	}
	
out:
	return ret;
}

int main(void) {
	// Make sure these standard output streams are not buffered
	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stderr, NULL, _IONBF, 0);
	
	return challenge_main();
}
