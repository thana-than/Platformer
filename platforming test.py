import pygame as pyg
import time
pyg.init()

window_x=600
window_y=550
screen=pyg.display.set_mode((window_x,window_y))

block_loc = window_x/2 - 32, window_y/2 + 32
face_loc = window_x/2 - 32, window_y/2 - 256

mad_face = pyg.image.load("ohgodplsno-02.png")
happy_face = pyg.image.load("ohgodplsno-01.png")
face_rect = mad_face.get_rect()
ishappy = True

g = 1
t = 0
push = 0
ground = 0

face_rect.x = face_loc[0]
face_rect.y = face_loc[1]

block = pyg.image.load("block.png")
block_rect = block.get_rect()

block_rect.x = block_loc[0]
block_rect.y = block_loc[1]

space = 0
space_press = 0

white=255,255,255
black=0,0,0
screen.fill(white)
pyg.display.update()
gameExit=False

FPS=60
clock = pyg.time.Clock()

while not gameExit:
    t += 1
    if space == 1 and space_press == 1:
        space_press = 0
        
    for event in pyg.event.get():
        if event.type == pyg.KEYDOWN:
            if event.key == pyg.K_SPACE:
                space_press = 1
                space = 1
        elif event.type == pyg.KEYUP:
            if event.key == pyg.K_SPACE:
                space = 0
    
    if space_press == 1:
        push = -12
        t = 0
    else:
        if push < 0:
            push = push + 1

    speed = 0, g*t+(push/t)
  
    #speed = 0, g*t
    
    if face_rect.collidepoint(face_rect.x, block_rect.y-32) == 1 and space == 0:
        ground = 1
        g = 0
        t = 0
        push = 0
    else:
        if space == 0:
            ground = 0
            g = 1
    
    face_rect = face_rect.move(speed)
    
        

    print("Speed",speed,"Gravity",g,"Time",t,"Push",push,"Space Press", space_press)

    screen.fill(white)

    screen.blit(block, block_rect)
    
    if ishappy:
        screen.blit(happy_face, face_rect)
    else:
        screen.blit(mad_face, face_rect)
        
    pyg.display.flip()
    clock.tick(FPS)
