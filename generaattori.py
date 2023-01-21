# !/usr/bin/python3
from tkinter import *

from tkinter import messagebox
import math, random,pygame

'''
def create_canvas(top, getheight, getwidth):
    #top = Tk()
    C = Canvas(top, bg = "white", height = getheight, width = getwidth)
    #coord = 10, 50, 240, 210
    C.pack()
    top.mainloop()
    return C

def _create_circle(self, x, y, r,canvaas, **kwargs,):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)

'''
'''
tkinter.Canvas.create_circle = _create_circle
'''
#canvas.create_circle(100, 120, 50, fill="blue", outline="#DDD", width=4)
#def create_circle(x, y, r, canvas): #center coordinates, radius
#    x0 = x - r
#    y0 = y - r
#    x1 = x + r
#    y1 = y + r
#    return canvas.create_oval(x0, y0, x1, y1)


def main():
        #intialize canvas
    #canvas = Tk()
    #create_canvas(canvas, width, height)
    #canvas.mainloop()
    #width of screen and sample
    width = 400
    height= 400
    # gene vars
    r = 10
    k = 30
    # generator variables
    w = r/math.sqrt(2)
    cols = math.floor(width/w)
    rows = math.floor(height/w)
    grid=[]
    
    #grid making
    for x in range(cols*rows):
        grid.append(-1)
    

    #random point in grid
    x = random.randrange(0,width-1,1)
    active = [x]
    
    #sample generating
    while len(active)>0:
        size = len(active)-1
        sample = random.randint(0,size)
        break

    #root = Tk()
    #myCanvas = Canvas(root)
    #yCanvas.pack()
    
    #create_circle(100, 100, 20, myCanvas)

    background_color = (255,255,255)
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    #pygame.display.set_caption("TUFF")
    screen.fill(background_color)
    
    times = 100
    #for x in range(times):
        #canvas.create_cirle = _create_cirle
        #create_circle(100, 100, 20, myCanvas)
    #root.mainloop()

    pygame.draw.circle(screen, (0, 0, 255), (150, 50), 15, 1)
    pygame.display.flip()

    running = True
    while running:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          running = False
          pygame.display.update()




main()
