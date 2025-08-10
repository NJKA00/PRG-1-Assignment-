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
    
    with open(filename, 'r') as file:
        map_struct = file.readlines()
        index = 0
         # Replace newline with an empty string so only map characters remain
        for line in map_struct:
            map_struct[index] = line.replace("\n","")
            index+= 1
    #convert each string line into a list of characters
    line_index = 0
    map_list = []
    for line in map_struct:
        map_list.append([])
        # Add the character (tile) to the corresponding row
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
    x_min = player['x'] - view_diameter #Calculates the minimum x-coordinate of the visible area around the player
    if x_min<0:
        x_min = 0 #Ensures the leftmost visible boundary doesn’t go outside the map
    x_max = player['x'] + view_diameter
    if x_max > MAP_WIDTH-1:
        x_max = MAP_WIDTH-1
    y_min = player['y'] - view_diameter
    if y_min<0: #Prevents the top boundary from going beyond the top of the map
        y_min = 0
    y_max = player['y'] + view_diameter #Calculates the maximum y-coordinate of the visible area
    if y_max > MAP_HEIGHT-1:
        y_max = MAP_HEIGHT-1

#Creates ranges for all x and y coordinates in the player’s visible square area.
    x_range = range(x_min, x_max+1) 
    y_range = range (y_min,y_max+1)
    for y in y_range:   
        for x in x_range:
            #If the tile in fog is '?' (meaning unexplored), replace it with a space ' ' (meaning explored/visible
            if fog[y][x] == '?':
                fog[y][x] = ' '

def initialize_game(game_map, fog, player):
    # initialize map
    # load_map("level1.txt", game_map)

    # TODO: initialize fog

    player['x'] = 0
    player['y'] = 0
    player['copper'] = 0
    player['silver'] = 0
    player['gold'] = 0
    player['GP'] = 450
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
    
# This function draws the entire map, covered by the fog
def draw_map(game_map, fog, player):
    print(f"+{'-' * MAP_WIDTH}+")
    for y_index in range(MAP_HEIGHT):
        print("|", end="")
        for x_index in range(MAP_WIDTH):
            if x_index == player['x'] and y_index == player['y']:
                print('M', end='')  # Player at (0,0)
            elif x_index == player.get('portal_x') and y_index == player.get('portal_y'):
                print('P', end='')  # Portal at previous player location
            elif fog[y_index][x_index] == ' ':
                print(game_map[y_index][x_index], end='')
            else:
                print('?', end='')
        print("|")
    print(f"+{'-'*MAP_WIDTH}+")

def place_portal_and_move_player(player):
    # Save old player position as portal
    old_x, old_y = player['x'], player['y']
    player['portal_x'], player['portal_y'] = old_x, old_y

    # Move player to (0,0)
    player['x'], player['y']=0,0

def teleport_to_portal(player):
    if 'portal_x' in player and 'portal_y' in player:
        old_x, old_y = player['x'], player['y']
        new_x, new_y = player['portal_x'], player['portal_y']
        
        # Move player to portal
        player['x'], player['y'] = new_x, new_y
        
        # Remove the portal since player is there now
        del player['portal_x']
        del player['portal_y']
        
        # Optionally, mark old player spot as empty (depends on your map logic)
        # For example:
        # game_map[old_y][old_x] = '.'

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
                
                print(game_map[y][x], end='')
        print('|')
    print(f'+{'-'*len(x_range)}+')
    

# # This function saves the game
# def save_game():
#     with open('Saved game.txt', "w") as file:
#         player_prog = ''
#         for stat, value in player.items(): # Iterates over each stat in the player dictionary.
#             player_prog += f'{stat}:{value}\n'
#         file.write(player_prog)
#     with open ('fog_folder', 'w') as file:
#         fog_content = ''
#         for column in fog: # Iterates through each row/column of the fog array.
#             for tile in column:# Iterates over each fog tile in the row.
#                 fog_content += f'{tile}'
#             fog_content+=f"\n"
#         file.write(fog_content)
#     with open('map_folder','w') as file:
#         map_content =''
#         for column in game_map:
#             for tile in column:
#                 map_content += f"{tile}"
#             map_content += f'\n'
#         file.write(map_content)
#     return
        
# This function loads the game

def save_game():
    name = player['name']
    
    # Save player data
    with open(f'save_{name}.txt', "w") as file:
        for stat, value in player.items():
            if stat == 'bagpack load':
                serialized = ','.join([f'{k}:{v}' for k, v in value.items()]) # Convert backpack into a single string
                file.write(f'{stat}:{serialized}\n')
            else:
                file.write(f'{stat}:{value}\n')

    # Save fog
    with open(f'fog_{name}.txt', 'w') as file:
        for row in fog:
            file.write(''.join(row) + '\n')

    # Save map
    with open(f'map_{name}.txt', 'w') as file:
        for row in game_map:
            file.write(''.join(row) + '\n')




def load_game(game_map, fog, player, name):
    try:
        
        with open(f'save_{name}.txt', 'r') as file: 
            player.clear()
            for line in file:
                stat, value = line.strip().split(':', 1)
                
                if value == "True":
                    value = True
                elif value == "False":
                    value = False
                elif value.isdigit():
                    value = int(value)

                if stat == "bagpack load":
                    player['bagpack load'] = {}
                    items = value.split(",")
                    for item in items:
                        k, v = item.strip().split(":")
                        player['bagpack load'][k.strip()] = int(v.strip())
                else:
                    player[stat] = value

        # These lines already match the save_game function
        game_map[:] = load_map(f'map_{name}.txt', game_map)
        fog[:] = load_map(f'fog_{name}.txt', fog)

        player['Pickaxe material'] = ['copper', 'silver', 'gold']
        return True
    except FileNotFoundError:
        print("Save file not found.")
        return False
  

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
    print(f'Day {player['day']}')
    print("----- Sundrop Town -----")
    print("(B)uy stuff")
    print("See Player (I)nformation")
    print("See Mine (M)ap")
    print("(E)nter mine")
    print("Sa(V)e game")
    print("(Q)uit to main menu")
    print("------------------------")

#prints all choices available in shop
def show_shop_menu():
    print('----------------------- Shop Menu -------------------------')
    
    print (f'(B)ackpack upgrade to carry {player['bag_size']+2} items for {player['bag_size']*2} GP')
    print('(T)orch to increase viewing area')
    print('(L)eave shop')
    print('-----------------------------------------------------------')
    print(f'GP: {player['GP']}')
    print('-----------------------------------------------------------')

#prints all player info
def player_info():
    print('----- Player Information -----')
    print(f'Name: {name}')
    print(F'Portal position: ({player['x']}, {player['y']})')
    print(f'Pickaxe level: {player['Pickaxe Level']} ({player['Pickaxe material'][player['Pickaxe Level']-1]})')
    print(f'Gold: {player['bagpack load']['g']} ')
    print(f'Silver: {player['bagpack load']['s']} ')
    print(f'Copper: {player['bagpack load']['c']} ')
    print('------------------------------')
    print(f'Load: {player['load']} / {player['bag_size']}')
    print('------------------------------')
    print(f'GP: {player['GP']}')
    print(f'Steps taken: {player['steps']}')
    print('------------------------------')

#create fog overlaying the map
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

# identifies the movement of the player, move accordingly if pressing w,a,s,d
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
        print(f'You mined {amt} pieces of copper.')
        if sum(player['bagpack load'].values())+amt>= player['bag_size']:
            amt = player['bag_size']-sum(player['bagpack load'].values())
            player['bagpack load']['c']+= amt
        else:
            player['bagpack load']['c']+= amt

        
    
    elif current_tile == 's':
        game_map[player['y']][player['x']] = ' '
        amt =randint(1,3)
        print(f'You mined {amt} pieces of silver.')
        if sum(player['bagpack load'].values())+amt>= player['bag_size']:
            amt = player['bag_size']-sum(player['bagpack load'].values())
            player['bagpack load']['s']+= amt
        else:
            player['bagpack load']['s']+= amt

    
    elif current_tile == 'g':
        game_map[player['y']][player['x']] = ' '
        amt =randint(1,2)
        print(f'You mined {amt} pieces of gold')
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
            print(f"You sell {amount} {ore_name} ore for {prices} GP: +{sale_value} GP")
            total_sale += sale_value
            player['bagpack load'][ore] = 0  
            player[ore_name] += amount       
    player['GP'] += total_sale
    player['load'] = 0



    if total_sale > 0 and player['GP'] < 500:
        print(f"You now have {player['GP']} GP!")
    
    elif player['GP'] >= 500:

        print(f"{'-'*51}\nWoo-hoo! Well done, {name}, you have {player['GP']} GP!\nYou now have enough to retire and play video games every day.\nAnd it only took you {player['day']} days and {player['steps']} steps! You win!\n{'-'*51}")
        with open('high_scores.txt', 'a') as file:
            file.write(f"{player['name']}:{player['GP']}:{player['steps']}\n")
        return 'won'
        
            
    else:
        print("You had no ore to sell.\n")




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

def show_high_scores():
    try:
        with open("high_scores.txt", "r") as file:
            scores = []
            for line in file:
                name, gp, steps = line.strip().split(":")
                gp = int(gp)
                steps = int(steps)
                scores.append((gp, steps, name))

            # Sort by GP descending, then steps ascending
            scores.sort(key=lambda x: (-x[0], x[1]))

            print("\n----- Top 5 High Scores -----")
            for i, (gp, steps, name) in enumerate(scores[:5], start=1):
                print(f"{i}. {name} - GP: {gp}, Steps: {steps}")
            print("-----------------------------\n")
    except FileNotFoundError:
        print("No high scores yet.")










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
            town_menu_running=True
            initialize_game(game_map, fog, player)
            name = input('Greetings, miner! What is your name? ')
            player['name']= name

            game_map = load_map("level1.txt", game_map)
            create_fog(fog)
        elif choice == 'l':
            town_menu_running=True
            load_game(game_map, fog, player, name)

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
                            continue
                    
                
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
                
                draw_map(game_map, fog, player) 
            
                

            elif town_choice == ('e'):
                teleport_to_portal(player)
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
                    
                
                    if movement in ['w','a','s','d']:
                        

                        player_movement(movement)
                        clear_fog(fog, player)
                        TURNS_PER_DAY-=1
                        
                    elif movement == 'm':
                        draw_map(game_map, fog, player)
                    elif movement == 'i':
                        player_info()
                    elif movement == 'q':
                        in_town = False
                    elif movement == 'p':
                        print('You place your portal stone here and zap back to town.')
                        result = sell_mat()
                        place_portal_and_move_player(player)
                        if result == 'won':
                            town_menu_running = False
                            break
                        player['day']+= 1
                        TURNS_PER_DAY = 20
                        break
                    
                    else:
                        print("Invalid option. Please try again.")
                    if player['x'] == 0 and player['y']==0:
                        result = sell_mat()
                        if result == 'won':
                            town_menu_running = False
                            break
                        break
                    player['steps']+=1
                    mine_tile()
                    print(player['bagpack load'])
                    if  player['load']>=player['bag_size']:
                        place_portal_and_move_player(player)
                        in_town = True
                        TURNS_PER_DAY = 20
                        player['day']+=1
                        player['x'] = 0
                        player['y'] = 0
                        print("You can't carry any more, so you can't go that way.\nYou are exhausted.\nYou place your portal stone here and zap back to town.")
                        result = sell_mat()
                        if result == 'won':
                            town_menu_running = False
                            break
                        break
                    if TURNS_PER_DAY<=0:
                        place_portal_and_move_player(player)
                        print('You are exhausted.\nYou place your portal stone here and zap back to town.')
                        result = sell_mat()
                        if result == 'won':
                            town_menu_running = False
                            break
                        player['day']+= 1
                        TURNS_PER_DAY=20
                        break

                    


                        



            elif town_choice == ('v'):
                save_game()
                print("Game Saved!")
            elif town_choice == "njka":
                clear_fog(fog,player)
                draw_map(game_map,fog,player)
            
            else: 
                print("Invalid option, please try again.")
                continue


    
        
    elif choice == "q":
        print('Hope you had fun. Goodbye!')
        break
    elif choice =='h':
        show_high_scores()
    else: 
        print("Invalid option, please try again.")
        continue