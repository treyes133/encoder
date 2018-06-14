import threading
import os, math, io, time
import pygame, sys
from pygame.locals import *

file_name ="tar.png"
length = 3072
fs = os.path.getsize(file_name)
count = math.ceil(fs/length)
square_count = 0
height = 750
width = math.ceil(count*math.ceil(length/3)/height)
if(width < 300):
    height = math.ceil(math.ceil(fs/3)/300)
    width = 300
height = height +1
WHITE = (255, 255, 255)
size = (width, height)
pygame.init()
flags = DOUBLEBUF
screen = pygame.display.set_mode(size, flags)
screen.set_alpha(None)
pygame.display.set_caption("Running...")
clock = pygame.time.Clock()
screen.fill(WHITE)
pygame.display.flip()
clock.tick(3000)
locks = []
finished = []
end = False
def refresh(rate):
    global end
    while not end:
        pygame.display.flip()
        time.sleep(1/rate)
def process_chunk(data, index, lock_num):
    global square_count
    global length
    color_tuple = [0]*math.ceil(len(data)/3)
    incrimenter = 0
    for i in range(0,math.floor(len(data)/3)*3,3):
        color_tuple[incrimenter] = (data[i],data[i+1],data[i+2])
        incrimenter += 1
    remaining = len(data)-(3*incrimenter)
    i = i+3
    if(remaining !=0):
        if(remaining == 1):
            color_tuple[incrimenter] = (data[i],255,255)
        else:
            color_tuple[incrimenter] = (data[i],data[i+1],255)
    start_point = index*math.floor(length/3)
    row = math.floor(start_point/width)
    column = start_point - row*width
    for color in color_tuple:
        pygame.event.get()
        pygame.draw.rect(screen, color, [column,row,1,1], 0)
        if(column+1 == width):
           row = row+1
           column = 0
        else:
           column = column+1
    global locks
    locks[lock_num] = False
    global finished
    finished[index] = True
chunk_processed = [False]*count
finished = [False]*count
current_read = False
num = 0
best = [0,0]
t_count = 75
total_squares = math.ceil(fs/3)
print("working...")
for max_threads in range(t_count,t_count+1):
    refresher = threading.Thread(target = refresh, args=(1000,))
    refresher.start()
    for t in range(max_threads):
        locks.append(False)
    time_start = time.time()
    chunk_processed = [False]*count
    current_read = False
    num = 0
    screen.fill(WHITE)
    pygame.display.flip()
    with open(file_name, 'rb') as file:
        data = True
        while not all(chunk_processed):
            if not current_read and data:
                data = file.read(length)
                current_read = True
            for t in range(0,max_threads):
                if(not locks[t]):
                    if(len(data) != 0 and current_read):
                        locks[t] = True
                        current_read = False
                        thread = threading.Thread(target = process_chunk, args=(data,num,t,))
                        thread.start()
                        chunk_processed[num] = True
                        num = num + 1
            for evt in pygame.event.get():
                if evt.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            time.sleep(0.01)
    while not any(locks) and not any(finished):
        time.sleep(0.001)
    time_end = time.time()
    time.sleep(1)
    if best == [0,0] or best[1] > time_end-time_start:
        best = [max_threads,time_end-time_start]
end = True
bin_sequence = bin(total_squares)[2:]
if(len(bin_sequence)%3 == 2):
    bin_sequence = "0"+bin_sequence
elif(len(bin_sequence)%3 == 1):
    bin_sequence = "00"+bin_sequence
counter = 0
pygame.display.flip()
for dig in range(0,int(len(bin_sequence)),3):
    color_matrix = [0,0,0]
    if(int(bin_sequence[dig]) == 1):
       color_matrix[0]=255
    if(int(bin_sequence[dig+1]) == 1):
       color_matrix[1]=255
    if(int(bin_sequence[dig+2]) == 1):
       color_matrix[2]=255
    col = (color_matrix[0],color_matrix[1],color_matrix[2])
    pygame.draw.rect(screen, col, [counter,height-1,1,1], 0)
    counter = counter+1
    pygame.display.flip()
pygame.draw.rect(screen, (100,100,100), [counter,height-1,1,1], 0)
pygame.display.flip()
print("total time :: ",best[1])
pygame.display.set_caption("Complete")
path = file_name+".png"
pygame.image.save(screen,path)
print("done")
pygame.quit()
