
const unsigned int DECK_SIZE = 20;

enum card_t {
    MANA,
    CREATURE,
};

typedef enum card_t CardType;

struct card {
    char *name;
    CardType type;
    unsigned int cost;
    // Power/Toughness only have meaning when type is a creature
    unsigned int power;
    unsigned int toughness;
};
typedef struct card Card;
typedef Card *Deck;

struct player {
    Deck deck;
    // Pointer to index of "top of deck"
    unsigned int deck_index;
    unsigned int max_mana;
    unsigned int current_mana;
    int hp;
};

typedef struct player Player;