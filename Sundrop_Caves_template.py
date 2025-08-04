from random import randint

player = {}
game_map = []
fog = []

MAP_WIDTH = 0
MAP_HEIGHT = 0

TURNS_PER_DAY = 20
WIN_GP = 500

minerals = ['copper', 'silver', 'gold']
mineral_names = {'C': 'copper', 'S': 'silver', 'G': 'gold'}
pickaxe_price = [50, 150]

prices = {}
prices['copper'] = (1, 3)
prices['silver'] = (5, 8)
prices['gold'] = (10, 18)

# This function loads a map structure (a nested list) from a file
# It also updates MAP_WIDTH and MAP_HEIGHT
def load_map(filename, map_struct):
    map_file = open(filename, 'r')
    global MAP_WIDTH
    global MAP_HEIGHT
    
    map_struct.clear()
    
    # TODO: Add your map loading code here
    
    MAP_WIDTH = len(map_struct[0])
    MAP_HEIGHT = len(map_struct)

    map_file.close()

# This function clears the fog of war at the 3x3 square around the player
def clear_fog(fog, player):
    return

def initialize_game(game_map, fog, player):
    # initialize map
    load_map("level1.txt", game_map)

    # TODO: initialize fog
    
    # TODO: initialize player
    #   You will probably add other entries into the player dictionary
    player['x'] = 0
    player['y'] = 0
    player['copper'] = 0
    player['silver'] = 0
    player['gold'] = 0
    player['GP'] = 0
    player['day'] = 0
    player['steps'] = 0
    player['turns'] = TURNS_PER_DAY
    player['bag_size']= 10 
    player['Name'] = ''

    clear_fog(fog, player)
    
# This function draws the entire map, covered by the fof
def draw_map(game_map, fog, player):
    return

# This function draws the 3x3 viewport
def draw_view(game_map, fog, player):
    return

# This function shows the information for the player
def show_information(player):
    return

# This function saves the game
def save_game(game_map, fog, player):
    # save map
    # save fog
    # save player
    return
        
# This function loads the game
def load_game(game_map, fog, player):
    # load map
    # load fog
    # load player
    return

def show_main_menu():
    print()
    print("--- Main Menu ----")
    print("(N)ew game")
    print("(L)oad saved game")
    print("(H)igh scores")
    print("(Q)uit")
    print("------------------")

def show_town_menu():
    print()
    # TODO: Show Day
    print("----- Sundrop Town -----")
    print("(B)uy stuff")
    print("See Player (I)nformation")
    print("See Mine (M)ap")
    print("(E)nter mine")
    print("Sa(V)e game")
    print("(Q)uit to main menu")
    print("------------------------")

def show_shop_menu():
    print('----------------------- Shop Menu -------------------------')
    print('(P)ickaxe upgrade to Level 2 to mine silver ore for 50 GP')
    print (f'(B)ackpack upgrade to carry {player['bag_size']+2} items for {player['bag_size']*2} GP')
    print('(L)eave shop')
    print('-----------------------------------------------------------')
    print(f'GP: {player['GP']}')
    print('-----------------------------------------------------------')

def player_info():
    print('----- Player Information -----')
    print(f'Name: {player['Name']}')
    print('Portal position: (7, 1)')
    print('Pickaxe level: 2 (silver)')
    print('------------------------------')
    print('Load: 0 / 12')
    print('------------------------------')
    print(f'GP: {player['GP']}')
    Steps taken: 16
    print('------------------------------')
            

#--------------------------- MAIN GAME ---------------------------
game_state = 'main'
print("---------------- Welcome to Sundrop Caves! ----------------")
print("You spent all your money to get the deed to a mine, a small")
print("  backpack, a simple pickaxe and a magical portal stone.")
print()
print("How quickly can you get the 1000 GP you need to retire")
print("  and live happily ever after?")
print("-----------------------------------------------------------")

# TODO: The game!
town_menu_running = True  
main_menu_running = True    
shop_menu_running = True
while main_menu_running:
    show_main_menu()
    choice = input("Your choice? ")
    choice = choice.lower()
    if choice == "n":
        name = input('Greetings, miner! What is your name? ')
        player['Name']= name
        print(f'{player['Name']}')
        print(f'Pleased to meet you, {name}. Welcome to Sundrop Town!')

        initialize_game(game_map, fog, player)

        while town_menu_running:
            show_town_menu()
            town_choice = input('Your Choice? ')
            town_choice = town_choice.lower()

            if town_choice == 'q':
                print('returning to main menu...')
                break
            elif town_choice == 'b':
                
                while shop_menu_running:
                    show_shop_menu()
                    buy_choice = input('Your Choice? ')
                    if buy_choice == "b":
                        if player['GP'] >= player['bag_size']*2: 
                            print(f'Congratulations! You can now carry {player['bag_size']} items!')
                        else:
                            print("Purchase Failed. You do not have enough GP to purchase this product")
                    elif buy_choice == ('p'):
                        # advanced, do later
                        pass
                    elif buy_choice == ('l'):
                        break
                    else:
                        print('Invalid choice. Try again')




    elif choice == 'l':
        # do layter
        pass
    elif choice == 'i':
        
    elif choice == "q":
        print('Hope you had fun. Goodbye!')
        break
