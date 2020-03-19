import pygame
import time
import numpy as np

white = (255,255,255)
black = (0,0,0)
lightblue = (173, 216, 230)
lightgreen = (144,238,144)

x = pygame.init()

# Initializing all constant values
margin = 10 # we are defining margin to keep maze a bit away from edge

grid_size = 16
cell_size = 35

border_size = 6

display_width = 641+cell_size+border_size
display_height = 641+cell_size+border_size

win = pygame.display.set_mode((display_width,display_height))

pygame.display.set_caption("Simulation Interface")

gameExit = False

##

# Making cell class and edge class

class cell(object):
    def __init__(self,id,x_cor,y_cor,width = cell_size,height = cell_size ,color = lightblue ):
        self.id = id
        self.x_cor = x_cor
        self.y_cor = y_cor
        self.width = width
        self.height = height
        self.color = color

class edge(object):
    def __init__(self,pos, x_cor,y_cor,state,color = black):
        global border_size
        global cell_size
        self.pos = pos
        self.x_cor = x_cor
        self.y_cor = y_cor
        self.state = state
        self.color = color
        if self.state == "H":
            self.width = cell_size
            self.height = border_size
        elif self.state == "V":
            self.width = border_size
            self.height = cell_size+(border_size*2)
##
'''
cells = np.zeros((grid_size,grid_size) , dtype = int)
print(cells)
'''
# Drawing boilerplate/ blank maze
win.fill(white)
edges = dict()
#chart = ['up','right','down','left']
#state = {"up" : "H" , "down" : "H" , "left" : "V" , "right" : "V"}
cells = []

fhand = open("log.txt", 'a')

cursory = margin
for row in range(grid_size):
    cursorx = margin
    cells.append([])
    for column in range(grid_size):
        iid = str(row)+str(column)
        cells[row].append(cell(iid, cursorx+border_size,cursory+border_size))
        #print(cells[row][column].color,cells[row][column].x_cor ,cells[row][column].y_cor ,cells[row][column].width,cells[row][column].height )
        pygame.draw.rect(win ,cells[row][column].color ,[cells[row][column].x_cor , cells[row][column].y_cor , cells[row][column].width , cells[row][column].height])

        edges[iid] = []

        edges[iid].append(edge("up",cursorx+border_size, cursory,"H")) #upper edge
        edges[iid].append(edge("right",cursorx+cell_size+border_size,cursory,"V")) # right edge
        edges[iid].append(edge("down",cursorx+border_size,cursory+border_size+cell_size,"H")) # bottom edge
        edges[iid].append(edge("left",cursorx,cursory,"V")) # left edge
        for l in range(4):
            #fhand.write(str(edges[iid][l].x_cor)+" "+str(edges[iid][l].y_cor)+" "+str(edges[iid][l].width)+" "+str(edges[iid][l].height))
            #fhand.write("\n")
            #print(edges[iid][l].color,edges[iid][l].x_cor,edges[iid][l].y_cor,edges[iid][l].width,edges[iid][l].height)
            pygame.draw.rect(win,edges[iid][l].color,[edges[iid][l].x_cor,edges[iid][l].y_cor,edges[iid][l].width,edges[iid][l].height])


        cursorx += cell_size+border_size
    cursory += cell_size + border_size
pygame.display.update()
print("done")
while not gameExit:


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                gameExit = True


    #pygame.display.update()

pygame.quit()
quit()
