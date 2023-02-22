import cmd
import textwrap
import sys
import os
import time
import random
import asciiart as aa

screen_width = 150


###################### Create player model ######################################
class Player():
    def __init__(self):
        self.name = ""
        self.hero_type = ""
        self.hp = 0
        self.mp = 0
        self.sp = 0
        self.status_effects = []
        self.location = ''
        self.gameover = False

myPlayer = Player()


################# Create zones on the map #####################################
ZONENAME = ''
DESCRIPTION = 'description'
EXAMINATION = 'examine'
ANSWER = 'unknown'
BONUS_FIND = 'x',
BONUS_EDGE = 'y',
BONUS_EFFECT = 'z',
SOLVED = False
UP = 'up', 'north'
DOWN = 'down', 'south'
LEFT = 'left', 'west'
RIGHT = 'right', 'east'

zone_map = {
    'a1': {
        ZONENAME: "Empty wilderness",
        DESCRIPTION: f"""Appearing from behind one of the desert trees, a thin man\n
                    wearing a cowboy hat calls out to you,\n
                    "Tell me, stranger, what is the past-continuous form of\n
                    *She sells seashells by the seashore*\n
                    If you can't tell me," he warns, holding up a stone. "I'll throw this stone at you!"\n 
                    """,
        EXAMINATION: """From the top of a sand dune, all you can see are more sand dunes,\n
                     some scattered trees and shrubs, and a small pile of rokcs.\n
                     And although the sky is blue, the glowing horizon is black.\n 
                     It's darkest at four opposite corners, giving the impression of a square.\n 
                     The northern and western sides of the square are speckled with stars,\n
                     while in the South you can see the start of a forest. In the East\n
                     you can see a path up into the mountains.\n  
                     """,
        ANSWER: "She was selling seashells by the seashore",
        BONUS_FIND: 'rokcs',
        BONUS_EDGE: 'rocks',
        BONUS_EFFECT: '+1',
        SOLVED: False,
        UP: 'You fell off!',
        DOWN: 'b1',
        LEFT: 'You fell off!',
        RIGHT: 'a2',
    },
    'a2': {
        ZONENAME: 'Mountain path',
        DESCRIPTION: 'A black bird flies from out of nowhere and perches itself on a rock beside the path.\n'
                     'You look at it, and it squawks,\n'
                     '"What is the future-continuous form of,\n'
                     '*They had driven here tonight*".\n'
                     'The bird fluffed its feathers, lifted a foot and added, "Tell me,\n'
                     'or I will scratch you!"\n',
        EXAMINATION: 'The mountain path winds between a dense forest and the vastness of space.\n'
                     'It has a snow-capped peak far ahead, and it\'s strange to hear the sounds of\n'
                     'birds and monkeys on one side, and a deep silence on the other. Further ahead,\n'
                     'where the mountain peaks, the forest retreats to reveal the long, sharp rocks of\n'
                     'the steep incline. You can however see something shiney tucked behind a rock.',
        ANSWER: "They will be driving here tonight",
        BONUS_FIND: 'shiney',
        BONUS_EDGE: 'shiny',
        BONUS_EFFECT: '+1',
        SOLVED: False,
        UP: 'You fell off!',
        DOWN: 'b2',
        LEFT: 'a1',
        RIGHT: 'a3',
    },
    'a3': {
        ZONENAME: 'Snowy mountain top',
        DESCRIPTION: 'You see a black dot moving towards you, and then see two smaller\n'
                     'black dots appear above the bigger black dot.\n'
                     'As you wait, you see the furry outline of a polar bear approaching you!\n'
                     'It stops a few feet away and sits down. Then says,\n'
                     '"What is the past-continuous and past-simple form of,\n'
                     '*I will choose a meal when I arrive*".\n'
                     'The bear waves a paw at you, "Or I will swipe you!"\n',
        EXAMINATION: 'Everything is white, with a few traces of dark rock and stone\n'
                     'showing evidence of the mountain below your feet. The snowy haze\n'
                     'is a mixchure of the starlight reflecting off the snow\n'
                     'and the suspended snowflakes being windswept up from behind the peak.\n'
                     'There is a steep rockface on the side of the mountain, and you can\'t\n'
                     'see anything beyond. You can, however, see a hang glider resting\n'
                     'on the edge of the mountain.',
        ANSWER: "I was choosing a meal when I arrived",
        BONUS_FIND: 'mixchure',
        BONUS_EDGE: 'mixture',
        BONUS_EFFECT: '+1',
        SOLVED: False,
        UP: 'You fell off!',
        DOWN: ["You can't", "The mountain is too steep, and you could fall into valley below!."],
        LEFT: 'a2',
        RIGHT: 'a4',
    },
    'a4': {
        ZONENAME: 'Palm-ringed oasis splash-pool',
        DESCRIPTION: 'Just as you are about to leave, with your toes still in the water,\n'
                     'and enjoying the heat from the sun; \n'
                     'you suddenly feel something sharp\n'
                     'encircle your big toe. Not making any quick movements,\n'
                     'you look down - through the clear water - and see a crab emerge\n'
                     'from the sand.\n' 
                     f'{aa.crab}\n'
                     'It has big eyes, looking back up at you, and\n'
                     'you are unsure what to do.'
                     'Then a monkey swings down from a tree, haunches beside you and\n'
                     'seems to understand the nature of the situation. He looks to you\n'
                     'and says, \n'
                     '"That is Eddy. Eddy doesn\'t like strangers. He wants to chop off your toe."\n'
                     '"But why?" You ask.\n'
                     '"We don\'t know," the monkey replies. "We just know that Eddy is protective."\n'
                     '"Has Eddy chopped off toes before?"\n'
                     'The monkey lifts a foot and shows a missing toe. He adds, \n'
                     '"You will see many animals here have a missing toe. But at least\n'
                     'we\'ve all improved our English grammar".\n'
                     '"Eddy has a grammar question?"\n'
                     '"Yes," the monkey nods. "Answer his question correctly then he\'ll leave your toe alone."\n'
                     'You nod, accepting the conditions.\n'
                     'The monkey looks at Eddy, and Eddy looks back at the monkey as\n'
                     'some bubbles come up to the surface. The monkey then\n'
                     'looks to you and says,\n'
                     '"You must change the following sentence into the perfect-form;\n'
                     '*I studied a lot at school, and will study more at university*.\n',

        EXAMINATION: 'After having taken the hang glider and just jumped ahead,\n'
                     'you glided down through the clouds and aimed for an oasis\n'
                     'in the middle of a dessert. \nIts a lovely place and you feel\n'
                     'healthier than before. Around you are some\n'
                     'relaxed animals, like buffalo and giraffes, camels and even\n'
                     'goats. Some are lying in the shade, others playing while a few\n'
                     'are drinking from the small lake. Beside you in a bush, you see a bottel\n'
                     'of some kind.\n\n'
                     'Further beyond, to the North and East, you see a deep, dark starry space.\n'
                     'To the South the forest has a faint mist hanging about it. Likely due\n'
                     'to all the ponds and lakes in that area.',
        ANSWER: 'I had studied a lot at school, and will have studied more at university',
        BONUS_FIND: 'bottel',
        BONUS_EDGE: 'bottle',
        BONUS_EFFECT: '+2',
        SOLVED: False,
        UP: 'You fell off!',
        DOWN: 'b4',
        LEFT: ["You can't", "The mountain is too steep from this side."],
        RIGHT: 'You fell off!',
    },
    'b1': {
        ZONENAME: 'Woody forest',
        DESCRIPTION: 'As you start to move, a man with a gun calls out at you from a distance,\n'
                     '"Stop, or I\'ll shoot!"\n'
                     'The man is very far away, but you can see him standing behind a bush,\n'
                     'wearing a red hat and holding a rifle. You call back, having to shout,\n'
                     '"What do you want?" You listen carefully for the reply.\n'
                     '"Which of these modal verbs is best used to make a suggestion:\n\n'
                     ' - Could,\n'
                     ' - Should,\n'
                     ' - Would.\n\n'
                     'You only get one guess!"',
        EXAMINATION: 'The forest has some tall pine trees.\n'
                     'A few birds swoop about the air. A Brown-headed nuthatch,\n'
                     'a Red-cockaded woodpecker, and you even see some squirrels\n'
                     'running along a brand with some pinecones.\n'
                     'The area is well-shaded with a gentle breeze.\n'
                     'To the west the sky is still an imnense starry-speckled space,\n'
                     'while to the south this forest seems to give way to an open grassland.\n'
                     'To the east, however, the forest only looks to be getting thicker, wetter,\n'
                     'and a lot noisier.',
        ANSWER: 'Should',
        BONUS_FIND: 'imnense',
        BONUS_EDGE: 'immense',
        BONUS_EFFECT: '+1',
        SOLVED: False,
        UP: 'a1',
        DOWN: 'c1',
        LEFT: 'You fell off!',
        RIGHT: 'b2',
    },
    'b2': {
        ZONENAME: 'Jungle',
        DESCRIPTION: 'As you lower your leg to get back to the ground, a green and yellow snake\n'
                     'descends before you.\n'
                     'It\'s head is as big as your fist and it looks straight at you.\n'
                     'Eyes are white and it hisses before saying,\n'
                     '"Change the modal verb in the following sentence so that the possibility\n'
                     'is turned into a necessity, or an obligation;\n'
                     '*I might do my homework*"\n',
        EXAMINATION: 'With the trees so tightly packed, and the ground vegetation\n'
                     'so dense; it\'s difficult to see anything beyond a few meters!\n'
                     'You do, however, see plenty of reptiles scuttling around. As well as\n'
                     'frogs hopping in-and-out from under large, fallen leaves. From far away\n'
                     'the sound of a high-pitched bird or monkey fills the air.\n\n'
                     'The ground is wet enough to make squelching sounds as you walk\n'
                     'and the humidity is sticking your clothes to your skin.\n'
                     'The smell in the aire is also so pungent that it\'s difficult to\n'
                     'figure out where it\'s coming from.\n'
                     'Deciding to take a break, you find a tree with a low branch and\n'
                     'sit in it\'s crook. ',
        ANSWER: ['I must do my homework', 'I should do my homework', 'I ought to do my homework'],
        BONUS_FIND: 'aire',
        BONUS_EDGE: 'air',
        BONUS_EFFECT: '+1',
        SOLVED: False,
        UP: 'a2',
        DOWN: 'c2',
        LEFT: 'b1',
        RIGHT: 'b3',
    },
    'b3': {
        ZONENAME: 'Mountain cave forests',
        DESCRIPTION: 'Grabbing onto a vine to swing around a protruding rock; you get halfway\n'
                'before you come face-to-face with a mountain goat. It\'s somehow defying\n'
                'gravity, standing with the edges of its hooves balanced in the shallow cuts\n'
                'in the rock. You\'re very impressed. Then it says,\n'
                '"Before you continue, you must repeat the following sentence by contracting\n'
                'all the modal verbs:\n\n'
                '*They can not, should not, and will not accept failure*"\n\n',
        EXAMINATION: 'Traversing the path along the mountainside would be\n'
                     'nearly impossible without the help of trees and bushes\n'
                     'growing out from the rockface. Below is a deep valley,\n'
                     'and one wrong-footing (or a loosely anchored support branch)\n'
                     'would spell disatser!\n'
                     'It\'s too risky to climb northwards up the mountain, where\n'
                     'the snow-capped peak looms overhead. It also seems too risky\n'
                     'to climb down and out of the valley to the south, where you can\n'
                     'see wide open fields of rice paddies.\n'
                     'The only way to move would be west to the forest, or eastwards\n'
                     'to a more barren swamp-like area.\n',
        ANSWER: 'They can\'t, shouldn\'t, and won\'t accept failure',
        BONUS_FIND: 'disatser',
        BONUS_EDGE: 'disaster',
        BONUS_EFFECT: '+2',
        SOLVED: False,
        UP: ["You can't", "The mountain is too steep. One wrong move and you\'ll fall!."],
        DOWN: ["You can't", "The mountain is too steep. One wrong move and you\'ll fall!."],
        LEFT: 'b2',
        RIGHT: 'b4',
    },
    'b4': {
        ZONENAME: 'Creepy swamp',
        DESCRIPTION: 'When you step forward, the displaced pressure pushes up the\n'
                     'skull of some long-beak bird! Startled, you step away, and then\n'
                     'hear a voice from above.\n'
                     'Looking up, you see a massive spider!\n'
                     f'{aa.spider}\n'
                     'Familiar with talking creatures, you ask,\n'
                     '"What grammar question do you have for me, giant spider?"\n'
                     'The spider moves closer and replies,\n\n'
                     '"Change the following sentence by using the more formal\n'
                     'modal verb:\n'
                     '*I will ask her tomorrow, then we will let you know*"\n\n',
        EXAMINATION: 'Although there aren\'t many tall trees, and there\'s an\n'
                     'abundance of light; the many stagnant pools of this weathered\n'
                     'swamp feels spooky. Above the ground is a faint\n'
                     'mist that gets thicker over the pools, making it eezy to misstep.\n'
                     'Large cobwebs hang from broken branches and look like they can\n'
                     'catch large birds!\n\n'
                     'Further east, the horizon is dark and displays the vastness of \n'
                     'empty space with many thousands of stars. To the west is where a\n'
                     'forest is both part of a mountain side, and part of a deep valley.\n'
                     'The North seems to be a desert, but you noticed many signs along\n'
                     'the way stating that trespassers are unwelcome. To the South is an\n'
                     'expansive open plain.',
        ANSWER: 'I shall ask her tomorrow, then we shall let you know',
        BONUS_FIND: 'eezy',
        BONUS_EDGE: 'easy',
        BONUS_EFFECT: '+2',
        SOLVED: False,
        UP: ["You can't", "The crab forbids you."],
        DOWN: 'c4',
        LEFT: 'b3',
        RIGHT: 'You fell off!',
    },
    'c1': {
        ZONENAME: '',
        DESCRIPTION: 'description',
        EXAMINATION: 'examine',
        ANSWER: '',
        BONUS_FIND: '',
        BONUS_EDGE: '',
        SOLVED: False,
        UP: 'b1',
        DOWN: 'd1',
        LEFT: 'You fell off!',
        RIGHT: 'c2',
    },
    'c2': {
        ZONENAME: '',
        DESCRIPTION: 'description',
        EXAMINATION: 'examine',
        ANSWER: '',
        BONUS_FIND: '',
        BONUS_EDGE: '',
        BONUS_EFFECT: '',
        SOLVED: False,
        UP: 'b2',
        DOWN: 'd2',
        LEFT: 'c1',
        RIGHT: 'c3',
    },
    'c3': {
        ZONENAME: '',
        DESCRIPTION: 'description',
        EXAMINATION: 'examine',
        ANSWER: '',
        BONUS_FIND: '',
        BONUS_EDGE: '',
        BONUS_EFFECT: '',
        SOLVED: False,
        UP: 'b3',
        DOWN: 'd3',
        LEFT: 'c2',
        RIGHT: 'c4',
    },
    'c4': {
        ZONENAME: '',
        DESCRIPTION: 'description',
        EXAMINATION: 'examine',
        ANSWER: '',
        BONUS_FIND: '',
        BONUS_EDGE: '',
        BONUS_EFFECT: '',
        SOLVED: False,
        UP: 'b4',
        DOWN: 'd4',
        LEFT: 'c3',
        RIGHT: 'You fell off!',
    },
    'd1': {
        ZONENAME: '',
        DESCRIPTION: 'description',
        EXAMINATION: 'examine',
        ANSWER: '',
        BONUS_FIND: '',
        BONUS_EDGE: '',
        BONUS_EFFECT: '',
        SOLVED: False,
        UP: 'c1',
        DOWN: 'You fell off!',
        LEFT: 'You fell off!',
        RIGHT: 'd2',
    },
    'd2': {
        ZONENAME: '',
        DESCRIPTION: 'description',
        EXAMINATION: 'examine',
        ANSWER: '',
        BONUS_FIND: '',
        BONUS_EDGE: '',
        BONUS_EFFECT: '',
        SOLVED: False,
        UP: 'c2',
        DOWN: 'You fell off!',
        LEFT: 'd1',
        RIGHT: 'd3',
    },
    'd3': {
        ZONENAME: '',
        DESCRIPTION: 'description',
        EXAMINATION: 'examine',
        ANSWER: '',
        BONUS_FIND: '',
        BONUS_EDGE: '',
        BONUS_EFFECT: '',
        SOLVED: False,
        UP: 'c3',
        DOWN: 'You fell off!',
        LEFT: 'd2',
        RIGHT: 'd4',
    },
    'd4': {
        ZONENAME: '',
        DESCRIPTION: 'description',
        EXAMINATION: 'examine',
        ANSWER: '',
        BONUS_FIND: '',
        BONUS_EDGE: '',
        BONUS_EFFECT: '',
        SOLVED: False,
        UP: 'c4',
        DOWN: 'You fell off!',
        LEFT: 'd3',
        RIGHT: 'You fell off!',
    }
}

def clear():
    os.system('cls')


def cleanReply(reply):
    return reply.lower().strip()


#### Title Screen ####

def execute_title_screen_selection(selection):
    if selection.lower() == 'play':
        start_game()
    elif selection.lower() == 'help':
        help_menu()
    elif selection.lower() == 'quit':
        sys.exit()

def title_screen_selections():

    random_num = random.randint(1,3)
    print(aa.random_animals[random_num])

    available_title_options = ['play', 'help', 'quit']
    reply = input("> ")
    option = cleanReply(reply)
    execute_title_screen_selection(option)

    while option not in available_title_options:
        print("\n ** Please type play, help or quit **")
        reply = input("> ")
        option = cleanReply(reply)
        execute_title_screen_selection(option)



def title_screen():
    clear()
    print('##############################')
    print('#  Welcome to the Text RPG!  #')
    print('##############################')
    print('        - Play -              ')
    print('        - Help -              ')
    print('        - Quit -              ')
    print('##############################')
    title_screen_selections()


def help_menu():
    clear()
    print('#############################################                ')
    print('#               Help menu                   #                ')
    print('#############################################                ')
    print(' - Type commands to execute them                             ')
    print(' - > "Where am I?" to know which zone you are in           ')
    print(' - > "What is my health?" to check your health points     ')
    print(' - > "How much magic do I have?" to check your available magic points')
    print(' - > "What is my speed?" to see how quick you are           ')
    print(' - > "Examine" to better understand the current zone       ')
    print(' - > "Move" to initiate movement from one zone to another  ')
    print(' - > "Left", "Right", "Up", or "Down" to choose a direction ')
    print(' - > "Solved" to see how many zone questions you\'ve solved')
    print('#############################################                ')
    title_screen_selections()

#### GAME Functionality ####




#### MAP ####

"""
# Player starts at a1
---------------------
| a1 | a2 | a3 | a4 |
---------------------
| b1 | b2 | b3 | b4 |
---------------------
| c1 | c2 | c3 | c4 |
---------------------
| d1 | d2 | d3 | d4 |
---------------------
"""



solved_places = {
    'a1': False, 'a2': False, 'a3': False, 'a4': False,
    'b1': False, 'b2': False, 'b3': False, 'b4': False,
    'c1': False, 'c2': False, 'c3': False, 'c4': False,
    'd1': False, 'd2': False, 'd3': False, 'd4': False,
}


def game_check():
    if myPlayer.hp < 1:
        clear()
        print(aa.game_over)
        sys.exit()

def prompt():
    game_check()

    print(f"\n ~ + ~ @ ~ * ~ & ~ # ~ & ~ * ~ @ ~ + ~ \n")
    print("What would you like to do? ")
    reply = input("> ")
    action = cleanReply(reply)
    acceptable_actions = ['move', 'go', 'walk', 'travel',
                          'look', 'inspect', 'examine', 'investigate',
                          'where am i?', 'quit', 'what is my health?', 'how much magic do i have?',
                          'what is my speed?', zone_map[myPlayer.location][BONUS_FIND], 'solved']
    while action not in acceptable_actions:
        print("^^ Unknown action ^^\nPlease try again\n\n")
        print("What would you like to do? ")
        reply = input("> ")
        action = cleanReply(reply)

    if action == 'quit':
        sys.exit()
    elif action == 'where am i?':
        print_location()
    elif action == 'what is my health?':
        print_hp()
    elif action == 'how much magic do i have?':
        print_mp()
    elif action == 'what is my speed?':
        print_sp()

    elif action in ['move', 'go', 'walk', 'travel']:
        player_move()
    elif action in ['look', 'inspect', 'examine', 'investigate']:
        player_examine()

    elif action == 'solved':
        print_solved()

    elif action == zone_map[myPlayer.location][BONUS_FIND]:
        bonus_find = zone_map[myPlayer.location][BONUS_FIND]
        bonus_edge = zone_map[myPlayer.location][BONUS_EDGE]
        bonus_effect = zone_map[myPlayer.location][BONUS_EFFECT]
        secret_potion(bonus_find, bonus_edge, bonus_effect)


###### GAME INTERACTIVITY ##############
def print_location():
    clear()
    print(f"\n    <>~<>~<>~<>  Zone {myPlayer.location.capitalize()}  <>~<>~<>~<>  \n")

    name_length = len(f"{zone_map[myPlayer.location][ZONENAME]}")
    padded_length = 37 - name_length - 4
    print(f">>{'-' * int(padded_length/2)}> {zone_map[myPlayer.location][ZONENAME]} <{'-' * int(padded_length/2)}<<")

    print(f"\n    <>~<>~<>~<>  Zone {myPlayer.location.capitalize()}  <>~<>~<>~<>  \n")
    prompt()


def print_solved():
    clear()
    player_solved = []
    for i, j in solved_places.items():
        if j:
            player_solved.append(i.capitalize())
    print(f"\n  {'=' * len(player_solved)} >> Solved: {player_solved}  << {'=' * len(player_solved)}  \n")
    prompt()


def print_hp():
    clear()
    print(f"\n  {'+' * myPlayer.hp} >> Health: {myPlayer.hp}  << {'+' * myPlayer.hp}  \n")
    prompt()


def print_mp():
    clear()
    print(f"\n  {'^' * myPlayer.mp} >> Magic: {myPlayer.mp}  << {'^' * myPlayer.mp}  \n")
    prompt()


def print_sp():
    clear()
    print(f"\n  {'*' * myPlayer.sp} >> Speed: {myPlayer.sp}  << {'*' * myPlayer.sp}  \n")
    prompt()


def toss():
    toss = "You toss away the bottle\n"
    for i in toss:
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(0.06)
    zone_map[myPlayer.location][BONUS_FIND] = 'plokijuh'
    prompt()


def add_one(bonus_effect):
    result = random.randint(1, 3)
    effect = int(bonus_effect[-1])
    if result == 1:
        myPlayer.hp += effect
        print(f"Your health increased by {effect}")
    elif result == 2:
        myPlayer.mp += effect
        print(f"Your health increased by {effect}")
    else:
        myPlayer.sp += effect
        print(f"Your health increased by {effect}")
    zone_map[myPlayer.location][BONUS_FIND] = 'plokijuh'
    prompt()


def add_two(bonus_effect):
    result = random.randint(1, 3)
    effect = int(bonus_effect[-1]) + 1
    if result == 1:
        myPlayer.hp += effect
        print(f"Your health increased by {effect}")
    elif result == 2:
        myPlayer.mp += effect
        print(f"Your health increased by {effect}")
    else:
        myPlayer.sp += effect
        print(f"Your health increased by {effect}")
    zone_map[myPlayer.location][BONUS_FIND] = 'plokijuh'
    prompt()


def secret_potion(bonus_find, bonus_edge, bonus_effect):
    bonus_greeting1 = f"""\n\n You found a secret potion! *{bonus_find}* \n\n
        The effect is: {bonus_effect}\n
        Say the word correctly when you drink it, then it will work harder for you\n
        Or you can toss it\n"""
    for i in bonus_greeting1:
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(0.06)

    reply = input("> ")
    clean_reply = cleanReply(reply)
    if clean_reply == bonus_edge:
        add_two(bonus_effect)
    elif clean_reply == "toss" or clean_reply == "toss it":
        toss()
    else:
        add_one(bonus_effect)


def player_move():
    ask = f"\n Where would you like to move to?\n"
    for i in ask:
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(0.09)
    reply = input("> > ")
    dest = cleanReply(reply)

    acceptable_directions = ['up', 'north', 'down', 'south',
                             'left', 'west', 'right', 'east',
                             'quit', 'not move']
    while dest not in acceptable_directions:
        print("\n ** Did not recognise direction. Please try again **")
        ask = f"\n Where would you like to move to?\n> "
        reply = input("> ")
        for i in ask:
            sys.stdout.write(i)
            sys.stdout.flush()
            time.sleep(0.09)
        dest = cleanReply(reply)

    if dest in ['up', 'north']:
        destination = zone_map[myPlayer.location][UP]
        fallcheck(destination)
        problemcheck(destination)
        movement_handler(destination)
    elif dest in ['down', 'south']:
        destination = zone_map[myPlayer.location][DOWN]
        fallcheck(destination)
        problemcheck(destination)
        movement_handler(destination)
    elif dest in ['left', 'west']:
        destination = zone_map[myPlayer.location][LEFT]
        fallcheck(destination)
        problemcheck(destination)
        movement_handler(destination)
    elif dest in ['right', 'east']:
        destination = zone_map[myPlayer.location][RIGHT]
        fallcheck(destination)
        problemcheck(destination)
        movement_handler(destination)
    elif dest in ['quit']:
        sys.exit()
    elif dest in ['not move']:
        prompt()


def fallcheck(destination):
    if destination == "You fell off!":
        death_spiral = f"\n\n*******\n***<^><^><^>***\n <^> You fell off the puzzle-grid <^> \n***<^><^><^>***\n****\n***\n**\n*\n&^ ! %$#@ ! @#$% ! ^&\n\n"
        for i in death_spiral:
            sys.stdout.write(i)
            sys.stdout.flush()
            time.sleep(0.09)

        clear()
        print(aa.game_over)
        sys.exit()


def problemcheck(destination):
    if type(destination) == list:
        print("\n\n")
        for i in destination[1]:
            sys.stdout.write(i)
            sys.stdout.flush()
            time.sleep(0.12)
        print("\n\n")
        prompt()



def lose_health():
    lost_health = f"\nOh no, {myPlayer.name}!\n" \
                  f"That's incorrect...\n" \
                  f"You lose 2 health points\n"
    for i in lost_health:
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(0.11)

    myPlayer.hp -= 2
    print_hp()
    prompt()


def got_caught():
    just_got_caught = "\n\n  OH, NO !!! YOU GOT CAUGHT !!!!!!  \n\n"
    for i in just_got_caught:
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(0.11)

    myPlayer.hp -= 2
    print_hp()
    prompt()


def player_answering(destination, game_answer):
    print("Provide your answer here:\n")
    option = input("> > ")
    player_answer = cleanReply(option)

    if player_answer in game_answer:
        zone_map[myPlayer.location][SOLVED] = True

        clear()
        well_done1 = f"\nWell done. You have solved the problem and moved to Zone {destination.capitalize()}  ...\n"
        well_done2 = aa.well_done_display

        for i in well_done1:
            sys.stdout.write(i)
            sys.stdout.flush()
            time.sleep(0.08)
        for i in well_done2:
            sys.stdout.write(i)
            sys.stdout.flush()
            time.sleep(0.01)

        solved_places[myPlayer.location] = True

        myPlayer.location = destination

        if destination == 'a4':
            myPlayer.hp += 3

        print_location()

    elif player_answer == 'escape':
        escape_using_speed()
    elif player_answer == 'magic':
        player_using_magic(destination, game_answer[0])

    else:
        lose_health()


def player_using_magic(destination, game_answer):
    mp = myPlayer.mp
    answer = game_answer.capitalize()
    for i in range(mp):
        print(f"{' '* i }{'_.~$(_.' * i}")
        time.sleep(0.4)
    print("\n\n")
    non_magic_chars = [" ", ",", ".", ";", ":", "'"]
    for i in answer:
        if i in non_magic_chars:
            sys.stdout.write(i)
            sys.stdout.flush()
            time.sleep(0.5)
            continue
        missed = random.randint(1, 10)
        if mp > missed:
            sys.stdout.write(i)
            sys.stdout.flush()
            time.sleep(0.01)
        elif mp == missed:
            sys.stdout.write("~")
            sys.stdout.flush()
            time.sleep(0.01)
        else:
            sys.stdout.write(f"{'?' * (missed - mp)}")
            sys.stdout.flush()
            time.sleep(0.01)

    myPlayer.mp -= 1
    print("\n         <> <> <>        \n")
    answer_after_magic = "You must now give your answer...\n"
    for i in answer_after_magic:
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(0.1)

    # Retrieve answers
    game_answer_list = get_answer_list()
    player_answering(destination, game_answer_list)


def escape_using_speed():
    speed = myPlayer.sp
    myPlayer.sp -= 1

    answer = zone_map[myPlayer.location][ANSWER]
    answer_length = len(answer)

    snakey = "-=========:>"
    distance = 2
    mousey = "~~(8:>"

    clear()
    for i in range(3):
        print("  _<>_<>_<>__Countdown__<>_<>_<>_  ")
        print(f"          {' '* (0 + i)}{'|'* (3 - i)} <> {3 - i} <> {'|'* (3 - i)}")
        print(f'\n     {"_.~^~." * distance}\n')
        print(f"  {snakey}{' ' * distance}{mousey}")
        print(f'\n{"|O|" * answer_length}\n')
        time.sleep(1.5)
        clear()

    non_magic_chars = [' ', ',', '.', ';', ':']
    for i in answer:
        if i in non_magic_chars:
            answer_length -= 1
            continue
        if distance == 0:
            got_caught()

        missed = random.randint(0, 10)
        if speed > missed:
            distance += 1
        else:
            distance -= 1
        clear()
        print("  _<>_<>_<>__   o_O   __<>_<>_<>_  ")
        print(f"          '|_|_|_|_|_|_|'        ")
        print(f'\n     {"_.~^~." * distance}\n')
        print(f"  {snakey}{' ' * distance}{mousey}")
        print(f'\n{"|O|" * answer_length}\n')
        answer_length -= 1
        time.sleep(0.05)

    print("\n\n  YOU ESCAPED !!!!!!  \n\n")


def get_answer_list():
    game_answer = []
    if type(zone_map[myPlayer.location][ANSWER]) == list:
        for i in zone_map[myPlayer.location][ANSWER]:
            game_answer.append(i.lower())
    else:
        game_answer.append(zone_map[myPlayer.location][ANSWER].lower())
    return game_answer


def movement_handler(destination):
    if solved_places[destination]:
        myPlayer.location = destination
        if destination == 'a4':
            myPlayer.hp += 3
        clear()
        print_location()
        return

    clear()
    print("~*=#=*~*=#=*~*=#=*~*=#=*~*=#=*~*=#=*~*=#=*\n")
    print("~*=# Before going to an Unsolved Zone =#=*\n")
    print("~*=#=*~*=#=*~*=#=*~*=#=*~*=#=*~*=#=*~*=#=*\n")
    print(zone_map[myPlayer.location][DESCRIPTION])
    print("~^=@=^~^=@=^~^=@=^~^=@=^~^=@=^~^=@=^~^=@=^\n")
    print("Would you like to:\n  - Answer\n  - Magic\n  - Escape\n ")
    option = input("> ")
    response = cleanReply(option)

    while response not in ['answer', 'magic', 'escape', 'quit']:
        print("Could not understand..")
        print("Would you like to:\n  - Answer, \n  - Magic, or\n  - Escape\n ")
        option = input("> ")
        response = cleanReply(option)

    game_answer = get_answer_list()

    if response == 'answer':
        player_answering(destination, game_answer)

    elif response == 'magic':
        if myPlayer.mp < 1:
            no_magic_left = "\n\nYou have no magic left :(\n\n"
            for i in no_magic_left:
                sys.stdout.write(i)
                sys.stdout.flush()
                time.sleep(0.09)
            time.sleep(2)
        else:
            # Convert list of answer/s into a string-answer for magic
            string_answer = game_answer[random.randint(0, (len(game_answer) - 1))]
            player_using_magic(destination, string_answer)

    elif response == 'escape':
        escape_using_speed()

    elif response.lower() == 'quit':
        sys.exit()


def player_examine():
    clear()
    print(f"\n{zone_map[myPlayer.location][EXAMINATION]}\n\n")
    prompt()


def main_game_loop():

    while myPlayer.gameover is False:
        prompt()


def assign_attributes(hero_type):
    if hero_type == 'spartan':
        myPlayer.hp = random.randint(7, 10)
        myPlayer.mp = random.randint(2, 4)
        myPlayer.sp = random.randint(4, 6)
    elif hero_type == 'wizard':
        myPlayer.hp = random.randint(3, 6)
        myPlayer.mp = random.randint(8, 9)
        myPlayer.sp = random.randint(2, 5)
    elif hero_type == 'ninja':
        myPlayer.hp = random.randint(5, 7)
        myPlayer.mp = random.randint(1, 5)
        myPlayer.sp = random.randint(7, 8)


def start_game():
    clear()

    question = "Hello. What's your name?\n"
    for i in question:
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(0.05)
    player_name = input("> ")
    if player_name == 'quit':
        sys.exit()

    myPlayer.name = player_name
    print("\n")

    greeting1 = f"Hello, {player_name}. Nice to meet you.\n"
    greeting2 = f"And welcome to... \n"
    greeting3 = f"A 16-zone puzzle grid!\n"
    greeting4 = f"The only way to escape is to "
    greeting5 = f"solve your way to...\n"
    greeting6 = f"... Zone D4 ...        \n"

    greeting7 = f"Before moving from one zone to the next, you must answer a question. Failure causes damage\n"
    greeting8 = f"  ->  Spartans can absorb more damage.\n"
    greeting9 = f"  ->  Wizards have more magic to help them answer questions.\n"
    greeting10 = f"  ->  Ninjas are better able to escape questions without getting hurt.\n"
    greeting11 = f"Given these options...\n"
    greeting12 = f"What kind of hero do you want to play?\n"

    for i in greeting1:
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(0.07)
    for i in greeting2:
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(0.11)
    for i in greeting3:
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(0.07)
    for i in greeting4:
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(0.07)
    for i in greeting5:
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(0.07)
    for i in greeting6:
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(0.2)
    greeting6p5 = "\n`-._,-'^`-._,-'^`-._,-'^`-._,-'`-._,-'^`-._,-'^`-._,-'^`-._,-'\n\n"
    for i in greeting6p5:
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(0.04)
    for i in greeting7:
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(0.05)
    for i in greeting8:
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(0.1)
    for i in greeting9:
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(0.11)
    for i in greeting10:
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(0.13)
    for i in greeting11:
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(0.1)
    for i in greeting12:
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(0.08)

    hero_type = input("> ")

    while hero_type.lower() not in ['spartan', 'wizard', 'ninja', 'quit']:
        print("\n~~~~~ Could not understand ~~~~~")
        print("~~~~~ please select spartan, wizard or ninja ~~~~~")
        hero_type = input("> ")

    if hero_type.lower() == 'quit':
        sys.exit()

    myPlayer.hero_type = hero_type
    assign_attributes(hero_type.lower().strip())

    clear()
    game_start_address1 = f"Very well, {myPlayer.name} the {myPlayer.hero_type}\n"
    game_start_address2 = "Good luck! And remember not to fall off the edge!\n"
    game_start_address3 = "Heh.. Heh.. Heh..."

    if myPlayer.hero_type.lower() == 'spartan':
        print(aa.spartan)
    elif myPlayer.hero_type.lower() == 'wizard':
        print(aa.wizard)
    elif myPlayer.hero_type.lower() == 'ninja':
        print(aa.ninja)

    for i in game_start_address1:
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(0.08)
    for i in game_start_address2:
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(0.1)
    for i in game_start_address3:
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(0.2)

    clear()
    print("########################")
    print("##    Let's begin!    ##")
    print("########################")

    myPlayer.location = 'b1'

    main_game_loop()


title_screen()



