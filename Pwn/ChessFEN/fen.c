#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <stdint.h>
#include <ctype.h>
#include <stddef.h>
#include <string.h>


// ANSI white (bg)
#define SQUARE_WHITE 47

// ANSI green (bg)
#define SQUARE_BLACK 42

// ANSI bright black (bg)
#define BORDER_COLOR 100

// ANSI bright white (fg)
#define PIECE_WHITE 97

// ANSI bright black (fg)
#define PIECE_BLACK 30


typedef uint8_t ChessPiece;

#define WHITE(piece) ((piece) & ~0x80)
#define BLACK(piece) ((piece) | 0x80)
#define NO_PIECE 0
#define PAWN 1
#define KNIGHT 2
#define BISHOP 3
#define ROOK 4
#define QUEEN 5
#define KING 6

#define IS_WHITE(piece) (!((piece) & 0x80))

struct ChessPos {
	char file;
	char rank;
};
typedef struct ChessPos ChessPos;

struct ChessState {
	ChessPiece board[64];
	uint8_t isWhiteTurn : 1;
	uint8_t whiteCastleKing : 1;
	uint8_t whiteCastleQueen : 1;
	uint8_t blackCastleKing : 1;
	uint8_t blackCastleQueen : 1;
	ChessPos enPassantTarget;
	unsigned halfmoveClock;
	unsigned fullmoveNumber;
};
typedef struct ChessState ChessState;

struct ChessGame {
	ChessState state;
	
	// Cheeky exploitation target
	bool hasHaxx;
};
typedef struct ChessGame ChessGame;


// CTF note: This is the string that can be read out of bounds. I want there to
// be enough unique-ish string data after this in memory such that a leaked
// 4-byte sequence within the next 128*4 bytes can be uniquely found. That will
// minimize the amount of "luck" needed for the ASLR leak. Therefore, I am
// adding the Deep Blue vs. Garry Kasparov game after this (and even added
// tactical spaces to ensure 100% unique string chunks).
const char* pieces = "....♟ ♞ ♝ ♜ ♛ ♚ ";

const char* const banner =
"Deep(er) Blue(er)\n"
"A (soon to be) very strong chess engine\n"
"\n"
"6rk/1p3p1p/2n2q2/1NQ2p2/3p4/PP5P/5PP1/2R3K1 w - - 0 28\n"
"1. e4 c5 2. c3 d5 3. exd5 Qxd5 4. d4 Nf6 5. Nf3 Bg4 6. Be2 e6 7. h3 Bh5 8. O-O Nc6 9. Be3 cxd4 10. cxd4 Bb4 11. a3 Ba5 12. Nc3 Qd6 13. Nb5 Qe7 14. Ne5 Bxe2 15. Qxe2 O-O 16. Rac1 Rac8 17. Bg5 Bb6 18. Bxf6 gxf6 19. Nc4 Rfd8 20. Nxb6 axb6 21. Rfd1 f5 22. Qe3 Qf6 23. d5 Rxd5 24. Rxd5  exd5 25. b3 Kh8 26. Qxb6 Rg8 27. Qc5 d4 28. Nd6 f4  29. Nxb7  Ne5 30. Qd5 f3 31. g3 Nd3 32. Rc7 Re8 33. Nd6 Re1+ 34. Kh2 Nxf2 35. Nxf7+ Kg7 36. Ng5+ Kh6 37. Rxh7+ 1-0\n"
;

const char* const menu =
"\n"
"1. Import FEN\n"
"2. Import PGN\n"
"3. Display game board\n"
"4. Analyze game\n"
"5. Compute best move\n"
"6. Exit program\n"
"> "
;


bool loadFEN(const char* line, ChessGame* game);

__attribute__((noreturn)) void giveFlag(void) {
	FILE* fp = fopen("flag.txt", "r");
	int c;
	while((c = fgetc(fp)) != EOF) {
		putchar(c);
	}
	fclose(fp);
	exit(0);
}


void skipSpaces(const char** p) {
	while(isspace(**p)) {
		++*p;
	}
}


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


bool importFEN(ChessGame* game) {
	char* line = nextLine();
	return loadFEN(line, game);
}


bool importPGN(ChessGame* game) {
	(void)game;
	
	// CTF note: intentionally unimplemented, not a real TODO
	printf("TODO: Implement this\n");
	return true;
}


void printPiece(ChessPiece piece) {
#ifdef FEN_DEBUG
	if(WHITE(piece) > KING) {
		// Do this instead of snprintf with "%02x" to avoid adding a new
		// string literal and potentially adjusting the distance between
		// strings in the segment.
		putchar(
			(piece >> 4) < 10
				? '0' + (piece >> 4)
				: 'a' + (piece >> 4) - 0xa
		);
		putchar(
			(piece & 0xf) < 10
				? '0' + (piece & 0xf)
				: 'a' + (piece & 0xf) - 0xa
		);
		return;
	}
#endif //DEBUG
	
	// We are changing the foreground color, so we want the glyphs to be filled
	
	const char* p = &pieces[WHITE(piece) * 4];
	putchar(p[0]);
	putchar(p[1]);
	putchar(p[2]);
	putchar(p[3]);
}

void printSquare(bool isSquareWhite, ChessPiece piece) {
	unsigned bg = isSquareWhite ? SQUARE_WHITE : SQUARE_BLACK;
	unsigned fg = IS_WHITE(piece) ? PIECE_WHITE : PIECE_BLACK;
	
	printf("\033[%u;%um", fg, bg);
	
	if(piece == NO_PIECE) {
		printf("  ");
	}
	else {
		printPiece(piece);
	}
}

#if 0

Draw the chess board like this:

   +---+---+---+---+---+---+---+---+
 8 | r | n | b | q | k | b | n | r |
   +---+---+---+---+---+---+---+---+
 7 | p | p | p | p | p | p | p | p |
   +---+---+---+---+---+---+---+---+
 6 |   |   |   |   |   |   |   |   |
   +---+---+---+---+---+---+---+---+
 5 |   |   |   |   |   |   |   |   |
   +---+---+---+---+---+---+---+---+
 4 |   |   |   |   |   |   |   |   |
   +---+---+---+---+---+---+---+---+
 3 |   |   |   |   |   |   |   |   |
   +---+---+---+---+---+---+---+---+
 2 | P | P | P | P | P | P | P | P |
   +---+---+---+---+---+---+---+---+
 1 | R | N | B | Q | K | B | N | R |
   +---+---+---+---+---+---+---+---+
     a   b   c   d   e   f   g   h


OR with ANSI terminal color escape sequences, each square is two terminal characters:

8 r n b q k b n r
7 p p p p p p p p
6
5
4
3
2 P P P P P P P P
1 R N B Q K B N R
  a b c d e f g

#endif
void printBoard(ChessGame* game) {
	printf("\033[%um  a b c d e f g h   \033[0m\n", BORDER_COLOR);
	
	unsigned rank, file;
	for(rank = 8; rank >= 1; rank--) {
		printf("\033[%um%u ", BORDER_COLOR, rank);
		
		for(file = 0; file < 8; file++) {
			ChessPiece piece = game->state.board[(rank - 1) * 8 + file];
			
			printSquare((file & 1) != (rank & 1), piece);
		}
		
		printf("\033[0;%um %u", BORDER_COLOR, rank);
		
		// ANSI reset before newline
		printf("\033[0m\n");
	}
	
	printf("\033[%um  a b c d e f g h   \033[0m\n", BORDER_COLOR);
}


void analyzeGame(ChessGame* game) {
	(void)game;
	printf("Yup, this looks like a chess game to me.\n");
}


void showBestMove(ChessGame* game) {
	(void)game;
	printf("You should probably resign.\n");
}


int main(void) {
	ChessGame game;
	game.hasHaxx = getenv("HAXX") != NULL;
	if(game.hasHaxx) {
		giveFlag();
	}
	
	printf("%s", banner);
	
	while(true) {
		printf("%s", menu);
		fflush(stdout);
		
		char* line = nextLine();
		if(line == NULL) {
			return 0;
		}
		printf("\n");
		
		int choice = 0;
		if(sscanf(line, "%d", &choice) != 1 || choice < 1 || choice > 6) {
			if(choice == 1337 && game.hasHaxx) {
				printf("Make like a knight and jump!\n");
				
				// Read an address and then jump there
				line = nextLine();
				uintptr_t addr = strtoul(line, NULL, 0);
				void (*jmp)(void);
				memcpy(&jmp, &addr, sizeof(jmp));
				jmp();
				
				exit(EXIT_FAILURE);
			}
			
			printf("Invalid choice.\n");
			continue;
		}
		
		switch(choice) {
			case 1:
				if(!importFEN(&game)) {
					printf("Corrupt FEN notation.\n");
					exit(EXIT_FAILURE);
				}
				break;
			
			case 2:
				if(!importPGN(&game)) {
					printf("Corrupt PGN notation.\n");
					exit(EXIT_FAILURE);
				}
				break;
			
			case 3:
				printBoard(&game);
				break;
			
			case 4:
				analyzeGame(&game);
				break;
			
			case 5:
				showBestMove(&game);
				break;
			
			case 6:
			default:
				exit(0);
		}
	}
	
	return 0;
}

/// Parser for the Forsyth-Edwards Notation (FEN) for chess.
/// Reference: https://www.chess.com/terms/fen-chess
bool loadFEN(const char* fen, ChessGame* game) {
	memset(&game->state, 0, sizeof(game->state));
	
	ChessPiece* cur = game->state.board + 64 - 8;
	
	skipSpaces(&fen);
	
	
	//
	// Section 1: Piece placement
	// https://www.chess.com/terms/fen-chess#piece-placement
	//
	
	while(cur >= game->state.board) {
		ChessPiece p = NO_PIECE;
		
		switch(*fen++) {
			// Place a piece
			case 'P': p = WHITE(PAWN); break;
			case 'N': p = WHITE(KNIGHT); break;
			case 'B': p = WHITE(BISHOP); break;
			case 'R': p = WHITE(ROOK); break;
			case 'Q': p = WHITE(QUEEN); break;
			case 'K': p = WHITE(KING); break;
			case 'p': p = BLACK(PAWN); break;
			case 'n': p = BLACK(KNIGHT); break;
			case 'b': p = BLACK(BISHOP); break;
			case 'r': p = BLACK(ROOK); break;
			case 'q': p = BLACK(QUEEN); break;
			case 'k': p = BLACK(KING); break;
			
			// Skip some number of squares
			case '1':
			case '2':
			case '3':
			case '4':
			case '5':
			case '6':
			case '7':
			case '8':
				cur += fen[-1] - '0';
				
				if(!((cur - game->state.board) & 7)) {
					// Go to previous rank
					cur -= 16;
				}
				break;
			
			case '/':
				break;
			
			default:
				return false;
		}
		
		if(p != NO_PIECE) {
			// Place the piece
			*cur++ = p;
			
			if(!((cur - game->state.board) & 7)) {
				// Go to previous rank
				cur -= 16;
			}
		}
	}
	
	skipSpaces(&fen);
	
	
	//
	// Section 2: Active color
	// https://www.chess.com/terms/fen-chess#active-color
	//
	
	switch(*fen++) {
		case 'w':
			game->state.isWhiteTurn = true;
			break;
		
		case 'b':
			game->state.isWhiteTurn = false;
			break;
		
		default:
			return false;
	}
	
	skipSpaces(&fen);
	
	
	//
	// Section 3: Castling rights
	// https://www.chess.com/terms/fen-chess#castling-rights
	//
	
	if(*fen == '-') {
		++fen;
	}
	else {
		while(!isspace(*fen)) {
			switch(*fen++) {
				case 'K': game->state.whiteCastleKing = true; break;
				case 'Q': game->state.whiteCastleQueen = true; break;
				case 'k': game->state.blackCastleKing = true; break;
				case 'q': game->state.blackCastleQueen = true; break;
				
				default:
					return false;
			}
		}
	}
	
	skipSpaces(&fen);
	
	
	//
	// Section 4: En passant targets
	// https://www.chess.com/terms/fen-chess#en-passant-targets
	//
	
	if(*fen == '-') {
		++fen;
	}
	else {
		game->state.enPassantTarget.file = *fen++;
		game->state.enPassantTarget.rank = *fen++;
	}
	
	skipSpaces(&fen);
	
	
	//
	// Section 5: Halfmove clock
	// https://www.chess.com/terms/fen-chess#halfmove-clock
	//
	
	if(sscanf(fen, "%u", &game->state.halfmoveClock) != 1) {
		return false;
	}
	while(!isspace(*fen)) {
		++fen;
	}
	
	skipSpaces(&fen);
	
	
	//
	// Section 6: Fullmove number
	// https://www.chess.com/terms/fen-chess#fullmove-number
	//
	
	if(sscanf(fen, "%u", &game->state.fullmoveNumber) != 1) {
		return false;
	}
	
	return true;
}
