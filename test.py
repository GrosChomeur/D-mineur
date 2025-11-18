#from minesweeper import *
from tkinter import *
from random import randint





class GameState: # we use a class to make cleaner variable management
    def __init__(self, width=9, height=9, init_bomb=10, size=200, theme=randint(0,1), difficulty=0):
        self.width = width
        self.height = height
        self.init_bomb = init_bomb
        self.bomb = init_bomb
        self.size = size
        self.theme = theme
        self.difficulty = difficulty  
        
        # Create empty board
        self.bob = [[[0, 0] for w in range(width)] for h in range(height)]
        
        # different themes color palettes
        self.color_board = {
            1: {"hiddenfill": "#99809C", "activefill": "#78A054", "fill": "#D4878D",
                "textcolor": "darkred", "border": "#FFD9DA", "handle": "#4f4f4f", "flag": "crimson"},
            2: {"hiddenfill": "#773344", "activefill": "#FF9F1C", "fill": "#F4CAE0",
                "textcolor": "#626430", "border": "#230903", "handle": "#F1E9DB", "flag": "#7EC4CF"}
        }
        
        self.set_colors()

    def set_colors(self):
        self.theme = self.theme % 2 + 1
        colors = self.color_board[self.theme]
        self.hidden = colors["hiddenfill"]
        self.active = colors["activefill"]
        self.fill = colors["fill"]
        self.textcolor = colors["textcolor"]
        self.border = colors["border"]
        self.handle = colors["handle"]
        self.flag = colors["flag"]
        self.flag_colors = [
    ["", "", "", "", "", "", "", "", "", ""],  # row 0
    ["", "", "", "", "", "", "", "", "", ""],  # row 1
    ["", "", "", "", "", "", "", "", "", ""],  # row 2
    ["", "", "", self.handle, self.flag, self.flag, self.flag, "", "", ""],  # row 3
    ["", "", "", self.handle, self.flag, self.flag, self.flag, "", "", ""],  # row 4
    ["", "", "", self.handle, self.flag, self.flag, self.flag, "", "", ""],  # row 5
    ["", "", "", self.handle, "", "", "", "", "", ""],  # row 6
    ["", "", "", self.handle, "", "", "", "", "", ""],  # row 7
    ["", "", "", self.handle, "", "", "", "", "", ""],  # row 8
    ["", "", "", "", "", "", "", "", "", ""],  # row 9
        ]

        print(f'Switched to theme {self.theme}')
              
    def change_theme(self,*args):
        self.set_colors()
        draw()


ms = GameState() # creation of our class object




bomb_color = [
    ["", "", "", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", "", "", ""],
    ["", "", "", "black", "black", "black", "black", "", "", ""],
    ["", "", "black", "black", "black", "black", "black", "black", "", ""],
    ["", "", "black", "black", "black", "black", "black", "black", "", ""],
    ["", "", "black", "black", "black", "black", "black", "black", "", ""],
    ["", "", "black", "black", "black", "black", "black", "black", "", ""],
    ["", "", "", "black", "black", "black", "black", "", "", ""],
    ["", "", "", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", "", "", ""],
]



def choose_difficulty():
    """change the difficulty of the game when the button is pressed and restart the game"""
    # case to determine difficulty
    ms.difficulty = (ms.difficulty+1)%3 # cycle through difficulties

    if ms.difficulty==0: # beginner
        ms.height, ms.width, ms.init_bomb = 9,9,10
        #diff_name.set("Beginner")
    elif ms.difficulty==1: # intermediate
        ms.height, ms.width, ms.init_bomb = 16,16,40
        #diff_name.set("Intermediate")
    elif ms.difficulty==2: # expert
        ms.height, ms.width, ms.init_bomb = 16,30,90
        #diff_name.set("Expert")



def create(start: list):
    """The following function creates the table of the game with the current difficulty after the first dig.
    It intialises an empty grid of [A,B] with :
    A : state (0:invisible ; 1:visible)
    B : object (-1: bomb ; 0:empty and nearby clear ; 1: one bomb nearby ; 2: two bombs nearby ; etc)

    param start : coordinate of the first click
    """
    ms.bob=[[[0, ""] for j in range(ms.width)] for i in range(ms.height)]

    # start : coordinate of the first click
    x = start[0]
    y = start[1]
    ms.bob[y][x] = [1,0]
    
    # number of bombs placed
    count=0
    
    # put bombs in safe places until the max number of bombs on board
    while count < ms.init_bomb :
        cellX, cellY = randint(0, ms.width-1), randint(0, ms.height-1)
        if ((cellX < x-1 or cellX > x+1) or (cellY < y-1 or cellY > y+1)) and (ms.bob[cellY][cellX][1] != -1) :
            ms.bob[cellY][cellX][1] = -1
            count += 1
    
    nb_bomb()
    
    return ms.bob





def nb_bomb():
    """initialise number of bombs around each cell in the grid
    For each cell in the grid, if it is not a bomb, count the number of adjacent bombs
    and update the cell's value accordingly.
    """
    # for each cell in the grid
    for h in range(ms.height):
        for w in range(ms.width):
            if ms.bob[h][w][1] == -1:  # if it's not a bomb we count the nearby bombs
                continue

            #initiating variables storing the obstruction in either of those direction (0:no obstruction, 1:obstruction)
            right=0
            left=0
            up=0
            down=0
            
            if w==0:
                left=1
            elif w==ms.width-1:
                right=1
            if h==0:
                up=1
            elif h==ms.height-1:
                down=1

            # using an accumulator we will check every square nearby and store the number of bombs.
            nb_bomb=0
            
            # using a nested loop we can go trough every square within a radius of one.
            for y in range((h-1)+up,(h+1)-down +1):
                for x in range((w-1)+left,(w+1)-right +1):

                    # with -1 being a bomb
                    if ms.bob[y][x][1] == -1:
                        nb_bomb +=1
                        
            # (-1: a bomb, 0: no bomb, 1:one bomb nearby, 2:..)
            ms.bob[h][w][1]= nb_bomb

def compute_cell_size():
    """Set ms.size so the game canvas (ms.width*ms.size x ms.height*ms.size) will not exceed screen size.
    Call this when difficulty changes."""
    
    # gives the screen proportions
    screen_w = 600
    screen_h = 800

    # min and max cell size to avoid too small or too big cells
    min_size = 40
    max_size = 100

    # available area for the canva (not more than a third of the screen)
    avail_w = int(screen_w) / 2
    avail_h = int(screen_h) / 2

    # compute max cell size that fits in available area
    size_w = avail_w // ms.width
    size_h = avail_h // ms.height
    ms.size = int(max(min(size_w, size_h, max_size), min_size))
    



























##################################################
##################### Test #######################
##################################################




assert ms.difficulty == 0, "The starting difficulty is not beginner"
choose_difficulty()
assert ms.difficulty == 1, "The difficulty was not changed to 1"
print("correct difficulties")
choose_difficulty()
choose_difficulty()


create([0,0])
assert ms.bob[0][0][1] != -1, "The first cell clicked is a bomb"
print("right initialisation of first cell")

c=0
for h in range(ms.height):
    for w in range(ms.width):
        if  ms.bob[h][w][1] == -1:
            c+=1
assert c==ms.init_bomb, f"There is {c} bombs in the grid, the correct number for our current difficulty ({ms.difficulty}) was {ms.init_bomb}"
print("right number of bombs in grid")

compute_cell_size()
assert ms.size >=40 and ms.size<=140


