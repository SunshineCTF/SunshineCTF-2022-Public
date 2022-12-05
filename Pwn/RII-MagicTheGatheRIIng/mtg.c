// Exploit. Overwrite the name of one of the computer's cards
//   so we can puts(puts) and get a libc address. Then, since they
//   will be given a libc binary, they could find a magic gadget
//   using relative offsets and overwrite the return address with that.
//   May require padding/alignment since not whole struct is controllable.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#include "mtg.h"


void print_menu() {
    puts("Simplified Magic the GatheRIIng");
    puts("1. Rules");
    puts("2. Load player cards");
    puts("3. Play! (slow mode)");
    puts("4. Play! (fast mode)");
    puts("5. Exit");
    printf("> ");
    fflush(stdout);
}

void print_rules() {
    puts("");
    puts(
        "Magic the Gathering (MTG) is an exciting game full of strategy, skills,\n"
        "abilities, spells, and more. That strategy also extends to deckbuilding\n"
        "- choosing what cards work well together and align with your playing style.\n\n"
        
        "But for today, we've made a beginner version that simply focuses on combat\n"
        "and mana generation. IF YOU'VE PLAYED MTG ALREADY, FORGET WHAT YOU KNOW.\n\n"

        "DECKBUILDING:\n"
        "We've taken care of the deckbuilding for you. We randomly generate both the\n"
        "CPU and Player decks with a mix of mana cards and creature cards. Each deck\n"
        "consists of 20 cards. Decks are only randomly generated once, and will remain\n"
        "the same if playing multiple games. Small amounts of customization to decks\n"
        "may be done by uploading individual cards.\n\n"

        "MANA:\n"
        "Mana is the resource used to cast spells. In these decks, the only spells\n"
        "available are Creature spells. Mana is created by Land cards, which are\n"
        "laid on the table in front of you. Each Land can produce 1 mana per turn.\n"
        "Your mana regenerates at the beginning of your turn. Each spell has an\n"
        "associated mana cost required to cast that spell.\n\n"

        "CREATURES:\n"
        "All creatures have a power (offense) and a toughness (defense) represented\n"
        "as two numbers separated with a slash. E.g., a Creature marked (3/2) has three\n"
        "power and two toughness. For simplicity, toughness is ignored in this game.\n"
        "Blocking and other combat mechanisms are also excluded; when a Creature is cast,\n"
        "it does damage equal to its power to the opposing player, and then is immediately"
        "discarded.\n"

        "TURN FORMAT:\n"
        "Turns begin by drawing a card from your deck. If it is a mana card, it is immediately\n"
        "played and the turn is over. If it is a Creature, the cost of the creature is\n"
        "compared to the available mana from previously played mana cards. If not enough mana\n"
        "is available, the Creature is discarded and the turn ends. Otherwise, the Creature\n"
        "is successfully cast and immediately attacks the opposing player. It does damage\n"
        "equal to its power, and then is immediately discarded. Due to this highly automated\n"
        "format, you don't actually get to make any decisions during the game. As such, both\n"
        "a \"human speed\" and a \"computer speed\" option for playing are available - just\n"
        "in case you're in a time crunch.\n\n"

        "WINNING:\n"
        "A player wins if:\n"
        "1) The opposing player goes to draw a card and no cards are available.\n"
        "2) The opposing player's health reaches 0 or less. Players begin with 20 HP.\n\n"

        "KEY DIFFERENCES TO REAL MTG:\n"
        "* Cards are not retained in hands.\n"
        "* No summoning sickness.\n"
        "* Creatures do not stay on the battlefield for multiple turns.\n"
        "* No blocking during combat."
    );
    puts("");
}

char *card_repr(Card *card) {
    char *format;
    if (card->type == MANA) {
        format = "Drew %s\n";
    }
    else {
        format = "Drew %s (%u/%u) Cost: %u\n";
    }
    int needed = snprintf(NULL, 0, format, card->name, card->power, card->toughness, card->cost);
    if (needed == -1) {
        puts("sprintf error");
        exit(1);
    }
    char *buf = malloc(needed + 1);
    if (!buf) {
        puts("malloc error");
        exit(1);
    }
    needed = snprintf(buf, needed, format, card->name, card->power, card->toughness, card->cost);
    buf[needed] = '\0';

    return buf;
}

int parse_line(Deck player_deck, char *line) {
    int8_t index = 0;
    char card_type = 'x';
    char name[0x20] = {0};
    uint32_t cost = 0;
    uint32_t power = 0;
    uint32_t toughness = 0;

    // Remove dangling newline if there
    if (line[strlen(line) - 1] == '\n') {
        line[strlen(line) - 1] = '\0';
    }

    if (sscanf(line, "%hhd %c %s %d %d %d", &index, &card_type, name, &cost, &power, &toughness) != 6) {
        // printf("Error parsing line: \"%s\"\n", line);
        return 1;
    }

    if (card_type != 'm' && card_type != 'c') {
        // printf("Invalid card type \"%c\"\n", card_type);
        return 1;
    }

    // Store card info in the player deck
    // BUG: index allows somewhat of a write-what-where
    // But values only allow complete control of every third qword
    Card *card = &player_deck[index];
    card->name = strdup(name);
    card->type = (card_type == 'm') ? MANA : CREATURE;
    card->cost = cost;
    // Set these, even though they mean nothing if it's a mana card
    card->power = power;
    card->toughness = toughness;

    return 0;
}

int load_cards(Deck player_deck) {
    static unsigned int cards_loaded = 0;
    const unsigned int MAXIMUM_CARDS = 2;

    if (cards_loaded >= MAXIMUM_CARDS) {
        puts("Already loaded maximum number of cards!");
        return 0;
    }
    puts("Enter cards:");

    // Just read in whole decklist at once
    while (cards_loaded < MAXIMUM_CARDS) {
        char *line = NULL;
        ssize_t bytes_read = 0;
        bytes_read = getline(&line, &bytes_read, stdin);

        if (bytes_read == -1) {
            // Done reading, or failed to read
            return 0;
        }

        if (bytes_read == 1) {
            // Only read a newline character, so stop
            break;
        }

        if (parse_line(player_deck, line)) {
            puts("Invalid card data");
            return 1;
        }
        cards_loaded += 1;
    }

    return 0;
}

void draw_board(char *message, Player *player, Player *cpu, unsigned int human_turn) {
    if (human_turn) {
        printf("                 CPU (HP: %d)                        \n", cpu->hp);
    }
    else{
        printf("                *CPU (HP: %d)*                       \n", cpu->hp);
    }
    printf("Mana: %u                  Cards in deck:  %u\n", cpu->current_mana, DECK_SIZE - cpu->deck_index);
    puts("");
    puts("");
    printf("      %s\n", message);
    puts("");
    puts("");
    printf("Mana: %u                  Cards in deck:  %u\n", player->current_mana, DECK_SIZE - player->deck_index);
    if (human_turn) {
        printf("              *PLAYER (HP: %d)*                      \n", player->hp);
    }
    else {
        printf("               PLAYER (HP: %d)                      \n", player->hp);
    }
    puts("==============================================================");
    puts("\n");
}

void init_player(Player *player, Deck deck) {
    player->deck = deck;
    player->current_mana = 0;
    player->max_mana = 0;
    player->deck_index = 0;
    player->hp = 10;
}

int do_turn(unsigned int delay, Player *human, Player *cpu, int human_turn) {
    // Return 0 - No outcome
    // Return 1 - Player wins
    // Return 2 - CPU wins
    Player *current_player = human_turn ? human : cpu;
    Player *other_player = human_turn ? cpu : human;
    char *msg = human_turn ? "Your turn!" : "CPU Turn!";
    sleep(delay);
    current_player->current_mana = current_player->max_mana;
    draw_board(msg, human, cpu, human_turn);
    sleep(delay);
    draw_board("Drawing!", human, cpu, human_turn);
    sleep(delay);
    if (current_player->deck_index == DECK_SIZE) {
        draw_board("Ran out of cards to draw!", human, cpu, human_turn);
        return 1;
    }
    Card card = current_player->deck[current_player->deck_index];
    current_player->deck_index += 1;
    char *buf = card_repr(&card);
    draw_board(buf, human, cpu, human_turn);
    free(buf);
    buf = NULL;
    sleep(delay);
    if (card.type == MANA) {
        current_player->max_mana += 1;
        current_player->current_mana = current_player->max_mana;
    }
    else {
        if (current_player->current_mana >= card.cost) {
            current_player->current_mana -= card.cost;
            draw_board("Casting and attacking with creature!", human, cpu, human_turn);
            sleep(delay);
            other_player->hp -= card.power;
            if (other_player->hp <= 0) {
                msg = human_turn ? "You win!" : "You lose!";
                draw_board(msg, human, cpu, human_turn);
                sleep(delay);
                int result = human_turn? 1 : 2;
                return result;
            }
        }
        else {
            draw_board("Not enough mana... discarding creature", human, cpu, human_turn);
            sleep(delay);
        }
    }
    return 0;
}

int play(unsigned int delay, Deck player_deck, Deck cpu_deck) {
    // Return 0 if CPU wins, 1 if player wins
    Player human;
    Player cpu;
    unsigned int human_turn = 0;
    init_player(&human, player_deck);
    init_player(&cpu, cpu_deck);
    char *msg;

    draw_board("New game!", &human, &cpu, human_turn);
    while(1) {
        human_turn = 0;
        if (do_turn(delay, &human, &cpu, human_turn)) {
            return 0;
        }
        human_turn = 1;
        if (do_turn(delay, &human, &cpu, human_turn)) {
            return 0;
        }
    }
    return 0;
}

void init_deck(Deck deck, unsigned int min_stat, unsigned int max_stat, unsigned int min_cost, unsigned int max_cost) {
    for (int i = 0; i < DECK_SIZE; i++) {
        Card *card = &deck[i];
        if (rand() % 2) {
            // 50/50 make mana card
            card->type = MANA;
            card->name = "Basic Land";
            card->cost = 0;
            card->power = 0;
            card->toughness = 0;
        }
        else {
            // 50/50 make creature card
            card->type = CREATURE;
            card->name = "Basic Troll";
            card->cost = rand() % (max_cost - min_cost) + min_cost;
            card->power = rand() % (max_stat - min_stat) + min_stat;
            card->toughness = rand() % (max_stat - min_stat) + min_stat;
        }
    }
}

void init_player_deck(Deck player_deck) {
    init_deck(player_deck, 1, 4, 1, 5);
}

void init_cpu_deck(Deck cpu_deck) {
    init_deck(cpu_deck, 3, 7, 1, 5);
}

int main(void) {
    // Put in a struct to avoid reordering
    struct local_vars {
        Card player_deck[DECK_SIZE];
        unsigned long int selection;
        unsigned long int anchor;
        Card cpu_deck[DECK_SIZE];
        unsigned long int anchor2;
    } vars;

    vars.anchor = 0xDEADBEEFCAFEBABE;
    vars.anchor2 = 0xF00DF00DF00DF00D;
    vars.selection = 0;

    // Time(NULL) is red herring - not a problem because beating the CPU has nothing to do with the challenge
    srand(time(NULL));
    init_player_deck(vars.player_deck);
    init_cpu_deck(vars.cpu_deck);


    do {
        vars.selection = 0;
        print_menu();
        if (scanf(" %ld", &vars.selection) != 1) {
            puts("Error getting input");
            exit(1);
        }

        // Eat remaining newline
        getchar();
        // __asm__("int3");
        switch(vars.selection) {
            case 1:
                print_rules();
                break;

            case 2:
                load_cards(vars.player_deck);
                break;

            case 3:
                // if(play(2, vars.player_deck, vars.cpu_deck)) {
                //     puts("Error while playing game");
                //     exit(1);
                // }
                play(2, vars.player_deck, vars.cpu_deck);
                break;

            case 4:
                if(play(0, vars.player_deck, vars.cpu_deck)) {
                    puts("Error while playing game");
                    exit(1);
                }
                break;

            case 5:
                // Clear out RCX so one_gadget works
                __asm__("xor %rsi, %rsi");
                __asm__("xor %rdx, %rdx");
                return 0;

            default:
                puts("Invalid selection");
        }
    } while (1);

    return 0;
}
