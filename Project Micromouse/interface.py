import pygame
import time
import numpy as np
from pygame_functions import *
import json
import pickle

white = (255,255,255)
black = (0,0,0)
lightblue = (173, 216, 230)
lightgreen = (144,238,144)

y_shift = 0
x = pygame.init()

# Initializing all constant values
margin = 10 # we are defining margin to keep maze a bit away from edge

grid_size = 16
cell_size = 35
dashboardsize = 300

border_size = 6

display_width = 641+cell_size+border_size+dashboardsize
display_height = 641+cell_size+border_size


win = pygame.display.set_mode((display_width,display_height))
#screenSize(display_width,display_height)
# screen = pygame.display.set_mode((display_width,display_height))
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
    def __init__(self,pos, x_cor,y_cor,state,color = lightgreen):
        global border_size
        global cell_size
        self.pos = pos
        self.x_cor = x_cor
        self.y_cor = y_cor
        self.state = state
        self.color = color
        if self.state == "H":
            self.width = cell_size+(border_size)*2
            self.height = border_size
            self.x_lower_bound = self.x_cor + border_size
            self.x_upper_bound = self.x_cor +border_size+ cell_size
            self.y_lower_bound = self.y_cor
            self.y_upper_bound = self.y_cor + border_size
        elif self.state == "V":
            self.width = border_size
            self.height = cell_size+(border_size*2)
            self.x_lower_bound = self.x_cor
            self.x_upper_bound = self.x_cor + border_size
            self.y_lower_bound = self.y_cor + border_size
            self.y_upper_bound = self.y_cor + border_size + cell_size

##
# Making user defined pygame_functions

def draw_edge(position, type):
    #global fhand
    mousedown = True
    pos = position
    old_pos = position
    postoggle = True
    buttontype = type
    while mousedown:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # if event.type == pygame.ACTIVEEVENT:
            #     if event.gain == 0 :
            #         postoggle = False
            #         pos = -1
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    buttontype = 1
                    mousedown = True
                    postoggle = True
                    pos = event.pos
                if event.button == 3:
                    buttontype = 3
                    mousedown = True
                    postoggle = True
                    pos = event.pos
            if postoggle:
                if event.type == pygame.MOUSEMOTION:
                    pos = event.pos
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mousedown = False
                    postoggle = False
                    break
                if event.button == 3:
                    mousedown = False
                    postoggle = False
                    break
        #print(pos)
        #if pos != old_pos:
            # We are getting required position here
        if buttontype == 1:
            x_pos = pos[0]
            y_pos = pos[1]
            for iids in iidlist:
                specedge = edges[iids]
                for ed in specedge:
                    if x_pos <= ed.x_upper_bound and x_pos >= ed.x_lower_bound and y_pos >= ed.y_lower_bound and y_pos <= ed.y_upper_bound:
                        #print(pos)
                        #print(iid)
                        #fhand.write(str(iids)+"\n")
                        ed.color = black
                        pygame.draw.rect(win,ed.color,[ed.x_cor,ed.y_cor,ed.width,ed.height])
                        pygame.display.update()
        elif buttontype == 3:
            x_pos = pos[0]
            y_pos = pos[1]
            for iids in iidlist:
                specedge = edges[iids]
                for ed in specedge:
                    if x_pos <= ed.x_upper_bound and x_pos >= ed.x_lower_bound and y_pos >= ed.y_lower_bound and y_pos <= ed.y_upper_bound:
                        #print(pos)
                        #print(iid)
                        #fhand.write(str(iids)+"\n")
                        ed.color = lightgreen
                        pygame.draw.rect(win,ed.color,[ed.x_cor,ed.y_cor,ed.width,ed.height])
                        pygame.display.update()





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
iidlist = []
#fhand = open("log.txt", 'w')

cursory = margin
for row in range(grid_size):
    cursorx = margin
    cells.append([])
    for column in range(grid_size):
        iid = str(row)+"-"+str(column)
        cells[row].append(cell(iid, cursorx+border_size,cursory+border_size))
        #print(cells[row][column].color,cells[row][column].x_cor ,cells[row][column].y_cor ,cells[row][column].width,cells[row][column].height )
        pygame.draw.rect(win ,cells[row][column].color ,[cells[row][column].x_cor , cells[row][column].y_cor , cells[row][column].width , cells[row][column].height])

        edges[iid] = []
        iidlist.append(iid)
        edges[iid].append(edge("up",cursorx, cursory,"H")) #upper edge
        edges[iid].append(edge("right",cursorx+cell_size+border_size,cursory,"V")) # right edge
        edges[iid].append(edge("down",cursorx,cursory+border_size+cell_size,"H")) # bottom edge
        edges[iid].append(edge("left",cursorx,cursory,"V")) # left edge
        for l in range(4):
            #fhand.write(str(edges[iid][l].x_cor)+" "+str(edges[iid][l].y_cor)+" "+str(edges[iid][l].width)+" "+str(edges[iid][l].height))
            #fhand.write("\n")
            #print(edges[iid][l].color,edges[iid][l].x_cor,edges[iid][l].y_cor,edges[iid][l].width,edges[iid][l].height)
            pygame.draw.rect(win,edges[iid][l].color,[edges[iid][l].x_cor,edges[iid][l].y_cor,edges[iid][l].width,edges[iid][l].height])
        cursorx += cell_size+border_size
    cursory += cell_size + border_size
#print(iidlist)
#print(edges)
pygame.display.update()

##
#
# for t in range(4):
#     print(edges["111"][t].x_lower_bound,edges["111"][t].x_upper_bound,edges["111"][t].y_lower_bound,edges["111"][t].y_upper_bound )
# print("---")
# for t in range(4):
#     print(edges["110"][t].x_lower_bound,edges["110"][t].x_upper_bound,edges["110"][t].y_lower_bound,edges["110"][t].y_upper_bound )



# Drawing edges from default.pickle
drawdefault = True
try:
    defaulthandle = open("mapfile/default.pickle" , "rb")
    #print("reading default")
except:
    print("Default pickle file not found.")
    drawdefault = False

if drawdefault:
    #print("Drawing Default")
    default_data = pickle.load(defaulthandle)
    iidlist =  default_data[0]
    cells = default_data[1]
    edges = default_data[2]
    for defaultids in default_data[0]:
        default_edge_info = default_data[2][defaultids]
        for each_default_edge in default_edge_info:
            if each_default_edge.color == black:
                #print("punch")
                pygame.draw.rect(win,each_default_edge.color,[each_default_edge.x_cor,each_default_edge.y_cor,each_default_edge.width,each_default_edge.height])
                pygame.display.update()

    defaulthandle.close()

##
# wordbox = makeTextBox(display_width - dashboardsize, display_height/2,dashboardsize)
# showTextBox(wordbox)
# entry = textBoxInput(wordbox)


# Simulation Loop

while not gameExit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                gameExit = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                draw_edge (event.pos,1)
            if event.button == 3:
                draw_edge (event.pos,3)
    # wordbox = makeTextBox(display_width - dashboardsize, display_height/2,dashboardsize)
    # showTextBox(wordbox)
    # entry = textBoxInput(wordbox)





    pygame.display.update()
# pickle_data = []
# pickle_data.append(iidlist)
# pickle_data.append(cells)
# pickle_data.append(edges)
#
# fhand = open("default.pickle" , "wb")
# pickle.dump(pickle_data,fhand)
# fhand.close()

# fhand = open("default2.pickle" , "rb")
# pickle_data = pickle.load(fhand)
# print(pickle_data[0][11][11].id)
pygame.quit()
quit()
