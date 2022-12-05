#define NROWS 15
#define NCOLS 15

#define ARRSZ(arr) (sizeof(arr)/sizeof((arr)[0]))

#define _GETBIT(arr, i) (((arr)[(i)>>3] >> ((i)&7)) & 1)
#define GETBIT(arr, r, c) _GETBIT(arr, (r)*NCOLS+(c))

#define _SETBIT(arr, i) ((arr)[(i)>>3] |= 1 << ((i)&7))
#define SETBIT(arr, r, c) _SETBIT(arr, (r)*NCOLS+(c))

#define _CLRBIT(arr, i) ((arr)[(i)>>3] &= ~(1 << ((i)&7)))
#define CLRBIT(arr, r, c) _CLRBIT(arr, (r)*NCOLS+(c))

#define UP 0
#define RIGHT 1
#define DOWN 2
#define LEFT 3
int dirs[4][2] = {{-1, 0}, {0, 1}, {1, 0}, {0, -1}};

//===============================================
// game state

// bitmaps
unsigned char apple[(NROWS*NCOLS+7)/8];
unsigned char snake[(NROWS*NCOLS+7)/8];

short head_r, head_c;
unsigned int head_dir;

unsigned int score, high_score, high_score_chaos;

int g_rand;

unsigned short hist_head, hist_tail;
unsigned char history[NROWS*NCOLS];

char reserved_data[170];

int (*move_snake)(int, int);

//===============================================


#include "util.h"
#include "display.h"



void srand(int seed) {
    g_rand = seed;
}
int rand() {
    g_rand = (g_rand * 1103515245) + 12345;
    return g_rand;
}

void spawn_apple() {
    int loc;
    do {
        loc = rand();

        // ensure the index is not negative before the signed modulo
        if (loc < 0)
            loc = -loc;

        loc = loc % (NROWS*NCOLS);
    } while (_GETBIT(snake, loc) || _GETBIT(apple, loc));
    _SETBIT(apple, loc);
}

int do_tick() {
    int nr = head_r + dirs[head_dir][0];
    int nc = head_c + dirs[head_dir][1];

    // allow wrapping through walls
    if (nr == NROWS)
        nr = 0;
    else if (nr == -1)
        nr = NROWS-1;
    if (nc == NCOLS)
        nc = 0;
    else if (nc == -1)
        nc = NCOLS-1;

    int ret = move_snake(nr, nc);
    if (!ret)
        return 0;
    
    SETBIT(snake, nr, nc);
    head_r = nr;
    head_c = nc;
    history[hist_head] = head_r*NCOLS + head_c;
    if (++hist_head == ARRSZ(history))
        hist_head = 0;

    for (int i = 0; i < ret-1; i++)
        spawn_apple();

    return 1;
}

int move_snake_chaos(int nr, int nc) {
    int got_apple = GETBIT(apple, nr, nc);
    int nclrs = 0;
    if (!got_apple) {
        // check game over
        if (GETBIT(snake, nr, nc))
            return 0;
        score++;
        nclrs = !!(score % 2 == 0);
    } else {
        CLRBIT(apple, nr, nc);
        score += 10;
        short hist_length;
        if (hist_head < hist_tail)
            hist_length = hist_head+ARRSZ(history) - hist_tail;
        else
            hist_length = hist_head - hist_tail;
        nclrs = hist_length/7;
    }

    for (int i = 0; i < nclrs; i++) {
        _CLRBIT(snake, history[hist_tail]);
        if (++hist_tail == ARRSZ(history))
            hist_tail = 0;
    }

    return 1 + got_apple;
}

int move_snake_normal(int nr, int nc) {
    int got_apple = GETBIT(apple, nr, nc);
    if (!got_apple) {
        _CLRBIT(snake, history[hist_tail]);

        // check game over
        if (GETBIT(snake, nr, nc)) {
            _SETBIT(snake, history[hist_tail]);
            return 0;
        }

        if (++hist_tail == ARRSZ(history))
            hist_tail = 0;
    } else {
        CLRBIT(apple, nr, nc);
        score++;
    }

    return 1 + got_apple;
}

void init_state(int chaos) {
    srand(*(int*)&snake[0]);
    memset(snake, 0, sizeof(snake));
    memset(apple, 0, sizeof(apple));
    memset(history, 0, sizeof(history));
    score = 0;
    head_r = 7;
    head_c = 1;
    head_dir = 1;
    hist_head = hist_tail = 0;
    for (int i = 0; i < 3; i++) {
        head_c++;
        SETBIT(snake, head_r, head_c);
        history[hist_head++] = head_r*NCOLS + head_c;
    }
    spawn_apple();
    if (chaos) {
        spawn_apple();
        spawn_apple();
    }
    move_snake = chaos ? move_snake_chaos : move_snake_normal;
}

#define TICK 100000
void game_loop(int dbg, int chaos) {
    fd_set rfds;
    FD_ZERO(&rfds);
    
    init_state(chaos);

    // game loop
    int game_over = 0;
    while (!game_over) {
        long tick_start = current_time();
        long tick_end = tick_start + TICK;
        struct timeval timeout = {0, TICK};
        int tick_done = 0;

        while (!tick_done) {
            print_board(chaos);

            FD_SET(0, &rfds);
            int ret = dbg ? 1 : select(1, &rfds, 0, 0, &timeout);

            // timeout expired (no user input)
            if (!ret)
                tick_done = 1;
            else if (ret < 0) {
                writestr("EOF\n");
                exit(1);
            } else {
                // note arrow keys translated to wasd
                char op = getchar();
                if (op == 'w') {
                    if (head_dir != DOWN) {
                        head_dir = UP;
                        tick_done = 1;
                    }
                } else if (op == 'a') {
                    if (head_dir != RIGHT) {
                        head_dir = LEFT;
                        tick_done = 1;
                    }
                }
                else if (op == 's') {
                    if (head_dir != UP) {
                        head_dir = DOWN;
                        tick_done = 1;
                    }
                } else if (op == 'd') {
                    if (head_dir != LEFT) {
                        head_dir = RIGHT;
                        tick_done = 1;
                    }
                } else if (op == '/') {
                    dbg = !dbg;
                    break;
                } else if (op == 'q') {
                    game_over = 1;
                    break;
                }
            }

            long cur_time;
            if (tick_done || (!dbg && (cur_time = current_time()) >= tick_end)) {
                tick_done = 1;
                game_over = !do_tick();
            } else if (!dbg) {
                timeout.tv_sec = 0;
                timeout.tv_usec = tick_end-cur_time;
            }
        }
    }

    print_game_over(chaos);
    if (chaos && score > high_score_chaos)
        high_score_chaos = score;
    else if (!chaos && score > high_score)
        high_score = score;
    writestr("press enter to continue...\n");
    while (getchar() != '\n');
}

int main() {
    int menu_sel = 0, dbg = 0;
    init_state(0);
    while (1) {
        print_board(menu_sel);
        print_main_menu(menu_sel);
        char op = getchar();
        // note arrow keys translated to wasd
        if (op == '\n') {
            if (menu_sel == 0 || menu_sel == 1) {
                game_loop(dbg, menu_sel);
                dbg = 0;
            }
            else
                break;
        }
        else if (op == 'w') {
            if (menu_sel)
                menu_sel--;
        }
        else if (op == 's') {
            if (menu_sel < 2)
                menu_sel++;
        } else if (op == '/')
            dbg = !dbg;
    }
    return 0;
}
