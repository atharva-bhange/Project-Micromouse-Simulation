import pygame
from pygame import *
import time
import numpy as np
#import numpy as np
#import json
import pickle

red = (255,0,0)
white = (255,255,255)
black = (0,0,0)
lightblue = (173, 216, 230)
lightgreen = (144,238,144)
green = (0,128,0)

x_mid = [7 , 7 , 8 , 8]
y_mid = [7 , 8 , 7 , 8]



isValid = True

is_saved = True

edges = dict()
cells = []
iidlist = []

y_shift = 0
x = pygame.init()

# Initializing all constant values
margin = 10 # we are defining margin to keep maze a bit away from edge

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


win = pygame.display.set_mode((display_width,display_height))
#screenSize(display_width,display_height)
# screen = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Simulation Interface")

gameExit = False

##

# Making cell class and edge class

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


##
##

'''
cells = np.zeros((grid_size,grid_size) , dtype = int)
print(cells)
'''
# Drawing boilerplate/ blank maze
win.fill(white)

#chart = ['up','right','down','left']
#state = {"up" : "H" , "down" : "H" , "left" : "V" , "right" : "V"}

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



# Drawing edges from default.pickle if map.pickle is not available
drawmap = True
try:
    maphandle = open("mapfile/map.pickle" , "rb")
except:
    drawmap = False
    drawdefault = True
    try:
        defaulthandle = open("mapfile/default.pickle" , "rb")
        #print("reading default")
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
#changeCellcolor("7-7" , lightblue)
#printCell("7-7" , 66,black)

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
