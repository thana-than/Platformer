import pygame as pyg
import time
pyg.init()

#window setup
window_x=600
window_y=550
screen=pyg.display.set_mode((window_x,window_y))

#place objects
block_loc = window_x/2 - 32, window_y/2 + 64
face_loc = window_x/2 - 32, window_y/2 - 256

#load objects
block = pyg.image.load("block.png")
block_rect = block.get_rect()

block_rect.x = block_loc[0]
block_rect.y = block_loc[1]

#load player
mad_face = pyg.image.load("ohgodplsno-02.png")
happy_face = pyg.image.load("ohgodplsno-01.png")
face_rect = mad_face.get_rect()
ishappy = True

face_rect.x = face_loc[0]
face_rect.y = face_loc[1]

#player physics initialization
grav = 0
jump = 0
ground = 0
velocity = [0,0] # [x,y]

shift = 0
left = 0
down = 0
up = 0
right = 0
r = 0

space = 0
space_press = 0
space_release = 0

white=255,255,255
black=0,0,0
screen.fill(white)
pyg.display.update()
gameExit=False

FPS=60
clock = pyg.time.Clock()

###RESET POSITION###

def ResetPosition():
    velocity = [0,0]
    grav = 0
    jump = 0
    ground = 0
    block_rect.x = block_loc[0]
    block_rect.y = block_loc[1]
    face_rect.x = face_loc[0]
    face_rect.y = face_loc[1]
    return;

###COLLISION CHECK FUNCTION###

def VerticalCollision(vertical_distance = -1*velocity[1]):
    #check to see if player is aligned with the x for block
    if block_rect.x > face_rect.x + 64 or block_rect.x < face_rect.x - 64:
        return False;
    
    #checks vertical collision
    if face_rect.collidepoint(face_rect.x, block_rect.top + vertical_distance):
        return True;
    else:
        return False;

###GAMELOOP###

while not gameExit:
    
###INPUTS###

    #checks for initial space press
    if space == 1 and space_press == 1:
        space_press = 0 
    #checks for initial space release
    if space == 0 and space_release == 1:
        space_release = 0

    #check for keyboard
    for event in pyg.event.get():
        #checks for spacebar
        if event.type == pyg.KEYDOWN:
            if event.key == pyg.K_SPACE:
                space_press = 1
                space = 1
        elif event.type == pyg.KEYUP:
            if event.key == pyg.K_SPACE:
                space = 0
                space_release = 1
        #checks for down arrow (used in debug)
        if event.type == pyg.KEYDOWN:
            if event.key == pyg.K_DOWN:
                down = 1
        elif event.type == pyg.KEYUP:
            if event.key == pyg.K_DOWN:
                down = 0
        #checks for up arrow (used in debug)
        if event.type == pyg.KEYDOWN:
            if event.key == pyg.K_UP:
                up = 1
        elif event.type == pyg.KEYUP:
            if event.key == pyg.K_UP:
                up = 0
        #checks for right arrow (used in debug)
        if event.type == pyg.KEYDOWN:
            if event.key == pyg.K_RIGHT:
                right = 1
        elif event.type == pyg.KEYUP:
            if event.key == pyg.K_RIGHT:
                right = 0
        #checks for left arrow (used in debug)
        if event.type == pyg.KEYDOWN:
            if event.key == pyg.K_LEFT:
                left = 1
        elif event.type == pyg.KEYUP:
            if event.key == pyg.K_LEFT:
                left = 0
        #checks for shift key (used in debug)
        if event.type == pyg.KEYDOWN:
            if event.key == pyg.K_LSHIFT or event.key == pyg.K_RSHIFT:
                shift = 1
        elif event.type == pyg.KEYUP:
            if event.key == pyg.K_LSHIFT or event.key == pyg.K_RSHIFT:
                shift = 0
        #checks for r key (used in debug)
        if event.type == pyg.KEYDOWN:
            if event.key == pyg.K_RETURN:
                r = 1
        elif event.type == pyg.KEYUP:
            if event.key == pyg.K_RETURN:
                r = 0

###DEBUG###
            
    #move block down
    if down:
        if shift:
            block_rect.y = block_rect.y + 32
        else:
            block_rect.y = block_rect.y + 8

    #move block up
    if up:
        if shift:
            block_rect.y = block_rect.y - 32
        else:
            block_rect.y = block_rect.y - 8

    #move block right
    if right:
        if shift:
            block_rect.x = block_rect.x + 32
        else:
            block_rect.x = block_rect.x + 8

    #move block left
    if left:
        if shift:
            block_rect.x = block_rect.x - 32
        else:
            block_rect.x = block_rect.x - 8

    #reset positions
    if r:
        ResetPosition()
            
    #print debug to console
    print("velocity",velocity,"gravity",grav,"\njump",jump,"Ground",ground,"Space Press", space_press)
        
###JUMP###
 
    #when the spacebar is first pressed - begin jump
    if space_press == 1 and ground == 1:
        jump = -20
        grav = 0
        ground = 0

    #if the spacebar is released before hitting the jump peak, half jump and reset grav
    #this effectively creates a parabola that realistically cuts off the jump early
    if space_release == 1 and velocity[1] < jump/2:
        jump = jump / 2
        grav = 0
    
###VERTICAL MOVEMENT###

    #grav
    #grav will never be greater than 20 in order to keep falling distance reasonable and bug free
    if grav < 20 and ground == 0:
        grav += .5

    if ground == 0:
        velocity[1] = grav + (jump + grav)
    elif velocity[1]:
        velocity[1] = 0

###COLLISION CHECKING###

    if VerticalCollision(-1 * velocity[1]):
        if ground == 0: #if it was just in the air
            jump = 0 #stop the jump
            velocity[1] = 0
            face_rect.y = block_rect.top - 64
        if VerticalCollision(1):
            face_rect.y = block_rect.top - 64
        grav = 0
        ground = 1
    elif ground == 1 and (velocity[1] or VerticalCollision(-1) == 0):
        if VerticalCollision(-20) == 0:
            ground = 0
        else:
            face_rect.y = block_rect.top - 64

###APPLYING MOVEMENT###
    #simply assigns the players position to the previous calculations
    face_rect = face_rect.move(velocity)


    #screen updating
    screen.fill(white)
    
    screen.blit(block, block_rect)
    
    if ishappy:
        screen.blit(happy_face, face_rect)
    else:
        screen.blit(mad_face, face_rect)
        
    pyg.display.flip()
    
    #continue time
    clock.tick(FPS)

    ###THAT'S ALL FOLKS