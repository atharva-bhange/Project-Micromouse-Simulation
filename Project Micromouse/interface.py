import pygame
from pygame import *
import time
import numpy as np
import pickle
from constants import *
from classes import *
from functions import *

pygame.init()
pygame.display.set_caption("Simulation Interface")

# Drawing boilerplate/ blank maze
win.fill(white)

#chart = ['up','right','down','left']
#state = {"up" : "H" , "down" : "H" , "left" : "V" , "right" : "V"}
cursory = margin
for row in range(grid_size):
    cursorx = margin
    cells.append([])
    for column in range(grid_size):
        iid = str(row)+"-"+str(column)
        cells[row].append(cell(iid, cursorx+border_size,cursory+border_size))
        pygame.draw.rect(win ,cells[row][column].color ,[cells[row][column].x_cor , cells[row][column].y_cor , cells[row][column].width , cells[row][column].height])

        edges[iid] = []
        iidlist.append(iid)
        edges[iid].append(edge("up",cursorx, cursory,"H")) #upper edge
        edges[iid].append(edge("right",cursorx+cell_size+border_size,cursory,"V")) # right edge
        edges[iid].append(edge("down",cursorx,cursory+border_size+cell_size,"H")) # bottom edge
        edges[iid].append(edge("left",cursorx,cursory,"V")) # left edge
        for l in range(4):
            pygame.draw.rect(win,edges[iid][l].color,[edges[iid][l].x_cor,edges[iid][l].y_cor,edges[iid][l].width,edges[iid][l].height])
        cursorx += cell_size+border_size
    cursory += cell_size + border_size
pygame.display.update()

# Drawing edges from default.pickle if map.pickle is not available
drawmap = True
try:
    maphandle = open("mapfile/map.pickle" , "rb")
except:
    drawmap = False
    drawdefault = True
    try:
        defaulthandle = open("mapfile/default.pickle" , "rb")
    except:
        print("Default pickle file not found.")
        drawdefault = False
if drawmap:
    handle = maphandle
elif drawdefault:
    handle = defaulthandle
else:
    print("No Map Available")

if drawmap or drawdefault:
    data = pickle.load(handle)
    iidlist =  data[0]
    cells = data[1]
    edges = data[2]
    for defaultids in data[0]:
        edge_info = data[2][defaultids]
        for each_edge in edge_info:
            if each_edge.color == black:
                pygame.draw.rect(win,each_edge.color,[each_edge.x_cor,each_edge.y_cor,each_edge.width,each_edge.height])
                pygame.display.update()
if drawmap:
    maphandle.close()
elif drawdefault:
    defaulthandle.close()

##
#Making an emtyp maze array  and calculating distances from goal

for i in range(grid_size):
    for j in range(grid_size):
        isValid = True
        for t in range(4):
            if i == x_mid[t] and j == y_mid[t]:
                isValid = False
                break
        if not isValid:
            continue
        # Assigning code goes here
        dis_list = []
        for l in range(4):
            virtual_x = x_mid[l]
            virtual_y = y_mid[l]
            dis = abs(virtual_x - i)+abs(virtual_y - j)
            dis_list.append(dis)
        min_dis = min(dis_list)
        printCell(str(i)+"-"+str(j) , min(dis_list) , black , update = False)
        arr[i][j] = min_dis

    if not isValid:
        continue

for t in range(4):
    i = t
    j = t
    printCell(str(x_mid[i])+"-"+str(y_mid[j]) , str(arr[x_mid[i]][y_mid[j]]) , black )

pygame.display.update()
##

# Simulation Loop
saveButton = button("saveButton" , lightgreen, green , display_width-dashboardsize, margin , dashboardsize-margin , 30 , "Save")
saveButton.updateButton()


while not gameExit:
    if get_seconds() == end_time:
        erase_notification()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if is_saved:
                gameExit = True
            else:
                notification("Changes Not Saved!" , red,red)
                is_saved = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if is_saved:
                    gameExit = True
                else:
                    notification("Changes Not Saved!" , red,red)
                    is_saved = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if saveButton.isActive:
                    pass
                    saveMap()
                else:
                    draw_edge (event.pos,1)
            if event.button == 3:
                draw_edge (event.pos,3)
        if event.type == pygame.MOUSEMOTION:
            mospos = event.pos
            mospos_x = mospos[0]
            mospos_y = mospos[1]
            if mospos_x >= saveButton.x_lower_bound and mospos_x <= saveButton.x_upper_bound and mospos_y >= saveButton.y_lower_bound and mospos_y <= saveButton.y_upper_bound:
                saveButton.hover()
                saveButton.updateButton()
            else:
                saveButton.nothover()
                saveButton.updateButton()



    pygame.display.update()
pygame.quit()
quit()
