from random import randint

width = 10
height = 10
init_bomb = 10
bob = []

def create(start: list):
    """create the table of the game with the current difficulty after the first dig
    intialisation of an empty grid of [A,B]
    A : state (0:invisible ; 1:visible)
    B : object (-1: bomb ; 0:empty and nearby clear ; 1: one bomb nearby..)"""
    global bob
    bob=[[[0, ""] for j in range(width)] for i in range(height)]

    # start : coordinate of the first clic
    x = start[0]
    y = start[1]
    bob[y][x] = [1,0]
    
    # number of bombs placed
    count=0
    
    # put bombs in safe places until the max number of bombs on board
    while count < init_bomb :
        cellX, cellY = randint(0,height-1), randint(0,width-1)
        if ((cellX < x-1 or cellX > x+1) or (cellY < y-1 or cellY > y+1)) or (bob[cellY][cellX][1] != -1) :
            bob[cellY][cellX][1] = -1
            count += 1
    
    nb_bomb()
    

def nb_bomb():
    """initialise number of bombs around each cell in the grid"""
    for h in range(height):
        for w in range(width):
            if bob[h][w][1] == -1:  # if it's not a bomb we count the nearby bombs
                continue

            #initiating variables storing the obstruction in either of those direction (0:no obstruction, 1:obstruction)
            right=0
            left=0
            up=0
            down=0
            
            if w==0:
                left=1
            elif w==width-1:
                right=1
            if h==0:
                up=1
            elif h==height-1:
                down=1

            # using an accumulator we will check every square nearby and store the number of bombs.
            nb_bomb = 0
            
            # using a nested loop we can go trough every square within a radius of one.
            for y in range((h-1)+up,(h+1)-down +1):
                for x in range((w-1)+left,(w+1)-right +1):

                    # with -1 being a bomb
                    if bob[y][x][1] == -1:
                        nb_bomb +=1
                        
            # (-1: a bomb, 0: no bomb, 1:one bomb nearby, 2:..)
            bob[h][w][1] = nb_bomb

            

print(create([5,5]))

for row in bob:
    for cell in row:
        print(cell, end=" ")
    print()