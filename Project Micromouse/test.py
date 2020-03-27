import math
import numpy as np

grid_size = 16

arr = np.zeros([grid_size , grid_size] , int)

x_mid = [7 , 7 , 8 , 8]
y_mid = [7 , 8 , 7 , 8]

isValid = True

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
        arr[i][j] = min_dis

    if not isValid:
        continue
