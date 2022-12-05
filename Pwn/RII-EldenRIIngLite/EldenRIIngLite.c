#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

/* `name` basically serves no purpose, it's just padding that
gives the user a reason to be able to write to the `key` entry
when this struct is allocated as a chunk of memory. */
typedef struct _Unpolished
{
    char *name;
    char *departing_message;
} Unpolished;

long int warden_runes = 3200;
long int mergot_runes = 12000;
long int aethelwulf_runes = 20000;

/* Simple setup function to make heap allocations more predictable. */
void setup()
{
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

/* New player constructor. `player->name` essentially serves as
padding to allow the usage of `player->departing_message` as the
mechanism to write to the tcache. */
Unpolished *new_player()
{
    size_t bytes_read = 0;
    Unpolished *player = (Unpolished *) malloc(sizeof(Unpolished));
    player->name = (char *) malloc(sizeof(char) * 32);
    player->departing_message = (char *) malloc(sizeof(char) * 256);
    printf("Brave Unpolished, what is thy name? : ");
    bytes_read = read(0, player->name, sizeof(char) * 32);
    if(bytes_read == 0)
        return NULL;
    player->name[bytes_read - 1] = '\0';
    return player;
}

/* First boss for the user to beat. Facilitates the execution of the
found magic gadget. */
int first_boss()
{
    char *msg = NULL;
    int choice = 0;
    char leave_msg = '\0';
    long *dropped_runes = &warden_runes;
    puts("As you travel the lands of Dimgrave, a large, golden spectacle " \
    "manifests itself before you: a Botanic Warden upon his steed.\nYou " \
    "enter his line of sight, and combat initiates.\n");
    puts("The Botanic Warden charges you, his halberd ready to cleave " \
    "you in half! Think quickly, Unpolished!");
    printf("1. Drink from the Bottle of Amazing Power\n" \
    "2. Run in the opposite direction whilst summoning Typhoon, your steed\n" \
    "3. Attempt to parry the incoming strike\n: ");

    scanf("%d", &choice);

    switch(choice)
    {
        case 1:
            puts("\nYou uncork your bottle and take a swig of the miraculous " \
            "elixir. While the taste is sublime, you cannot help but " \
            "notice that you are now in two pieces thanks to the Warden's " \
            "halberd. Perhaps you should have been quicker...");
            return 1;
        case 2:
            puts("\nYou whistle to summon Typhoon. As the steed appears before " \
            "you from thin air, you make a running leap onto the saddle, " \
            "narrowly avoiding the enormous swing of the Warden's halberd.\n");
            break;
        case 3:
            puts("\nYou repeatedly swing your shield in a panicked attempt " \
            "to parry the incoming blow. You exhaust your stamina, leaving " \
            "yourself completely vulnerable, resulting in your demise.");
            return 1;
        default:
            puts("\nYou freeze in terror, the Warden lops your head off, " \
            "and he leaves feeling more confused than victorious.");
            return 1;
    }

    puts("As you turn Typhoon to face the Warden, you draw your armament and " \
    "prepare to strike...\n\nAfter some intense fighting on horseback, it's " \
    "evident that the Warden is almost defeated.\n");
    puts("In a final attempt to secure victory, the Warden makes a high jump " \
    "into the air and directs his shield towards you, performing a powerful " \
    "plunging attack. How shall you proceed?");
    printf("1. Dash out of the way and strike the Warden\n" \
    "2. Attempt to tank the attack and follow up with a flourish\n" \
    "3. Cast thunderbolt against the Warden\n: ");

    scanf("%d", &choice);

    switch(choice)
    {
        case 1:
            puts("\nYou mistime your dash and lose your i-frames precisely at the " \
            "moment the shield flattens you. You are now a pancake.");
            return 1;
        case 2:
            puts("\n\"I should have invested more skill points into Vigor\", you " \
            "think to yourself as you fail to endure the hit.");
            return 1;
        case 3:
            puts("\nYou conjure up a mighty thunderbolt and hurl it at the " \
            "Warden. Your attack was successful: the Warden is finished.");
            printf("The Warden dropped %ld runes!\n", *dropped_runes);
            break;
        default:
            puts("\nApproximately 2.2 tons of Botanic Warden comes into contact " \
            "with your face. It feels exactly how it sounds.");
            return 1;
    }

    /* Serves as the mechanism for writing to `__free_hook`. When `free` is
    called at the end of the function, the user should be able to execute
    a magic gadget. */
    puts("After the battle, you feel compelled to leave a helpful message.\n");
    printf("Leave a message? (y/n): ");
    scanf(" %c", &leave_msg);
    getchar();
    if(leave_msg == 'y')
    {
        msg = (char *) malloc(sizeof(char) * 0x80);
        printf("Leave your message: ");
        size_t read_bytes = read(0, msg, 0x80);
        if(read_bytes == 0)
            return 1;
        msg[read_bytes - 1] = '\0';
        printf("\"%s\", you write on the ground in gold letters.\n", msg);
        __asm__("mov %rdx, %r13"); // Ugly, but makes the magic gadget work. Might also help the user
        free(msg); // Should execute shell if *__free_hook == magic_gadget 
    }
    puts("\nWith a few swigs from your crimson flask, you venture ownward.\n");
    return 0;
}

/* Allows the user to leak libc by printing a libc address in the GOT. */
int second_boss()
{
    // Order locals for libc leak
    struct
    {
        char taunt[16];
        long int *dropped_runes;
    } locals;
    locals.dropped_runes = &mergot_runes;
    int choice = 0;

    puts("You arrive at a golden wall of fog that serves at the entry to " \
    "Galeshroud Castle. You pass through the fog wall, and Mergot, the " \
    "Fallen Auspice, confronts you on a long bridge that leads to the castle.\n");
    puts("Mergot lunges at you with his gnarled cane, determined to " \
    "put your quest to an end. How do you respond?");
    printf("1. Roll forwards\n" \
    "2. Roll backwards\n" \
    "3. Roll to the side\n: ");

    scanf("%d", &choice);

    switch(choice)
    {
        case 1:
            puts("\nYour timely dodge results in you rolling under Mergot's " \
            "cane and left arm, placing you directly behind him. You " \
            "use the opportunity to deliver a series of quick blows!");
            break;

        case 2:
            puts("\nAs you roll backwards, you press against the fog wall " \
            "you entered, which does now not allow you to pass through. " \
            "Given that you move virtually nowhere, Mergot's cane meets " \
            "your skull, ending the battle quicker than it started.");
            return 1;

        case 3:
            puts("\nYou successfully naviagte away from the swipe of Mergot's " \
            "cane, but the bridge is a lot thinner than you realized: you " \
            "slip off the edge, cursing gravity as you perish.");
            return 1;

        default:
            puts("\nMergot is visibly perplexed as you remain motionless for " \
            "the entire duration of his attack. It connects, and brings the " \
            "fight to a brisk end.");
            return 1;
    }

    puts("\nA frustrated Mergot summons an ephemeral holy hammer and swings " \
    "it 180 degrees. You block it at the last minute, but the force of " \
    "the blow sends you flying backwards, placing you on the edge of the bridge.");

    puts("With your back facing a large drop, you have an idea that may end " \
    "the fight quickly...\n");

    // Introduce libc-leaking vulnerability
    printf("You decide to anger Mergot with a taunt. What do you say to him?\n: ");
    size_t read_bytes = read(0, locals.taunt, 24);
    if(read_bytes == 0)
        return 1;
    locals.taunt[read_bytes - 1] = '\0';

    puts("\nWhatever you said, it got his attention. He leaps forward in anger, " \
    "ready to strike with a conjured golden sword. What do you do, Unpolished?");
    printf("1. Attempt to block the strike\n" \
    "2. Rush forward, taking Mergot head-on\n" \
    "3. Perform a \"lie on the ground\" emote\n: ");

    scanf("%d", &choice);

    switch(choice)
    {
        case 1:
            puts("\nYou successfully block the strike, but the force of the blow " \
            "sends both you and Mergot tumbling off the bridge. A draw does " \
            "not count as a win.");
            return 1;
        case 2:
            puts("\nAs you dash forward, you attempt a running slide under Mergot." \
            " However, his tail catches you during your slide, he flies off the "
            "bridge, and you both fall into the depths below.");
            return 1;
        case 3:
            puts("\nYou lie on the ground in a resigned fashion, completely ignoring " \
            "Mergot's attack. This move catches him off guard and breaks his " \
            "focus, resulting in him poorly landing on the edge of the bridge " \
            "and ultimately falling into the foggy abyss below, resulting in " \
            "your victory.");
            printf("Mergot dropped %ld runes!\n", *locals.dropped_runes); // Print libc
            break;
        default:
            puts("\nAs you tumble through the air after being knocked off the " \
            "bridge, you wonder why you hadn't reacted to Mergot's attack.");
            return 1;
    }

    puts("\nSatisfied with the outcome of the fight, you make your way towards " \
    "the gate of Galeshroud Castle...\n");
    return 0;
}

int last_boss()
{
    int choice = 0;
    long int *dropped_runes = &aethelwulf_runes;
    puts("After fighting many of the Castle's finest soldiers, you finally " \
    "reach the path to the Castle's throne room. Guarding this room is " \
    "Aethelwulf the Adjoined, lord of the Castle.");
    puts("\nWith a dragon's head adjoined to his left arm and a giant war " \
    "axe held in his right, he makes his way towards you.");
    puts("You notice flame seeping out of the dragon head's mouth. Aethelwulf " \
    "is preparing to launch a stream of fire at you! What do you do?");
    printf("1. Run to the left of Aethelwulf\n" \
    "2. Run to the right of Aethelwulf\n" \
    "3. Run away from Aethelwulf\n: ");

    scanf("%d", &choice);
    
    switch(choice)
    {
        case 1:
            puts("\nAs you run to the left of Aethelwulf, he sprays dragonfire " \
            "from his left arm and aims it at you. Unable to get away, " \
            "you are immersed in a searing conflagration.");
            return 1;
        case 2:
            puts("\nYou run to the right of Aethelwulf, managing to get behind " \
            "his dragon arm as he begins to spray flame, allowing you to " \
            "avoid the dragonfire. You use this chance to strike!");
            break;
        case 3:
            puts("\nAs you run away from Aethelwulf, you greatly understimate " \
            "the length of the fire stream. You feel a slight singe on " \
            "your back, but this quickly turns into something much more " \
            "uncomfortable and all-enveloping.");
            return 1;
        default:
            puts("\n\"Well, this hurts\", you think to yourself as you " \
            "become 5,000 Kelvin warmer.");
            return 1;
    }

    puts("Your series of blows damages Aethelwulf's left arm, inhibiting his " \
    "ability to produce flame. He swings his war axe in a swiping motion, " \
    "which you manage to roll under...\n");

    puts("After a trading a series of powerful blows, both you and Aethelwulf " \
    "are on your last legs. There can only be one winner, Unpolished. How " \
    "do you intend to finish the fight?");
    printf("1. Use your imitator to summon a clone of yourself and double-" \
    "team Aethelwulf\n" \
    "2. Cast Azure Meteor\n " \
    "3. Break Aethelwulf's stance and land a critical hit\n: ");

    scanf("%d", &choice);
    getchar();

    switch(choice)
    {
        case 1:
            puts("\nYou summon a phantom clone of yourself, and you both " \
            "attack Aethelwulf with a pincer attack that he has no chance " \
            "of defending. Aethelwulf is defeated.");
            break;

        case 2:
            puts("\nUsing your staff, you cast Azure Meteor, an enormous " \
            "magic laser, which turns Aethelwulf into dust.");
            break;
        case 3:
            puts("\nYou strike Aethelwulf with a strong, charged attack " \
            "that breaks his stance, bringing him to his knees. You " \
            "finish the fight by landing a critical hit.");
            break;
        default:
            puts("As you choose to do nothing, Aethelwulf performs a " \
            "series of attacks that stun locks you and erases any " \
            "chance you had of becoming the Elden Lard.");
            return 1;
    }

    printf("Aethelwulf dropped %ld runes!\n\n", *dropped_runes);
    
    puts("Congratulations Unpolished. With these victories, you are " \
    "one step closer to becoming the Elden Lard.\n");

    return 0;
}

/* Driver function for the challenge. Idea is that the user must
beat each of the three bosses with the intent of reaching the NG+
state that will ultimately serve as the capability to get a UAF.
In `second_boss()`, there's a libc leak. */
int game()
{
    char choice = '\0';
    if(first_boss())
        return 0;
    if(second_boss())
        return 0;
    if(last_boss())
        return 0;
    printf("Would you like to start NG+? (y/n) : ");
    scanf("%c", &choice);
    getchar();
    if(choice == 'y')
        return 1;
    else
        return 0;
}

int main()
{
    setup();
    Unpolished *player = new_player();
    if(player == NULL)
        return 1;

    int return_code = 1;
    while(return_code)
    {
        size_t bytes_read = 0;
        puts("As you sit at the site of favor, Malloca turns your runes into strength.");
        printf("What do you tell her before departing?\n: ");
        bytes_read = read(0, player->departing_message, sizeof(char) * 256);
        if(bytes_read == 0)
        {
            puts("As you fail to produce any words, a semi-human bonks you on the head, " \
            "killing you instantly. So ends the journey of the Brave Unpolished...");
            return 1;
        }
        player->departing_message[bytes_read - 1];
        puts("\nMalloca nods her head in acknowledgement.\n\"I bid thee farewell\", she says, "
        "and then disappears before your very eyes. You set upon your journey.\n");
        return_code = game();
        free(player); // UAF if no break after 1 iteration
    }
    return 0;
}
