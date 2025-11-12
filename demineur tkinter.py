from tkinter import *
from random import randint
from time import sleep

height=16
width=16
init_bomb=4
bomb=init_bomb
size=50

bob=[[[randint(0,1), randint(-1,6)] for w in range(width)] for h in range(height)]
flag_colors = [
    ["", "", "", "", "", "", "", "", "", ""],  # row 0
    ["", "", "", "", "", "", "", "", "", ""],  # row 1
    ["", "", "", "", "", "", "", "", "", ""],  # row 2
    ["", "", "", "#4f4f4f", "crimson", "crimson", "crimson", "", "", ""],  # row 3
    ["", "", "", "#4f4f4f", "crimson", "crimson", "crimson", "", "", ""],  # row 4
    ["", "", "", "#4f4f4f", "crimson", "crimson", "crimson", "", "", ""],  # row 5
    ["", "", "", "#4f4f4f", "", "", "", "", "", ""],  # row 6
    ["", "", "", "#4f4f4f", "", "", "", "", "", ""],  # row 7
    ["", "", "", "#4f4f4f", "", "", "", "", "", ""],  # row 8
    ["", "", "", "", "", "", "", "", "", ""],  # row 9
]



def draw_flag(event):
    global bomb
    (cellX, cellY) = event.x // size, event.y // size
    start_x, start_y = cellX * size, cellY * size

    if bob[cellY][cellX][0]==1:
        return
    
    if bob[cellY][cellX][0]==0:
        bob[cellY][cellX][0]=-1 # -1 stands for cell with flag
        bomb-=1
        bomb_var.set(bomb)
        pixel_size = size / 10 # we can change the size and the drawing will adapt
        for r in range(10): # draw a flag
            for c in range(10):
                color = flag_colors[r][c]
                if color != "":
                    x1 = start_x + c * pixel_size
                    y1 = start_y + r * pixel_size
                    x2 = x1 + pixel_size
                    y2 = y1 + pixel_size
                    can.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
        if bomb==0:
            verif_win()
        
    
    elif bob[cellY][cellX][0]==-1:
        can.create_rectangle(cellX*size, cellY*size, (cellX+1)* size, (cellY+1)*size, fill='lightpink', outline="crimson", width=3)
        bob[cellY][cellX][0]=0 # 0 stands for hided cell
        bomb+=1
        bomb_var.set(bomb)


                                                                                                                            
def dig(event):
    global bomb
    cellX, cellY = event.x // size, event.y // size
    start_x, start_y = cellX * size, cellY * size

    if bob[cellY][cellX][0]==1:
        return
    
    if bob[cellY][cellX][0]==0:
        if bob[cellY][cellX][1]==-1:
            return lose()

        can.create_rectangle(cellX*size, cellY*size, (cellX+1)* size, (cellY+1)*size, fill='pink')
        can.create_text(((cellX+0.5)*size, (cellY+0.5)*size), text=str(bob[cellY][cellX][1]), font=('Arial', 16, 'bold'))
                                                                                                                                
def verif_win():
    c=init_bomb
    for h in range(height):
        for w in range(width):
            if bob[h][w]==[-1,-1]:
                c-=1
    if c==0 :
        return win()



def win():
    can.delete("all")
    can.create_text(width/2*size, height/2*size, text="you win", font=('Arial', 30, 'bold'))


def lose():
    can.delete("all")
    can.create_text(width/2*size, height/2*size, text="you lose", font=('Arial', 30, 'bold'))

fen=Tk()
can=Canvas(fen, width = width*size, height = height*size, bg ='pink')
can.pack()
can.bind("<Button-1>", dig)
can.bind("<Button-2>", draw_flag)
bomb_var = IntVar(value=bomb)
Label(fen, text="Bombs:").pack(anchor="nw")
bomb_label = Label(fen, textvariable=bomb_var, font=("Arial", 14))
bomb_label.pack(anchor="nw")


for w in range(width + 1):
    x = w * size
    can.create_line(x, 0, x, height * size, fill='black')


for h in range(height + 1):
    y = h * size
    can.create_line(0, y, width * size, y, fill='black')

for h in range(height):
    for w in range(width):
        if bob[h][w][0]==0:
            can.create_rectangle(w*size, h*size, (w+1)* size, (h+1)*size, fill='lightpink', outline="crimson", width=3)
        else:
            can.create_text(((w+0.5)*size, (h+0.5)*size), text=str(bob[h][w][1]), font=('Arial', 16, 'bold'))
        


fen.mainloop()