import pygame
from pygame import *
import time
import numpy as np
import pickle
from constants import *

'''
   _____ _
  / ____| |
 | |    | | __ _ ___ ___  ___  ___
 | |    | |/ _` / __/ __|/ _ \/ __|
 | |____| | (_| \__ \__ \  __/\__ \
  \_____|_|\__,_|___/___/\___||___/


'''

class cell(object):
    def __init__(self,id,x_cor,y_cor,width = cell_size,height = cell_size ,color = lightblue , ):
        self.id = id
        self.x_cor = x_cor
        self.y_cor = y_cor
        self.width = width
        self.height = height
        self.color = color
        split_id = self.id.split("-")
        self.i = int(split_id[0])
        self.j = int(split_id[1])
        self.x_lower_bound = self.x_cor
        self.x_upper_bound = self.x_cor + cell_size
        self.y_lower_bound = self.y_cor
        self.y_upper_bound = self.y_cor + cell_size

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

class button(object):
    def __init__(self,id,inactive_color,active_color,x_pos,y_pos,width,height,value):
        self.id = id
        self.inactive_color = inactive_color
        self.active_color = active_color
        self.isActive = False
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.value = value
        if self.isActive == True:
            self.color = self.active_color
        else:
            self.color = self.inactive_color
        self.x_lower_bound = self.x_pos
        self.x_upper_bound = self.x_pos + self.width
        self.y_lower_bound = self.y_pos
        self.y_upper_bound = self.y_pos + self.height
    def hover(self):
        self.isActive = True
    def nothover(self):
        self.isActive = False
    def updateButton(self):
        global win
        if self.isActive == True:
            self.color = self.active_color
        else:
            self.color = self.inactive_color
        pygame.draw.rect(win,self.color,[self.x_pos,self.y_pos,self.width,self.height])
        button_font = pygame.font.SysFont(None,25)
        button_text_surface = button_font.render(self.value,True,black)
        botton_rect = button_text_surface.get_rect()
        win.blit(button_text_surface,[self.x_pos+(self.width//2)-(botton_rect.width//2) , self.y_pos+(self.height//2)-(botton_rect.height//2)])
        pygame.display.update()

##

# Class for robot

class robot(object):
    def __init__(self , cell_location_id ,source , facing = "up" ):
        global cells
        global cell_size
        global win
        ls = cell_location_id.split("-")
        self.i = int(ls[0])
        self.j = int(ls[1])
        self.x_cor = cells[self.i][self.j].x_cor
        self.y_cor = cells[self.i][self.j].y_cor
        self.width = cell_size
        self.height = cell_size
        self.source = source
        self.facing = facing
        if facing == 'up':
            self.display = win.blit(self.source, [self.x_cor,self.y_cor,self.width, self.height])
        else:
            old_facing = 'up'
            new_facing = self.facing
            if (old_facing == "up" and new_facing == "left") or (old_facing == "left" and new_facing == "down") or (old_facing == "down" and new_facing == "right") or (old_facing == "right" and new_facing =="up"):
                # rotate anticlockwise 90 deg
                rotate = pygame.transform.rotate(self.source , 90.0)
            elif (old_facing == "up" and new_facing == "right") or (old_facing == "right" and new_facing == "down") or (old_facing == "down" and new_facing == "left") or (old_facing == "left" and new_facing =="up"):
                # rotate clockwise 90 deg
                rotate = pygame.transform.rotate(self.source , -90.0)
            else:
                # rotate 180 deg clockwise
                rotate = pygame.transform.rotate(self.source , -180.0)
            win.blit(rotate, [self.x_cor,self.y_cor,self.width, self.height])
    def moveTocell(self,new_i , new_j):
        self.i = new_i
        self.j = new_j
        self.x_cor = cells[self.i][self.j].x_cor
        self.y_cor = cells[self.i][self.j].y_cor
        win.blit(self.source, [self.x_cor,self.y_cor,self.width, self.height])
    def changeFacingto(self,new_facing):
        old_facing = self.facing
        self.facing = new_facing
        if (old_facing == "up" and new_facing == "left") or (old_facing == "left" and new_facing == "down") or (old_facing == "down" and new_facing == "right") or (old_facing == "right" and new_facing =="up"):
            # rotate anticlockwise 90 deg
            rotate = pygame.transform.rotate(self.source , 90.0)
        elif (old_facing == "up" and new_facing == "right") or (old_facing == "right" and new_facing == "down") or (old_facing == "down" and new_facing == "left") or (old_facing == "left" and new_facing =="up"):
            # rotate clockwise 90 deg
            rotate = pygame.transform.rotate(self.source , -90.0)
        else:
            # rotate 180 deg clockwise
            rotate = pygame.transform.rotate(self.source , -180.0)
        win.blit(rotate, [self.x_cor,self.y_cor,self.width, self.height])
