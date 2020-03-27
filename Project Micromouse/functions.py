import pygame
from pygame import *
import time
import numpy as np
import pickle
from constants import *
from classes import *
'''
  ______                _   _
 |  ____|              | | (_)
 | |__ _   _ _ __   ___| |_ _  ___  _ __  ___
 |  __| | | | '_ \ / __| __| |/ _ \| '_ \/ __|
 | |  | |_| | | | | (__| |_| | (_) | | | \__ \
 |_|   \__,_|_| |_|\___|\__|_|\___/|_| |_|___/
'''
# Making user defined pygame_functions

def draw_edge(position, type):
    global is_saved
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
                if is_saved:
                    pygame.quit()
                    quit()
                else:
                    notification("Changes Not Saved!" , red,red)
                    is_saved = True
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
                        is_saved = False
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
                        is_saved = False

##

# Saving existing drawn mapfile

def saveMap():
    global is_saved
    mapfile = open("mapfile/map.pickle" , "wb")
    pickle_data = []
    pickle_data.append(iidlist)
    pickle_data.append(cells)
    pickle_data.append(edges)

    pickle.dump(pickle_data,mapfile)
    mapfile.close()
    notification("File Saved",black,green)
    is_saved = True
##

#Function for rounded rectangle
def RoundedRect(surface,rect,color,radius=0.4):

    """
    AAfilledRoundedRect(surface,rect,color,radius=0.4)

    surface : destination
    rect    : rectangle
    color   : rgb or rgba
    radius  : 0 <= radius <= 1
    """

    rect         = Rect(rect)
    color        = Color(*color)
    alpha        = color.a
    color.a      = 0
    pos          = rect.topleft
    rect.topleft = 0,0
    rectangle    = Surface(rect.size,SRCALPHA)

    circle       = Surface([min(rect.size)*3]*2,SRCALPHA)
    draw.ellipse(circle,(0,0,0),circle.get_rect(),0)
    circle       = transform.smoothscale(circle,[int(min(rect.size)*radius)]*2)

    radius              = rectangle.blit(circle,(0,0))
    radius.bottomright  = rect.bottomright
    rectangle.blit(circle,radius)
    radius.topright     = rect.topright
    rectangle.blit(circle,radius)
    radius.bottomleft   = rect.bottomleft
    rectangle.blit(circle,radius)

    rectangle.fill((0,0,0),rect.inflate(-radius.w,0))
    rectangle.fill((0,0,0),rect.inflate(0,-radius.h))

    rectangle.fill(color,special_flags=BLEND_RGBA_MAX)
    rectangle.fill((255,255,255,alpha),special_flags=BLEND_RGBA_MIN)

    return surface.blit(rectangle,pos)

##
# get seconds time
def get_seconds():
    return time.localtime().tm_sec
##

end_time = None
notif_state = False
# Function for notification

def notification(msg , msg_color , bg_color):
    global notif_state
    global end_time
    global win
    global notif_height
    global notif_width
    global notif_x_pos
    global notif_y_pos

    RoundedRect(win,(notif_x_pos,notif_y_pos,notif_width,notif_height),bg_color , radius = 0.4)
    RoundedRect(win,(notif_x_pos+10,notif_y_pos+10,notif_width-20,notif_height-20),white , radius = 0.2)
    notif_text_x_pos = notif_x_pos+10
    notif_text_y_pos = notif_y_pos+10
    notif_text_width = notif_width-20
    notif_text_height = notif_height-20
    notification_font = pygame.font.SysFont(None,25)
    notification_text_surface = notification_font.render(msg,True,msg_color)
    notification_text_rect = notification_text_surface.get_rect()
    win.blit(notification_text_surface,[notif_text_x_pos+(notif_text_width//2) -(notification_text_rect.width//2),notif_text_y_pos+(notif_text_height//2) -(notification_text_rect.height//2)])
    pygame.display.update()
    end_time = get_seconds() + 3

# notification erase functionality
def erase_notification():
    global white
    global end_time
    global win
    global notif_height
    global notif_width
    global notif_x_pos
    global notif_y_pos
    win.fill(white,(notif_x_pos,notif_y_pos,notif_width,notif_height))
    pygame.display.update()
##

# funcyion to change colour of cells

def changeCellcolor(cellid , color):
    global win
    global cells
    ls = cellid.split("-")
    i = int(ls[0])
    j= int(ls[1])
    cellObject = cells[i][j]
    print(type(cellObject))
    cellObject.color = color

    pygame.draw.rect(win ,cellObject.color ,[cellObject.x_cor , cellObject.y_cor , cellObject.width , cellObject.height])
    pygame.display.update()
    is_saved = False

##
#Function to print number in cell

def printCell(cellid , num , color , update = True):
    global win
    global cells
    ls = cellid.split("-")
    i = int(ls[0])
    j = int(ls[1])
    cellObject = cells[i][j]
    pygame.draw.rect(win ,cellObject.color ,[cellObject.x_cor , cellObject.y_cor , cellObject.width , cellObject.height])
    pygame.display.update()
    print_font = pygame.font.SysFont(None,25)
    print_text_surface = print_font.render(str(num) , True, color)
    print_text_rect = print_text_surface.get_rect()
    print_text_x_pos = cellObject.x_cor
    print_text_y_pos = cellObject.y_cor
    print_text_width = cellObject.width
    print_text_height = cellObject.height
    win.blit(print_text_surface,[print_text_x_pos+(print_text_width//2) -(print_text_rect.width//2),print_text_y_pos+(print_text_height//2) -(print_text_rect.height//2)])
    if update:
        pygame.display.update()
    is_saved = False

#

## Making a function for initiate bot at start location
def initiatBot(pos):
    global bot_initiation
    global bot_initiation_cell_i
    global bot_initiation_cell_j
    global cells
    global win
    global black
    global arr
    x_pos = pos[0]
    y_pos = pos[1]
    for tab in range(4):
        cell_object = cells[allowed_bot_cell_i[tab]][allowed_bot_cell_j[tab]]
        if cell_object.x_lower_bound < x_pos and x_pos < cell_object.x_upper_bound and cell_object.y_lower_bound < y_pos and y_pos < cell_object.y_upper_bound:
            if bot_initiation:
                # colour old cell to set colour
                pygame.draw.rect(win ,cells[bot_initiation_cell_i][bot_initiation_cell_j].color ,[cells[bot_initiation_cell_i][bot_initiation_cell_j].x_cor , cells[bot_initiation_cell_i][bot_initiation_cell_j].y_cor , cells[bot_initiation_cell_i][bot_initiation_cell_j].width , cells[bot_initiation_cell_i][bot_initiation_cell_j].height])
                # set the old number
                str_id = str(bot_initiation_cell_i)+"-"+str(bot_initiation_cell_j)
                printCell(str_id , arr[bot_initiation_cell_i,bot_initiation_cell_j] , black)
                # draw on the new cell
                if tab == 0 or tab == 1:
                    bot = robot(cell_object.id , robot_source ,facing = "down")
                    bot_initiation = True
                    bot_initiation_cell_i = int(cell_object.id.split('-')[0])
                    bot_initiation_cell_j = int(cell_object.id.split('-')[1])
                else:
                    bot = robot(cell_object.id , robot_source ,facing = "up")
                    bot_initiation = True
                    bot_initiation_cell_i = int(cell_object.id.split('-')[0])
                    bot_initiation_cell_j = int(cell_object.id.split('-')[1])
                pygame.display.update()
            else:
                if tab == 0 or tab == 1:
                    bot = robot(cell_object.id , robot_source ,facing = "down")
                    bot_initiation = True
                    bot_initiation_cell_i = int(cell_object.id.split('-')[0])
                    bot_initiation_cell_j = int(cell_object.id.split('-')[1])
                else:
                    bot = robot(cell_object.id , robot_source ,facing = "up")
                    bot_initiation = True
                    bot_initiation_cell_i = int(cell_object.id.split('-')[0])
                    bot_initiation_cell_j = int(cell_object.id.split('-')[1])
                pygame.display.update()
