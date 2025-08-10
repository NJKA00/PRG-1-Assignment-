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
in_town = True
prices = {}
prices['copper'] = (1, 3)
prices['silver'] = (5, 8)
prices['gold'] = (10, 18)

# This function loads a map structure (a nested list) from a file
# It also updates MAP_WIDTH and MAP_HEIGHT
def load_map(filename, map_struct):
    global MAP_WIDTH
    global MAP_HEIGHT
    
    map_struct.clear()
    
    # TODO: Add your map loading code here
    with open(filename, 'r') as file:
        map_struct = file.readlines()
        index = 0
        for line in map_struct:
            map_struct[index] = line.replace("\n","")
            index+= 1
    line_index = 0
    map_list = []
    for line in map_struct:
        map_list.append([])
        for chr in line:
            map_list[line_index].append(chr)
        
        line_index +=1
            
    MAP_WIDTH = len(map_struct[0])
    MAP_HEIGHT = len(map_struct)
    return map_list

# This function clears the fog of war at the 3x3 square around the player
def clear_fog(fog, player):
    if player['torch']:
        view_diameter = 2
    else:
        view_diameter = 1
    x_min = player['x'] - view_diameter
    if x_min<0:
        x_min = 0 
    x_max = player['x'] + view_diameter
    if x_max > MAP_WIDTH-1:
        x_max = MAP_WIDTH-1
    y_min = player['y'] - view_diameter
    if y_min<0:
        y_min = 0
    y_max = player['y'] + view_diameter
    if y_max > MAP_HEIGHT-1:
        y_max = MAP_HEIGHT-1


    x_range = range(x_min, x_max+1)
    y_range = range (y_min,y_max+1)
    for y in y_range:   
        for x in x_range:
            if fog[y][x] == '?':
                fog[y][x] = ' '

def initialize_game(game_map, fog, player):
    # initialize map
    # load_map("level1.txt", game_map)

    # TODO: initialize fog
    
    # TODO: initialize player
    #   You will probably add other entries into the player dictionary
    player['x'] = 0
    player['y'] = 0
    player['copper'] = 0
    player['silver'] = 0
    player['gold'] = 0
    player['GP'] = 1000
    player['day'] = 1
    player['steps'] = 0
    player['turns'] = TURNS_PER_DAY
    player['bag_size']= 10 
    player['name'] = ''
    player['Pickaxe Level'] = 1
    player['Pickaxe material'] = ['copper', 'silver', 'gold']
    player['torch'] = False
    player['load'] = 0
    player['bagpack load'] = {}
    player['bagpack load']['c'] = 0
    player['bagpack load']['s'] = 0
    player['bagpack load']['g'] = 0
    clear_fog(fog, player)
    
# This function draws the entire map, covered by the fof
def draw_map(game_map, fog, player):
    print(f"+{"-"*MAP_WIDTH}+")
    y_index = 0
    for line in fog:
        print("|",end="")
        x_index = 0
        for chr in line:
            if (x_index == player['x'] and y_index == player['y'] and in_town == False)or (x_index==0 and y_index==0 and in_town==True):
                print('M',end='')
            elif (x_index == player['x'] and y_index == player['y'] and in_town == True):
                print('P', end ='')
            elif chr == ' ':
                print(game_map[y_index][x_index], end='')
            else:
                print(chr,end='')
            x_index += 1
        print("|")
        y_index +=1
    print(f"+{"-"*MAP_WIDTH}+")


# This function draws the 3x3 viewport
def draw_view(game_map, player):
    if player['torch']:
        view_diameter = 2
    else:
        view_diameter = 1
    x_min = player['x'] - view_diameter
    x_max = player['x'] + view_diameter
    y_min = player['y'] - view_diameter
    y_max = player['y'] + view_diameter
    clear_fog(fog, player)
    x_range = range(x_min, x_max+1)
    y_range = range (y_min,y_max+1)
    print(f'+{'-'*len(x_range)}+')
    for y in y_range: 
        print('|',end='')
        for x in x_range:
            if y<0 or x<0 or x> MAP_WIDTH-1 or y> MAP_HEIGHT-1 :
                print('#',end ='')
            elif x == player['x'] and y ==player['y']:
                print('M', end='')
        
            else:
                # print(f"[ {y} {x} ]", end='')
                print(game_map[y][x], end='')
        print('|')
    print(f'+{'-'*len(x_range)}+')
    

# This function saves the game
# def save_game(game_map, fog, player):
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
    print(f'(P)ickaxe upgrade to Level {player['Pickaxe Level']+1} to mine silver ore for 50 GP')
    print (f'(B)ackpack upgrade to carry {player['bag_size']+2} items for {player['bag_size']*2} GP')
    print('(T)orch to increase viewing area from 1 stud to 2 studs')
    print('(L)eave shop')
    print('-----------------------------------------------------------')
    print(f'GP: {player['GP']}')
    print('-----------------------------------------------------------')

def player_info():
    print('----- Player Information -----')
    print(f'Name: {name}')
    print(F'Portal position: ({player['x']}, {player['y']})')
    print(f'Pickaxe level: {player['Pickaxe Level']} ({player['Pickaxe material'][player['Pickaxe Level']-1]})')
    print('------------------------------')
    print(f'Load: {player['load']} / {player['bag_size']}')
    print('------------------------------')
    print(f'GP: {player['GP']}')
    print(f'Steps taken: {player['steps']}')
    print('------------------------------')

def create_fog(fog):
    global MAP_HEIGHT
    global MAP_WIDTH
    fog.clear()
    line_index = 0
    for line in range(MAP_HEIGHT):
        fog.append([])
        for chr in range(MAP_WIDTH):
            fog[line_index].append('?')
        #     print('?', end='')
        # print()
        line_index +=1
    # print(fog)    

def player_movement(movement):
    if movement == 'w' and player['y']!= 0:
        player['y']-= 1
    elif movement == 's' and player['y'] != MAP_HEIGHT-1:
        player['y'] += 1
    elif movement == 'a' and player['x']!= 0:
        player['x'] -= 1
    elif movement == 'd' and player['x']!= MAP_WIDTH-1:
        player['x'] += 1
    

def game_menu():
    print(f'Turns left: {player['turns']} Load: {player['load']} / {player['bag_size']} Steps: {player['steps']}')
    movement = input("Action?")
    movement = movement.lower()
    print('(WASD) to move')
    print('(M)ap, (I)nformation, (P)ortal, (Q)uit to main menu')

def mine_tile():
    if player['load'] >= player['bag_size']:
        print("Your bag is full! You can't mine anymore.")
        return
    current_tile = game_map[player['y']][player['x']]
    current_tile = current_tile.lower()
    if current_tile == 'c':
        game_map[player['y']][player['x']] = ' '
        amt =randint(1,5)
        print(f'{amt} copper mined')
        if sum(player['bagpack load'].values())+amt>= player['bag_size']:
            amt = player['bag_size']-sum(player['bagpack load'].values())
            player['bagpack load']['c']+= amt
        else:
            player['bagpack load']['c']+= amt

        
    
    elif current_tile == 's':
        game_map[player['y']][player['x']] = ' '
        amt =randint(1,3)
        print(f'{amt} silver mined')
        if sum(player['bagpack load'].values())+amt>= player['bag_size']:
            amt = player['bag_size']-sum(player['bagpack load'].values())
            player['bagpack load']['s']+= amt
        else:
            player['bagpack load']['s']+= amt

    
    elif current_tile == 'g':
        game_map[player['y']][player['x']] = ' '
        amt =randint(1,2)
        print(f'{amt} gold mined')
        if sum(player['bagpack load'].values())+amt>= player['bag_size']:
            amt = player['bag_size']-sum(player['bagpack load'].values())
            player['bagpack load']['g']+= amt
        else:
            player['bagpack load']['g']+= amt

    else:
        amt = 0

    player['load'] += amt

def sell_mat():
    total_sale=0
    for ore in player['bagpack load']:
        if ore == 'c':
            copper_price= randint(1, 3)
        elif ore == 's':
            silver_price = randint(5, 8)
        elif ore == 'g':
            gold_price = randint(10, 18)
        
    price_list = {"c":copper_price,
                  "s":silver_price,
                  "g":gold_price }
    for ore, amount in player['bagpack load'].items():
        if amount > 0:
            ore_name = mineral_names[ore.upper()]
            prices = price_list[ore]
            sale_value = prices * amount
            print(f"Sold {amount} {ore_name} for {prices} GP each: +{sale_value} GP")
            total_sale += sale_value
            player['bagpack load'][ore] = 0  
            player[ore_name] += amount       
    player['GP'] += total_sale
    player['load'] = 0
    if total_sale > 0:
        print(f"Total sale: {total_sale} GP\n")
    else:
        print("You had no ore to sell.\n")
def save_game():
    with open('Saved game.txt', "w") as file:
        player_prog = ''
        for stat, value in player.items():
            player_prog += f'{stat}:{value}\n'
        file.write(player_prog)
    with open ('fog_folder', 'w') as file:
        fog_content = ''
        for column in fog:
            for tile in column:
                fog_content += f'{tile}'
            fog_content+=f"\n"
        file.write(fog_content)
    with open('map_folder','w') as file:
        map_content =''
        for column in game_map:
            for tile in column:
                map_content += f"{tile}"
            map_content += f'\n'
        file.write(map_content)

# def valid_movement(next_y,next_x):

#     next_tile = game_map[next_y][next_x]
#     next_tile = next_tile.lower()
#     if next_tile in ['c','s','g'] and sum(player['current_load'].values()) >= player['load']:
#         print(f"cannot mine")
#         return False
#     elif movement == "d" and not player["x"]==MAP_WIDTH-1:
#         next_x = player["x"] + 1 
#         if valid_movement(player['y'],next_x):
#             player["x"]+=1
#     elif movement == "a" and not player["x"]==MAP_WIDTH-1:
#         next_x = player["x"] - 1 
#         if valid_movement(player['y'],next_x):
#             player["x"]-=1
#     elif movement == "w" and not player["y"]==MAP_HEIGHT-1:
#         next_y = player["y"] + 1 
#         if valid_movement(next_y,player['x']):
#             player["y"]+=1
#     elif movement == "s" and not player["y"]==MAP_HEIGHT-1:
#         next_y = player["y"] -1
#         if valid_movement(next_y,player['x']):
#             player["y"]-=1
#     else:
#         return True

def valid_movement(direction):
    dx, dy = 0, 0
    if direction == 'w':
        dy = -1
    elif direction == 's':
        dy = 1
    elif direction == 'a':
        dx = -1
    elif direction == 'd':
        dx = 1
    else:
        return False  # invalid direction

    new_x = player['x'] + dx
    new_y = player['y'] + dy

    # Check map boundaries
    if new_x < 0 or new_x >= MAP_WIDTH or new_y < 0 or new_y >= MAP_HEIGHT:
        return False

    # Optionally prevent movement onto certain tiles (like walls or full bag mining)
    tile = game_map[new_y][new_x].lower()

    # Prevent mining if bag is full
    if tile in ['c', 's', 'g'] and player['load'] >= player['bag_size']:
        print("You can't mine here — your bag is full!")
        return False

    return True










#--------------------------- MAIN GAME ---------------------------
#game_state = 'main'
print("---------------- Welcome to Sundrop Caves! ----------------")
print("You spent all your money to get the deed to a mine, a small")
print("  backpack, a simple pickaxe and a magical portal stone.")
print()
print("How quickly can you get the 500 GP you need to retire")
print("  and live happily ever after?")
print("-----------------------------------------------------------")

town_menu_running = True  
main_menu_running = True    
shop_menu_running = True
while main_menu_running:
    show_main_menu()
    choice = input("Your choice? ")
    choice = choice.lower()

    if choice == "n" or choice =='l':

        if choice == "n":
            initialize_game(game_map, fog, player)
            name = input('Greetings, miner! What is your name? ')
            player['name']= name

            game_map = load_map("level1.txt", game_map)
            create_fog(fog)
        elif choice == 'l':
            #initialize_game(game_map, fog, player)
            with open('Saved game.txt', 'r') as file:
                player.clear()  # remove old data
                for line in file:
                    stat, value = line.strip().split(':', 1)
                    if value.isdigit():
                        value = int(value)
                    if value == "True":
                        value = True
                    elif value == "False":
                        value=False
                    elif stat == "bagpack load":
                        value = value[1:-1]  # remove the braces "{}"
                        value = value.replace("'", "")  # remove single quotes
                        mineral_list = value.split(",")
                        player['bagpack load'] = {}
                        for item in mineral_list:
                            mineral, amount = item.split(":")
                            player['bagpack load'][mineral.strip()] = int(amount.strip())
                        
                            print(game_map)
                    else:
                        try:
                            value = int(value)
                        except ValueError:
                            pass
                    player[stat] = value
                
            game_map = load_map('map_folder',game_map)
            fog = load_map('fog_folder',fog)
            player['pickaxe material'] = ['copper','silver','gold']

        print(f'Pleased to meet you, {name}. Welcome to Sundrop Town!')
        while town_menu_running:
            in_town = True 
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
                    buy_choice = buy_choice.lower()
                    if buy_choice == "b":
                        if player['GP'] >= player['bag_size']*2: 
                            player['GP']-=player['bag_size']*2
                            player['bag_size']+=2
                            
                            print(f'Congratulations! You can now carry {player['bag_size']} items!')
                        else:
                            print("Purchase Failed. You do not have enough GP to purchase this product")
                    elif buy_choice == ('p'):
                        # advanced, do later
                        pass
                    elif buy_choice == ('l'):
                        break
                    elif buy_choice == ('t'): 
                        if player['torch'] == False:
                            if player['GP'] >= 50:
                                player['GP']-=50
                                print(f'Congratulations! You can now own a torch, increasing your view range!')
                                player['torch'] = True
                            else:
                                print("Purchase Failed. You do not have enough GP to purchase this product.")
                        else:
                            print('You only can own one torch.')

                    else:
                        print('Invalid choice. Try again')
                        
            elif town_choice == ('i'):
                player_info()
            elif town_choice == ('m'):
                # game_map = load_map("level1.txt", game_map)
                draw_map(game_map, fog, player) 
            
                

            elif town_choice == ('e'):
                in_town = False
                print('---------------------------------------------------')
                print(f'{f'DAY {player['day']}':^51}')
                print('---------------------------------------------------')
                print(f'Day {player['day']}')
                
                while True:
                    draw_view(game_map, player)
                    print(f'Turns left: {TURNS_PER_DAY} Load: {player['load']} / {player['bag_size']} Steps: {player['steps']}')
                    print('(WASD) to move')
                    print('(M)ap, (I)nformation, (P)ortal, (Q)uit to main menu')
                    movement = input("Action?")
                    movement = movement.lower()
                    print(movement)
                
                    if movement in ['w','a','s','d']:
                        valid_movement(player_movement(movement))

                        player_movement(movement)
                        clear_fog(fog, player)
                        TURNS_PER_DAY-=1
                        
                    elif movement == 'm':
                        draw_map(game_map, fog, player)
                    elif movement == 'i':
                        player_info()
                    elif movement == 'q':
                        break
                    elif movement == 'p':
                        sell_mat()
                        player['day']+= 1
                        TURNS_PER_DAY = 20
                        break
                    
                    else:
                        print("Invalid option. Please try again.")
                    if player['x'] == 0 and player['y']==0:
                        sell_mat()
                        break
                    player['steps']+=1
                    mine_tile()
                    print(player['bagpack load'])
                    if TURNS_PER_DAY<=0:
                        sell_mat()
                        player['day']+= 1
                        TURNS_PER_DAY=20
                        break
                    


                        



            elif town_choice == ('v'):
                save_game()
                print("Game Saved!")
            elif town_choice == "njka":
                clear_fog(fog,player)
                draw_map(game_map,fog,player)
            elif town_choice == ('l'):
                pass
            else: 
                print("Invalid option, please try again.")
                continue


    
        
    elif choice == "q":
        print('Hope you had fun. Goodbye!')
        break
    else: 
        print("Invalid option, please try again.")
        continue