from tkinter import *
from random import randint
from time import time



class GameState: # we use a class to make cleaner variable management
    def __init__(self, width=9, height=9, init_bomb=10, size=200, theme=randint(0,1), difficulty=0):
        self.width = width
        self.height = height
        self.init_bomb = init_bomb
        self.bomb = init_bomb
        self.size = size
        self.theme = theme
        self.difficulty = difficulty
        self.start = time()
        self.end = 0
        self.time = 0
        
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

    def game_time(self, laps):
        """Return the elapsed time since the start of the game in seconds."""
        self.time = int(self.end - self.start - laps)

        if self.time < 60:
            return f"{self.time} sec"
        else:
            return f"{self.time//60} min {self.time%60} sec"


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


def compute_cell_size():
    """Set ms.size so the game canvas will not exceed screen size.
    Call this when difficulty changes."""
    
    # screen proportions
    w_screen = fen.winfo_screenwidth()
    h_screen = fen.winfo_screenheight()

    # avoid too small or too big cells
    min_size = 40
    max_size = 100

    # The canva should not be more than a quarter of the sreen if possible
    w = int(w_screen) / 2
    h = int(h_screen) / 2

    # compute max cell size that fits in available area
    w = w // ms.width
    h = h // ms.height
    ms.size = int(max(min(w, h, max_size), min_size))
   


def choose_difficulty():
    """change the difficulty of the game when the button is pressed and restart the game"""
    # case to determine difficulty
    ms.difficulty = (ms.difficulty+1)%3 # cycle through difficulties

    if ms.difficulty==0: # beginner
        ms.height, ms.width, ms.init_bomb = 9,9,10
        diff_name.set("Beginner")
    elif ms.difficulty==1: # intermediate
        ms.height, ms.width, ms.init_bomb = 16,16,40
        diff_name.set("Intermediate")
    elif ms.difficulty==2: # expert
        ms.height, ms.width, ms.init_bomb = 16,30,90
        diff_name.set("Expert")

    print(f'{diff_name =}')
    print(f'{ms.height=}')
    print(f'{ms.width=}')
    print(f'{ms.init_bomb=}')

    compute_cell_size()
    print(f'{ms.size=}')
    restart()



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





def nb_bomb():
    """initialise number of bombs around each cell in the grid.
    For each cell in the grid, if not a bomb, count the number of adjacent bombs,
    update the cell's value accordingly.
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

    for row in ms.bob:
        for cell in row:
            print(cell, end=" ")
        print()


def draw_table(design, start_x, start_y):
    """draw_table draws a 10x10 design at the given start_x and start_y position on the canvas
    param design : 10x10 list of colors
    param start_x : x coordinate of the top-left corner
    param start_y : y coordinate of the top-left corner
    """
    pixel_size = ms.size / 10 # we can change the size and the drawing will adapt
    for r in range(10): # draw a the wished design
        for c in range(10):
            color = design[r][c]
            if color != "":
                x1 = start_x + c * pixel_size
                y1 = start_y + r * pixel_size
                x2 = x1 + pixel_size
                y2 = y1 + pixel_size
                can.create_rectangle(x1, y1, x2, y2, fill=color, outline="", tags="cell")



def color_nber(n):
    """Association of a color with a number n.

    param n : number between 1 and 8
    return : color in hex format
    """
    colors = {
        1: "#231CA8",
        2: "#688416",
        3: '#BD4242',
        4: '#372772',
        5: 'darkred',
        6: 'darkred',
        7: '#5D576B',
        8: 'black'
    }
    return colors.get(n, '')  # Default to empty string if n not in 1-8


def put_flag(event):
    """put_flag() is called when the user right-clicks, it determine the cell clicked.
    It draws a flag on the cell if the cell is hidden, or removes the flag if it is already dug.

    param event : mouse event, right click"""

    # determine the cell clicked
    (cellX, cellY) = event.x // ms.size, event.y // ms.size
    start_x, start_y = cellX * ms.size, cellY * ms.size

    # do nothing if the cell is already dug
    if ms.bob[cellY][cellX][0]==1:
        return
    
    # place or remove flag
    if ms.bob[cellY][cellX][0]==0:
        ms.bob[cellY][cellX][0]=-1 # -1 stands for cell with flag
        ms.bomb-=1
        bomb_var.set(ms.bomb)
        can.create_rectangle(start_x, start_y, start_x + ms.size, start_y + ms.size, fill=ms.hidden, tags="cell")
        draw_table(ms.flag_colors, start_x, start_y)
        
        if ms.bomb==0:
            verif_win()
        
    elif ms.bob[cellY][cellX][0]==-1:
        can.create_rectangle(start_x, start_y, start_x + ms.size, start_y + ms.size, fill=ms.hidden, activefill=ms.active, tags="cell")
        ms.bob[cellY][cellX][0]=0 # 0 stands for hided cell
        ms.bomb+=1
        bomb_var.set(ms.bomb)
    can.tag_raise("grid")


def adjacent_zero(cellY, cellX):
    """Adjacent_zero digs all adjacent cells if they are hidden.
    It continues to dig adjacent cells until all cells with zero inside neighbouring the first cell are shown.
    
    A stack is used to keep track of cells that might need their surroundings to be dug.

    param cellX : x coordinate of the first cell.
    param cellY : y coordinate of the first cell.
    """
    stack = [[cellX, cellY]]  # Initialize stack with the starting cell

    while len(stack) > 0:

        # initiating variables storing the obstruction in either of those direction (0:no obstruction, 1:obstruction)
        right=0
        left=0
        up=0
        down=0
        
        cell = stack.pop()  # Get the last cell from the stack
        w = cell[0]
        h = cell[1]
        
        if w==0:
            left=1
        elif w==ms.width-1:
            right=1
        if h==0:
            up=1
        elif h==ms.height-1:
            down=1
        
        # using a nested loop we can go trough every square within a radius of one (that are in index range) to verify if there is a cell with nothing inside near
        for h_cell in range((h-1)+up,(h+1)-down + 1):
            for w_cell in range((w-1)+left,(w+1)-right + 1):

                # if the cell is hidden, dig it
                if ms.bob[h_cell][w_cell][0]==0:
                    dig(w_cell, h_cell)

                    # if the cell dug has 0 bomb nearby, add it to the stack to check its neighbors later
                    if ms.bob[h_cell][w_cell][1]==0:
                        stack.append((w_cell, h_cell))




def dig(cellX, cellY):
    """The function dig reveals the content of the cell at (cellX, cellY) position on the canvas.

    param cellX : x coordinate of the cell
    param cellY : y coordinate of the cell
    """
    can.create_rectangle(cellX* ms.size, cellY* ms.size, (cellX+1)* ms.size, (cellY+1)* ms.size, fill=ms.fill, tags="cell")
    can.create_text(((cellX+0.5)* ms.size, (cellY+0.5)* ms.size), text=str(ms.bob[cellY][cellX][1]), font=('Arial', ms.size//2 - 5, 'bold'), fill=color_nber(ms.bob[cellY][cellX][1]), tags="cell")
    ms.bob[cellY][cellX][0]=1 # 1 stands for dug cell
    can.tag_raise("grid")



def first_dig(event):
    """first_dig is the function called when it's the first dig of the game. 
    It ensure that the first cell dug cell is not a bomb as well as the adjacent cells.
    It also initialise the bomb map and bind the keys to the verif_dig and put_flag functions.

    param event : mouse event, left click
    """
    cellX, cellY = event.x // ms.size, event.y // ms.size
    ms.bomb=ms.init_bomb
    bomb_var.set(ms.bomb)
    print("first dig")
    can.unbind("<Button-1>")
    can.bind("<Button-1>", verif_dig)
    can.bind("<Button-3>", put_flag)
    can.bind("<Button-2>", cheat) # debug key to change theme : scroll wheel click
    can.bind("<ButtonRelease-2>", draw)
    create([cellX, cellY])
    dig(cellX, cellY)
    adjacent_zero(cellY, cellX)
    ms.start = time()

    nb_bomb = 0 # debug of the number of bombs placed
    for h in range(ms.height):
        for w in range(ms.width):
            if ms.bob[h][w][1]==-1:
                nb_bomb+=1
    assert nb_bomb == ms.init_bomb, f'Wrong number of bombs : {nb_bomb}'
    


def verif_dig(event):
    """verif_dig is bound after the first dig.
    It reveals the number or bomb behind and make the user either lose or dig adjacent cells if there is no bomb nearby.

    param event : mouse event
    return : calls lose() if bomb is dug
    return : calls dig() and adjacent_zero() if no bomb is nearby
    return : calls adjacent_zero() if dug cell has 0 bomb nearby"""

    cellX, cellY = event.x // ms.size, event.y // ms.size

    if ms.bob[cellY][cellX][0]!=0: # do nothing if already dug or flagged
        return
    
    elif ms.bob[cellY][cellX][0]==0 : # try digging if its a hidden cell
        
        if ms.bob[cellY][cellX][1]==-1 : # cell contain a bomb so we lose
            draw_table(bomb_color, cellX * ms.size, cellY * ms.size)
            return lose()
        
        dig(cellX, cellY)

        if ms.bob[cellY][cellX][1]==0 : # dig all adjacent cells
            adjacent_zero(cellY, cellX)
            
    can.tag_raise("grid")


def timer_restart():
    can.after(3000, restart)


def verif_win():
    """verif_win checks if all bombs have been flagged.
    
    return : calls win() if all bombs are flagged
    """
    c=ms.init_bomb
    for h in range(ms.height):
        for w in range(ms.width):
            if ms.bob[h][w]==[-1, -1]:
                c-=1
    if ms.bomb==0 and c==0:
        return win()


def win():
    """animation on winning"""
    can.unbind("<Button-1>") # unbind all keys to avoid further interaction
    can.unbind("<Button-3>")
    can.delete("all")
    ms.end = time()
    can.create_text(ms.width/2 * ms.size, ms.height/2 * ms.size, text=f"You Win :)\nTime : {ms.game_time(0)}", font=('Arial', ms.size // (3-ms.difficulty) +2, 'bold'), fill=ms.textcolor, tags="endtext") # print win text
    timer_restart()


def lose(frame=1):
    """animation on losing"""
    if frame < 12:
        ms.change_theme() # alternate theme to create flashing effect
        can.delete("bomb") # let the user see where the bombs were
        fen.after(240 - frame*16, lambda : lose(frame + 1)) # call recursively after a delay
    else: 
        can.unbind("<Button-1>") # unbind all keys to avoid further interaction
        can.unbind("<Button-3>")
        can.unbind("<Button-2>")
        can.unbind("<ButtonRelease-2>")
        can.delete("all")
        ms.end = time()
        if ms.bomb < ms.init_bomb // 3 :
            can.create_text(ms.width/2 * ms.size, ms.height/2 * ms.size, text=f"Oh no, close\n But you might want to win at least once. \nAm I right ?\nTime : {ms.game_time(1.6)}", font=('Arial', ms.size // (3-ms.difficulty), 'bold'), fill=ms.textcolor, tags="endtext", justify="center") # print lose text
        else:
            can.create_text(ms.width/2 * ms.size, ms.height/2 * ms.size, text=f"You are quite bad try again\nTime : {ms.game_time(1.6)}", font=('Arial', ms.size // (3-ms.difficulty) +2, 'bold'), fill=ms.textcolor, tags="endtext", justify="center") # print lose text
        timer_restart()

def content():
    """draw the content of the board according to bob array with [(flagged or hidden or dug), number of bombs around]"""
    for h in range(ms.height):
        for w in range(ms.width):

            if ms.bob[h][w][0]==-1: # flagged cell
                draw_table(ms.flag_colors, w * ms.size, h * ms.size)

            elif ms.bob[h][w][0]==0: # hidden cell

                if ms.bob[h][w][1]==-1: # bomb hidden cell
                    draw_table(bomb_color, w * ms.size, h * ms.size)
                    can.create_rectangle(w * ms.size, h * ms.size, (w+1) * ms.size, (h+1) * ms.size, fill=ms.hidden, activefill=ms.active, tags="bomb")

                else: # normal hidden cell
                    can.create_rectangle(w * ms.size, h * ms.size, (w+1) * ms.size, (h+1) * ms.size, fill=ms.hidden, activefill=ms.active, tags="cell")

            else: # dug cell (=1)
                can.create_rectangle(w * ms.size, h * ms.size, (w+1) * ms.size, (h+1) * ms.size, fill=ms.fill, tags="cell")
                can.create_text(((w+0.5) * ms.size, (h+0.5) * ms.size), text=str(ms.bob[h][w][1]), font=('Arial', ms.size//2 - 5, 'bold'), fill=color_nber(ms.bob[h][w][1]), tags="number")
    can.tag_raise("grid")


def lines():
    """draw the grid lines on the canvas depending on ms.size and ms.width/ms.height"""
    
    # go through each line position and draw the lines
    for w in range(ms.width + 1): # vertical
        x = w * ms.size
        can.create_line(x, 0, x, ms.height * ms.size, fill=ms.border, width=ms.size//5, tags=("grid",))


    for h in range(ms.height + 1): # horizontal
        y = h * ms.size
        can.create_line(0, y, ms.width * ms.size, y, fill=ms.border, width=ms.size//5, tags=("grid",))


def draw(*event):
    """draw the entire board including lines and content of the cells"""
    can.delete("all")
    content()
    lines()
        
def cheat(*event):
    """cheat function to reveal the bomb map for debug purposes only"""
    can.delete("bomb")
    print("cheat activated")





fen=Tk()
fen.title("Demineur")

compute_cell_size()

# Create main container frame to hold sidebar and canvas side-by-side
main_frame = Frame(fen)
main_frame.pack(fill="both", expand=True)

# Sidebar (left panel)
sidebar = Frame(main_frame, bg="#181F1C", width=150)
sidebar.pack(side="left", fill="y", padx=5, pady=5)
sidebar.pack_propagate(False)  # keep fixed width

# Bombs counter label
bombs_label = Label(sidebar, text="Bombs Left:", bg="#181F1C", fg="white", font=("Arial", 11))
bombs_label.pack(pady=5)

bomb_var = IntVar(value=ms.bomb) # Dynamic variable to track bomb count
bomb_count = Label(sidebar, textvariable=bomb_var, bg="#181F1C", fg="white", font=("Arial", 20, "bold"))
bomb_count.pack(pady=5)



def restart():
    """restart is called when the restart button is pressed.
    """
    # print(f"{ms.init_bomb=}") # debug

    global can # we need to call the global canvas so we use global

    # destroy the canvas object to recreate a new one with the right size
    can.destroy()
    can = Canvas(main_frame, width=ms.width * ms.size, height=ms.height * ms.size, bg=ms.fill, highlightthickness=0)
    can.pack(side="left", fill="both", expand=True)
    can.unbind("<Button-3>")
    can.bind("<Button-1>", first_dig) # rebinding the keys to restart the binding of first dig
    can.delete("all")
    bomb_var.set(0)
    ms.bob = [[[0, 0] for j in range(ms.width)] for i in range(ms.height)]
    # init of the new board and other variables
    draw()



# Restart button
restart_button = Button(sidebar, text="Restart", bg="#AC69D6", fg="white", font=("Arial", 11, "bold"), command=restart, bd=6)
restart_button.pack(pady=20, padx=8, fill="x")

# Theme button
theme_button = Button(sidebar, text="Change theme", bg="#AC69D6", fg="white", font=("Arial", 11, "bold"), command=ms.change_theme, bd=6)
theme_button.pack(pady=5, padx=8, fill="x")

# Difficulty button
difficulty_button = Button(sidebar, text="Difficulty", bg="#AC69D6", fg="white", font=("Arial", 11, "bold"), command=choose_difficulty, bd=6)
difficulty_button.pack(pady=8, padx=8, fill="x")

# Difficulty label
diff_name = StringVar(value="Beginner") # Dynamic variable to print current difficulty
diff_label = Label(sidebar, textvariable=diff_name, bg="#181F1C", fg="white", font=("Arial", 16, "bold"))
diff_label.pack()

# Tutorial label
tuto_label = Label(sidebar, text="""Left click : dig
Right click : flag""", bg="#181F1C", fg="white", font=("Arial", 12))
tuto_label.pack(pady=20)


        
# Canvas (right side, main game area)
can = Canvas(main_frame, width=ms.width * ms.size, height=ms.height * ms.size, bg=ms.fill, highlightthickness=0)
can.pack(side="left", fill="both", expand=True)

can.bind("<Button-1>", first_dig)


draw() #first start of the game

fen.mainloop()






