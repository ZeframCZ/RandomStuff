import matplotlib.pyplot as plt
import matplotlib.animation as animation

from grid_map import grid_map
import copy
from random import randrange

WALL = 0.0
ROUTE = 0.3
RE_ROUTE = 0.5

exit_found = False
exit_x = 0
exit_y = 0


current_x = 0
current_y = 0
current_dir_x = 1
current_dir_y = 0
steps = 0

all_data = []

def pick_left(current_dir_x, current_dir_y):
    if (current_dir_x, current_dir_y) == (0, 1):
        return -1, 0
    if (current_dir_x, current_dir_y) == (1, 0):
        return 0, 1
    if (current_dir_x, current_dir_y) == (0, -1):
        return 1, 0
    if (current_dir_x, current_dir_y) == (-1, 0):
        return 0, -1

def pick_right(current_dir_x, current_dir_y):
    if (current_dir_x, current_dir_y) == (0, 1):
        return 1, 0
    if (current_dir_x, current_dir_y) == (1, 0):
        return 0, -1
    if (current_dir_x, current_dir_y) == (0, -1):
        return -1, 0
    if (current_dir_x, current_dir_y) == (-1, 0):
        return 0, 1

def pick_random(current_dir_x, current_dir_y):
    possibilities = []
    if (current_dir_x, current_dir_y) == (0, 1):
        possibilities = [[-1, 0],[1, 0],[0, 1]]

    if (current_dir_x, current_dir_y) == (0, -1):
        possibilities = [[-1, 0],[1, 0],[0, -1]]

    if (current_dir_x, current_dir_y) == (1, 0):
        possibilities = [[0, -1],[1, 0],[0, 1]]

    if (current_dir_x, current_dir_y) == (-1, 0):
        possibilities = [[-1, 0],[0, -1],[0, 1]]
    
    return possibilities[randrange(0,3,1)]

def determine_next_dir(current_dir_x, current_dir_y):
    #Choose right hand direction
    possible_dir_x, possible_dir_y = pick_right(current_dir_x, current_dir_y)
    if data[current_x+possible_dir_x][current_y+possible_dir_y] != WALL:
        return possible_dir_x, possible_dir_y
    
    if data[current_x+current_dir_x][current_y+current_dir_y] != WALL:
        return current_dir_x, current_dir_y

    possible_dir_x, possible_dir_y = pick_left(current_dir_x, current_dir_y)
    if data[current_x+possible_dir_x][current_y+possible_dir_y] != WALL:
        return possible_dir_x, possible_dir_y


    while(data[current_x+possible_dir_x][current_y+possible_dir_y] == WALL):
        possible_dir_x, possible_dir_y = pick_random(possible_dir_x, possible_dir_y)
    
    return possible_dir_x, possible_dir_y

def get_start(size_y, size_x):
    #left edge
    for col in range(size_y):
        if int(grid_map[0,col]) != WALL:
            return col, 0
    #upper edge
    for row in range(size_x):
        if int(grid_map[row, 0]) != WALL:
            return 0, row

def get_exit(size_y, size_x):
    #Right edge
    for col in range(size_y):
        if int(grid_map[size_x,col]) != WALL:
            return size_x-1, col-1
    #Bottom edge
    for row in range(size_x):
        if int(grid_map[row, size_y]) != WALL:
            return row-1, size_y-1

def get_size():
    a, b = max(grid_map)
    return b+1, a


size_x, size_y = get_size()
exit_y, exit_x = get_exit(size_x, size_y)
current_x, current_y = get_start(size_x, size_y)

#Get the map data
data = []
one_row = ()
for row in range(size_x):
    for col in range(size_y+1):
        one_row += (int(grid_map[col ,row]), )
    data.append(list(one_row))
    one_row = ()




#Search for the route
while(not exit_found):
    #Take the next step
    current_x += current_dir_x
    current_y += current_dir_y
    current_dir_x, current_dir_y = determine_next_dir(current_dir_x, current_dir_y)
    print(f"{current_x} {current_y}")
    #Save data for animation
    all_data.append(copy.deepcopy(data))
    #Paint the route
    if data[current_x][current_y] == ROUTE:
        data[current_x][current_y] = RE_ROUTE
    else:
        data[current_x][current_y] = ROUTE
    #Total steps = steps
    steps += 1
   
    
    #FIN! 
    if current_x >= exit_x and current_y >= exit_y:
        exit_found = True


print(f"in {steps} steps. {len(all_data)}")


#Draw the anim
i=0

def generate_data():
    global i
    if i< len(all_data)-1:
        i+= 1
    else:
        i = 0
    return all_data[i]

def update(data):
    mat.set_data(data)
    return mat 

def data_gen():
    while True:
        global i
        if i< len(all_data)-1:
            i+= 1
        else:
            i = 0
        yield all_data[i]


fig, ax = plt.subplots()
mat = ax.matshow(generate_data())
ani = animation.FuncAnimation(fig, update, data_gen, interval=5,save_count=0)
plt.show()
