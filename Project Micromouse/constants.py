import pygame
from pygame import *
import time
import numpy as np
import pickle

red = (255,0,0)
white = (255,255,255)
black = (0,0,0)
lightblue = (173, 216, 230)
lightgreen = (144,238,144)
green = (0,128,0)

shift = 0

x_mid = [7+shift , 7+shift , 8+shift , 8+shift]
y_mid = [7+shift , 8+shift , 7+shift , 8+shift]

isValid = True

is_saved = True

edges = dict()
cells = []
iidlist = []

y_shift = 0

margin = 10

grid_size = 16
cell_size = 35
dashboardsize = 300

border_size = 6

display_width = 641+cell_size+border_size+margin+dashboardsize
display_height = 641+cell_size+border_size

arr = np.zeros([grid_size , grid_size] , int)

notif_width = 300
notif_height = 50
notif_x_pos = display_width - notif_width-margin
notif_y_pos = display_height - margin - notif_height

robot_source = pygame.image.load("img/bot_transparent.png")

gameExit = False

win = pygame.display.set_mode((display_width,display_height))

bot_initiation = False
bot_initiation_cell_i  = None
bot_initiation_cell_j  = None

allowed_bot_cell_i = [0,0,grid_size-1,grid_size-1]
allowed_bot_cell_j = [0,grid_size-1,0,grid_size-1]
