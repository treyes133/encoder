import threading
import os, math, io, time
import pygame, sys
file_name ="g.jpg.png"
fs = os.path.getsize(file_name)
pygame.init()
image = pygame.image.load(file_name)
height = image.get_height()
width = image.get_width()
size = (width, height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Decoding...")
clock = pygame.time.Clock()
clock.tick(1000)
screen.blit(image,(0,0))
pygame.display.flip()
num_bytes = ""
stop_code = False
count = 0
while not stop_code:
    color = image.get_at([count,height-1])
    if(not(color[0]==100 and color[1] == 100 and color[2] == 100)):
        if(color[0] == 255):
            num_bytes = num_bytes+"1"
        else:
            num_bytes = num_bytes+"0"
        if(color[1] == 255):
            num_bytes = num_bytes+"1"
        else:
            num_bytes = num_bytes+"0"
        if(color[2] == 255):
            num_bytes = num_bytes+"1"
        else:
            num_bytes = num_bytes+"0"
        count = count + 1
    else:
        stop_code = True
num_bytes = int(num_bytes,2)
print(num_bytes)
row = 0
col = 0
print(width)
output = open("OUT"+file_name[:-4],'wb+')
for x in range(0,num_bytes*3,3):
    color = image.get_at([col,row])
    b1 = color[0]
    b2 = color[1]
    b3 = color[2] 
    output.write(bytes([b1])+bytes([b2])+bytes([b3])) 
    #print(b1," ",b2," ",b3)
    if(col + 1 >= width):
        col = 0
        row += 1
    else:
        col += 1
x = x + 3
print(x)
if(num_bytes-x >= 1):
    color = image.get_at([col,row])
    if(num_bytes-x == 2):
        b1 = color[0]
        b2 = color[1]
        output.write(bytes([b1])+bytes([b2]))
    else:
        b1 = color[0]
        output.write(bytes([b1]))
output.close()
pygame.display.set_caption("Done.")
