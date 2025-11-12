from tkinter import *
from random import randint
from time import sleep

height=16
width=16
bob=[[[randint(0,0), randint(-1,6)] for w in range(width)] for h in range(height)]
init_bomb=4
bomb=init_bomb
size=50
theme_input = 1

color_board = {
    1: {
        "hiddenfill": "#99809C",
        "activefill": "#78A054", #78A054
        "fill": "#D4878D",
        "textcolor": "blue",
        "border": "#FFD9DA",
        "handle": "#4f4f4f",
        "flag": "crimson"
    },
    2: {
        "hiddenfill": "#773344",
        "activefill": "#FF9F1C",
        "fill": "#F4CAE0",
        "textcolor": "green",
        "border": "#230903",
        "handle": "#F1E9DB",
        "flag": "#7EC4CF"
    }
}
hidden, active, fill, textcolor, border, handle, flag = color_board[theme_input]["hiddenfill"], color_board[theme_input]["activefill"], color_board[theme_input]["fill"], color_board[theme_input]["textcolor"], color_board[theme_input]["border"], color_board[theme_input]["handle"], color_board[theme_input]["flag"]

def set_colors(n=theme_input): # assign the value to the colors variables that will be used in the game depending on theme chosen (1 by default)
    """assign the colors according to the theme number n"""
    global hidden, active, fill, textcolor, border, handle, flag
    hidden, active, fill, textcolor, border, handle, flag = color_board[n]["hiddenfill"], color_board[n]["activefill"], color_board[n]["fill"], color_board[n]["textcolor"], color_board[n]["border"], color_board[n]["handle"], color_board[n]["flag"]



flag_colors = [
    ["", "", "", "", "", "", "", "", "", ""],  # row 0
    ["", "", "", "", "", "", "", "", "", ""],  # row 1
    ["", "", "", "", "", "", "", "", "", ""],  # row 2
    ["", "", "", handle, flag, flag, flag, "", "", ""],  # row 3
    ["", "", "", handle, flag, flag, flag, "", "", ""],  # row 4
    ["", "", "", handle, flag, flag, flag, "", "", ""],  # row 5
    ["", "", "", handle, "", "", "", "", "", ""],  # row 6
    ["", "", "", handle, "", "", "", "", "", ""],  # row 7
    ["", "", "", handle, "", "", "", "", "", ""],  # row 8
    ["", "", "", "", "", "", "", "", "", ""],  # row 9
]

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


def draw_table(design, start_x, start_y):
    pixel_size = size / 10 # we can change the size and the drawing will adapt
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
    """Returns the color associated with the number n."""
    colors = {
        1: 'blue',
        2: 'green',
        3: 'red',
        4: 'darkblue',
        5: 'darkred',
        6: 'darkred',
        7: 'black',
        8: 'black'
    }
    return colors.get(n, '')  # Default to empty string if n not in 1-8

def put_flag(event):
    """put_flag() is called when the user right-clicks, it determine the cell clicked. It draws a flag on the cell if the cell is hidden, or removes the flag if it is already dug."""
    global bomb
    (cellX, cellY) = event.x // size, event.y // size
    start_x, start_y = cellX * size, cellY * size

    if bob[cellY][cellX][0]==1:
        return
    
    if bob[cellY][cellX][0]==0:
        bob[cellY][cellX][0]=-1 # -1 stands for cell with flag
        bomb-=1
        bomb_var.set(bomb)
        can.create_rectangle(cellX*size, cellY*size, (cellX+1)* size, (cellY+1)*size, fill=hidden, tags="cell")
        draw_table(flag_colors, start_x, start_y)
        
        if bomb==0:
            verif_win()
        
    
    elif bob[cellY][cellX][0]==-1:
        can.create_rectangle(cellX*size, cellY*size, (cellX+1)* size, (cellY+1)*size, fill=hidden, activefill=active, tags="cell")
        bob[cellY][cellX][0]=0 # 0 stands for hided cell
        bomb+=1
        bomb_var.set(bomb)
    can.tag_raise("grid")


                                                                                                                            
def dig(event):
    global bomb
    cellX, cellY = event.x // size, event.y // size
    start_x, start_y = cellX * size, cellY * size

    if bob[cellY][cellX][0]==1:
        return
    
    if bob[cellY][cellX][0]==0:
        if bob[cellY][cellX][1]==-1:
            return lose()

        can.create_rectangle(cellX*size, cellY*size, (cellX+1)* size, (cellY+1)*size, fill=fill, tags="cell")
        can.create_text(((cellX+0.5)*size, (cellY+0.5)*size), text=str(bob[cellY][cellX][1]), font=('Arial', 16, 'bold'), fill=color_nber(bob[cellY][cellX][1]), tags="cell")
        
        bob[cellY][cellX][0]=1 # 1 stands for dug cell

        if bob[cellY][cellX][1]==0: # dig all adjacent cells
            ...

    can.tag_raise("grid")
                                                                                                                                
def verif_win():
    c=init_bomb
    for h in range(height):
        for w in range(width):
            if bob[h][w]==[0, -1]:
                return
    if bomb==0:
        return win()



def win():
    can.unbind_all("<Button-1>")
    can.unbind_all("<Button-3>")
    can.delete("all")
    can.create_text(width/2*size, height/2*size, text="you win", font=('Arial', 30, 'bold'), tags="endtext")


def lose(frame=0):
    """animation on losing"""

    if frame < 15:
            set_colors(frame % 2 + 1)  # alternate colors
            draw()
            can.delete("bomb") # redraw the grid
            fen.after(250 - frame*15, lambda : lose(frame + 1)) # call recursively after a delay
    else:
        can.unbind_all("<Button-1>")
        can.unbind_all("<Button-3>")
        can.delete("all")
        can.create_text(width/2*size, height/2*size, text="you are so bad u loser", font=('Arial', 30, 'bold'), tags="endtext")



def content():
    """draw the content of the board according to bob array with [(flagged or hidden or dug), number of bombs around]"""
    for h in range(height):
        for w in range(width):
            if bob[h][w][0]==-1:
                draw_table(flag_colors, w*size, h*size)
            elif bob[h][w][0]==0:
                if bob[h][w][1]==-1:
                    draw_table(bomb_color, w*size, h*size)
                    can.create_rectangle(w*size, h*size, (w+1)* size, (h+1)*size, fill=hidden, activefill=active, tags="bomb")
                else:
                    can.create_rectangle(w*size, h*size, (w+1)* size, (h+1)*size, fill=hidden, activefill=active, tags="cell")
            else:
                can.create_text(((w+0.5)*size, (h+0.5)*size), text=str(bob[h][w][1]), font=('Arial', 16, 'bold'), fill=color_nber(bob[h][w][1]))
    can.tag_raise("grid")


def lines():
    can.delete("grid") # remove previous grid lines to avoid duplicates
    
    # go through each line position and draw the lines
    for w in range(width + 1):
        x = w * size
        can.create_line(x, 0, x, height * size, fill=border, width=8, tags=("grid",))


    for h in range(height + 1):
        y = h * size
        can.create_line(0, y, width * size, y, fill=border, width=8, tags=("grid",))


def draw():
    can.delete("cell")
    content()
    lines()
    



fen=Tk()
fen.title("Demineur")





# Create main container frame to hold sidebar and canvas side-by-side
main_frame = Frame(fen)
main_frame.pack(fill="both", expand=True)

# Sidebar (left panel)
sidebar = Frame(main_frame, bg="#181F1C", width=150)
sidebar.pack(side="left", fill="y", padx=10, pady=10)
sidebar.pack_propagate(False)  # keep fixed width

# Bombs counter
bombs_label = Label(sidebar, text="Bombs Left:", bg="#181F1C", fg="white", font=("Arial", 11))
bombs_label.pack(pady=5)

bomb_var = IntVar(value=bomb)
bomb_count = Label(sidebar, textvariable=bomb_var, bg="#181F1C", fg="white", font=("Arial", 20, "bold"))
bomb_count.pack(pady=5)


# Canvas (right side, main game area)
can = Canvas(main_frame, width=width*size, height=height*size, bg=fill, highlightthickness=0)
can.pack(side="left", fill="both", expand=True)

can.bind("<Button-1>", dig)
can.bind("<Button-3>", put_flag)
can.bind("<Return>", set_colors)

set_colors(theme_input)
draw()

def restart():
    global bob, bomb, bomb_var, theme_input
    can.bind("<Button-1>", dig) # rebinding the keys in case of win/lose
    can.bind("<Button-3>", put_flag)
    can.delete("endtext")
    theme_input = randint(1,2)
    set_colors(theme_input)
    bomb=init_bomb
    bomb_var.set(bomb)
    bob=[[[randint(0,0), randint(-1,6)] for w in range(width)] for h in range(height)] # init of the new board and other variables
    draw()


# Restart button
restart_button = Button(sidebar, text="Restart", bg="#78A054", fg="white", font=("Arial", 11, "bold"), 
                        command=restart, padx=10, bd=2)
restart_button.pack(pady=10, padx=5, fill="x")



"""for w in range(width + 1):
    x = w * size
    can.create_line(x, 0, x, height * size, fill=border, width=8, tags=("grid",))


for h in range(height + 1):
    y = h * size
    can.create_line(0, y, width * size, y, fill=border, width=8, tags=("grid",))

for h in range(height):
    for w in range(width):
        if bob[h][w][0]==0:
            can.create_rectangle(w*size, h*size, (w+1)* size, (h+1)*size, fill=hidden, activefill=active)
        else:
            can.create_text(((w+0.5)*size, (h+0.5)*size), text=str(bob[h][w][1]), font=('Arial', 16, 'bold'), fill=color_nber(bob[h][w][1]))
can.tag_raise("grid")"""
        


fen.mainloop()