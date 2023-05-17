""" 

An attempt at remaking the classic game Tetris using Pygame. 
Two important definitions:
    A 'block' is a single block which occupies one column/row position on the board
    A 'block-shape' is a combination of single blocks in the shape of the classic 
        Tetris-shapes, described with letters like 'I' or 'T'

"""

# Load the necessary packages

import pygame as pg
import math
import sys
import time
import random

# Open the highscore text-file which stores the achieved highscore of a game if 
# the prior highscore was broken

fin = open('tetris-highscore.txt')

for i in fin:
    highscore = int(i)

# Defining some variables that are gonna be used later in the code

width = 350     # width of the tetris board
height = 700    # height of the tetris board
white = (255,255,255) 
line_color = (0,0,0)   # defining the color (black in this case) for the lines on the board
turn = 1    # the turn keeps track of the time within the game
level = 1   # the level that you're at in the game
points = 0  # the in-game points
n_tetris = 0 # the amount of full lines you have on the board
speed = 1   # this determines how fast the blocks fall in the game
secs = 0    # the in-game time
letter_list = ['I', 'O', 'T', 'Z', 'S', 'L', 'J']*10000 # list of possible blocks
spawn_list = random.sample(letter_list, 10000) # creating a random list of blocks
n = 0   # the place in the spawn_list which determines which block will be spawned

# defining the board, with extra spaces in the first two rows to be able to 
# not only print the blocks in the game, but also the next block

board = [[None]*15, [None]*15, [None]*10, [None]*10, [None]*10, 
         [None]*10, [None]*10, [None]*10, [None]*10, [None]*10, 
         [None]*10, [None]*10, [None]*10, [None]*10, [None]*10, 
         [None]*10, [None]*10, [None]*10, [None]*10, [None]*10]
  

class blocks():
    
    """
    
    Defining a single block with its type (which shape/letter), 
    state (moving or static), rotation of the block and its color.
    
    """
    
    def __init__(self, block, state, rotation, color):
        
        self.block = block
        self.state = state
        self.rotation = rotation
        self.color = color
        
# Assigning some Pygame-specific parameters

pg.init()
fps = 30
CLOCK = pg.time.Clock()
screen = pg.display.set_mode((width + 200, height + 100), 0, 10) # extra room for scores etc.
pg.display.set_caption('Tetris')

# Loading all the images and resizing them

initiating_window = pg.image.load('Tetris_logo.webp')
red_block_img = pg.image.load('red-block.png')
yellow_block_img = pg.image.load('yellow-block.png')
purple_block_img = pg.image.load('purple-block.png')
white_block_img = pg.image.load('white-block.png')
orange_block_img = pg.image.load('orange-block.png')
green_block_img = pg.image.load('green-block.png')
blue_block_img = pg.image.load('blue-block.png')
skull_img = pg.image.load('skull.png')

red_block_img = pg.transform.scale(red_block_img, (35,35))
yellow_block_img = pg.transform.scale(yellow_block_img, (35,35))
purple_block_img = pg.transform.scale(purple_block_img, (35,35))
white_block_img = pg.transform.scale(white_block_img, (35,35))
orange_block_img = pg.transform.scale(orange_block_img, (35,35))
green_block_img = pg.transform.scale(green_block_img, (35,35))
blue_block_img = pg.transform.scale(blue_block_img, (35,35))
initiating_window = pg.transform.scale(initiating_window, (width + 200, height + 100))
skull_img = pg.transform.scale(skull_img, (400, 400))



def coordinates(col, row):
    
    "Returning the coordinates of the screen for a column/row pair"
    
    offset = 0
    
    posx = width / 10 * (col - 1) + offset
    posy = height / 20 * (row - 1) + offset
    
    return [posx, posy]


def draw(col, row, color):
    
    "Printing a block with its assigned color in a specific column and row"
    
    colors = ['red', 'yellow', 'purple', 'white', 'orange', 'green', 'blue', 'skull']
    img = [red_block_img, yellow_block_img, purple_block_img, white_block_img, orange_block_img, 
           green_block_img, blue_block_img, skull_img]
    
    screen.blit(img[colors.index(color)], coordinates(col, row)) # matching the color to
                                                                 # the right block-name   
    

def print_board():
    
    "Prints the whole board with all of its blocks, including the next-block section"
    
    global board
    
    # prints the blocks on the playing board
    
    for i in range(20):
        for j in range(10):
            
            if board[i][j] != None:
                color = board[i][j].color # take the color-variable from the blocks-class
                draw(j+1,i+1, color)
                
    # prints the blocks in the 'next-block' section
                
    for i in range(2):
        for j in range(10,15):
            
            if board[i][j] != None:
                
                color = board[i][j].color
                draw(j+1,i+1, color)
                
                
def print_screen():
    
    "Draws the lines on the board"
    
    screen.fill(white)
    
    for i in range(11):
        
        pg.draw.line(screen, line_color, (width / 10 * i, 0), (width / 10 * i , height), 1)
    
    for i in range(21):
       
       pg.draw.line(screen, line_color, (0, height / 20 * i), (width, height / 20 * i), 1)
    
    

def game_initiating_window():
    
    "Prints the Tetris-logo and the board with its lines at the start of a game"
    
    screen.blit(initiating_window, (0,0))
    pg.display.update()
    time.sleep(0.5)
    screen.fill(white)
    
    for i in range(11):
        
        pg.draw.line(screen, line_color, (width / 10 * i, 0), (width / 10 * i , height), 1)
    
    for i in range(21):
       
       pg.draw.line(screen, line_color, (0, height / 20 * i), (width, height / 20 * i), 1)
        
    spawning_check() # prints the first block-shape at the top of the screen
        

def new_block(block):
    
    """
    
    Prints a combination of moving blocks at the top of the board in a certain configuration
    which is defined by its corresponding letter, e.g. 'I' or 'T', with its corresponding
    color and rotation
    
    """
    
    global board

    if block == 'I':
        
        board[0][4] = blocks('I', 'moving',1, 'red')
        board[0][5] = blocks('I', 'moving',1, 'red')
        board[0][6] = blocks('I', 'moving',1, 'red')
        board[0][7] = blocks('I', 'moving',1, 'red')
        
    if block == 'O':
        
        board[0][5] = blocks('O', 'moving',1, 'yellow')
        board[0][6] = blocks('O', 'moving',1, 'yellow')
        board[1][5] = blocks('O', 'moving',1, 'yellow')
        board[1][6] = blocks('O', 'moving',1, 'yellow')
        
    if block == 'T':
        
        board[0][5] = blocks('T', 'moving',1, 'purple')
        board[1][4] = blocks('T', 'moving',1, 'purple')
        board[1][5] = blocks('T', 'moving',1, 'purple')
        board[1][6] = blocks('T', 'moving',1, 'purple')
        
    if block == 'Z':
        
        board[0][4] = blocks('Z', 'moving',1, 'white')
        board[0][5] = blocks('Z', 'moving',1, 'white')
        board[1][5] = blocks('Z', 'moving',1, 'white')
        board[1][6] = blocks('Z', 'moving',1, 'white')
        
    if block =='S':
        
        board[1][4] = blocks('S', 'moving',1, 'orange')
        board[1][5] = blocks('S', 'moving',1, 'orange')
        board[0][5] = blocks('S', 'moving',1, 'orange')
        board[0][6] = blocks('S', 'moving',1, 'orange')
    
    if block == 'L':
        
        board[1][4] = blocks('L', 'moving',1, 'green')
        board[1][5] = blocks('L', 'moving',1, 'green')
        board[1][6] = blocks('L', 'moving',1, 'green')
        board[0][6] = blocks('L', 'moving',1, 'green')
        
    if block == 'J':
        
        board[0][4] = blocks('J', 'moving',1, 'blue')
        board[1][4] = blocks('J', 'moving',1, 'blue')
        board[1][5] = blocks('J', 'moving',1, 'blue')
        board[1][6] = blocks('J', 'moving',1, 'blue')
        

def next_block(block):
    
    "Prints a static block-shape, like in the new_block-function, in the next-block section"
    
    global board
    
    # first emptying the next-block section
    
    for i in range(2):
        for j in range(10,15):
            
            board[i][j] = None

    if block == 'I':
        
        board[0][11] = blocks('I', 'static',1, 'red')
        board[0][12] = blocks('I', 'static',1, 'red')
        board[0][13] = blocks('I', 'static',1, 'red')
        board[0][14] = blocks('I', 'static',1, 'red')
        
    if block == 'O':
        
        board[0][12] = blocks('O', 'static',1, 'yellow')
        board[0][13] = blocks('O', 'static',1, 'yellow')
        board[1][12] = blocks('O', 'static',1, 'yellow')
        board[1][13] = blocks('O', 'static',1, 'yellow')
        
    if block == 'T':
        
        board[0][12] = blocks('T', 'statc',1, 'purple')
        board[1][11] = blocks('T', 'static',1, 'purple')
        board[1][12] = blocks('T', 'static',1, 'purple')
        board[1][13] = blocks('T', 'static',1, 'purple')
        
    if block == 'Z':
        
        board[0][11] = blocks('Z', 'static',1, 'white')
        board[0][12] = blocks('Z', 'static',1, 'white')
        board[1][12] = blocks('Z', 'static',1, 'white')
        board[1][13] = blocks('Z', 'static',1, 'white')
        
    if block =='S':
        
        board[1][11] = blocks('S', 'static',1, 'orange')
        board[1][12] = blocks('S', 'static',1, 'orange')
        board[0][12] = blocks('S', 'static',1, 'orange')
        board[0][13] = blocks('S', 'static',1, 'orange')
    
    if block == 'L':
        
        board[1][11] = blocks('L', 'static',1, 'green')
        board[1][12] = blocks('L', 'static',1, 'green')
        board[1][13] = blocks('L', 'static',1, 'green')
        board[0][13] = blocks('L', 'static',1, 'green')
        
    if block == 'J':
        
        board[0][11] = blocks('J', 'static',1, 'blue')
        board[1][11] = blocks('J', 'static',1, 'blue')
        board[1][12] = blocks('J', 'static',1, 'blue')
        board[1][13] = blocks('J', 'static',1, 'blue')

    
                            
def spawning_check():
    
    """
    Checks if the board has no moving blocks and if so, prints a new block-shape 
    at the top of the board and in the next-block section
    
    """
    
    global board, spawn_list, n
    
    for i in range(20):
        for j in range(10):
                
                # the next line checks if a space on the board is not only not empty, i.e.
                # that the space is not None, and if there is a block, it's not moving
            if board[i][j] != None and board[i][j].state == 'moving':
                    
                return
    
    # increases the position in the spawn_list for the next block-shape to come
    
    new_block(spawn_list[n])
    next_block(spawn_list[n + 1])
    
    n = n + 1
    

def check_board():
    
    """
    
    Checks if the moving block-shape has any room to move down one layer. This happens
    by checking if there are any static blocks below the block-shape or if the shape is
    at the bottom of the board. Returns True if none of this is true.
    
    """
    
    global board
    
    for i in range(20):
        for j in range(10):
            
            if board[i][j] != None and board[i][j].state == 'moving':
                
                if i == 19:     # checks if the bottom of the board is reached
                    
                    return False
                
                elif board[i+1][j] != None and board[i+1][j].state == 'static':
                        
                    return False
                                    
    return True
                    

                    
def move_left():
    
    "Moves all the moving blocks to the left if there are no static blocks next to it"
    
    global board
    
    for i in range(20):
        
        # scans the first column of the board to see if there are any moving blocks present
        # if so, the function returns
        
        if board[i][0] != None and board[i][0].state == 'moving':
            
            return
    
    for k in range(20):
        for l in range(10):
            
            # checks if there are any static blocks to the left of any of the blocks
            # on the board, if so the function returns
                
            if board[k][l] != None and board[k][l].state == 'moving':
                
                if board[k][l - 1] != None and board[k][l - 1].state == 'static':
                    
                    return
                
    for m in range(20):
        for n in range(10):
                    
            if board[m][n] != None and board[m][n].state == 'moving':
               
               # if the blocks can move to the left, the function first assigns all the
               # class-properties of each of the blocks to transfer them to the new block
               
                rot = board[m][n].rotation 
                b = board[m][n].block
                color = board[m][n].color
                board[m][n] = None
                board[m][n-1] = blocks(b, 'moving', rot, color)
                
                        
                
def move_right():
    
    "Moves all the moving blocks to the right if there are no static blocks next to it"
    
    global board
    
    for i in range(20):
        
        # scans the last column of the board to see if there are any moving blocks present
        # if so, the function returns
        
        if board[i][9] != None and board[i][9].state == 'moving':
            
            return 
        
    
    for k in reversed(range(20)):
        for l in reversed(range(10)):
            
            # checks if there are any static blocks to the right of any of the blocks
            # on the board, if so the function returns
                
            if board[k][l] != None and board[k][l].state == 'moving':
                
                if board[k][l + 1] != None and board[k][l + 1].state == 'static':
                    
                    return
                
    for k in reversed(range(20)):
        for l in reversed(range(10)):
            
               # if the blocks can move to the right, the function first assigns all the
               # class-properties of each of the blocks to transfer them to the new block
               # the reversed iterations make sure that the most right blocks are moved
               # first, to not paste any blocks on top of each other
                
             if board[k][l] != None and board[k][l].state == 'moving':   
                
                rot = board[k][l].rotation  
                b = board[k][l].block
                color = board[k][l].color
                board[k][l] = None
                board[k][l+1] = blocks(b, 'moving', rot, color)
                
                        
def bring_down():

    "Moves all the moving blocks on the board down one level"    

    global board, points
    
    
    if check_board():   # checks if there are no blocks below the moving block-shape
        
        points = points + 1     # one point is added for each block-shape that moves down
    
        for i in reversed(range(20)):
            for j in reversed(range(10)):
                
                # the reversed iterations are used to make sure first the lower blocks
                # are brought down to not have multiple blocks in one space
            
                if board[i][j] != None and board[i][j].state == 'moving':
                
                    rot = board[i][j].rotation  
                    b = board[i][j].block
                    color = board[i][j].color
                    board[i][j] = None
                    board[i+1][j] = blocks(b, 'moving', rot, color)
                    
    else:
        
        # if there are blocks below the moving block-shape, or the bottom of the board 
        # is reached, the current moving blocks are changed into static blocks
        
        for i in range(20):
            for j in range(10):
                if board[i][j] != None:
                    board[i][j].state = 'static'     
                    

"""

Because I couldn't find a general way in which the block-shapes rotate, I wrote individual
rotation function for each shape. They all work the same way, there is mostly a difference
in how many configurations each shape has, but so I only included some notes for the
first function

"""                       


def rot_I(i,j,rot):
    
    "Rotates the 'I'-block-shape"
    
    global board
    
    # the 'I'-shape only has two configurations which are stored in the 'rotation'-variable
    # the rotation of the shape determines how the shape is transformed
    
    if rot == 1:
        
        for k in range(1,4):
            
            # this iteration checks for the blocks around the moving block-shape to see
            # if the shape can rotate without overlapping existing blocks

            if i > 16:  # this block-shape can't rotate if it's too low to the bottom of
                        # the board
                
                return
            
            if board[i + k][j + 1] != None and board[i + k][j + 1].state == 'static':
                
                return
            
        for k in range(4):
            
            # the current moving blocks are moved to the new spaces on the board and the
            # old spaces are being emptied
            
            board[i + k][j + 1] = blocks('I', 'moving', 2, 'red')
        
        board[i][j] = board[i][j + 2] = board[i][j + 3] = None
        
        
    if rot == 2:
        
        for k in range(4):
            
            # this iteration checks for the blocks around the moving block-shape to see
            # if the shape can rotate without overlapping existing blocks
            
            if j < 1 or j > 7: # this block-shape can't rotate if it's too close to the 
                               # side of the board
                
                return
            
            if board[i][j-1 + k] != None and board[i + k][j].state == 'static':
                
                return
            
        for k in range(4):
            
            # the current moving blocks are moved to the new spaces on the board and the
            # old spaces are being emptied
            
            board[i][j - 1 + k] = blocks('I', 'moving', 1, 'red')
            
        board[i + 1][j] = board[i + 2][j] = board[i + 3][j] = None
        
        
def rot_T(i,j,rot):
    
    global board
    
    if rot == 1:
        
        if i > 17:
            
            return
        
        if board[i + 2][j] != None and board[i + 2][j].state == 'static':
            
            return
        
        for k in range(3):
        
            board[i + k][j] = blocks('T', 'moving', 2, 'purple')
        board[i + 1][j + 1] = blocks('T', 'moving', 2, 'purple')
        board[i + 1][j - 1] = None
        
    
    if rot == 2:
        
        if j < 1:
            
            return
        
        if board[i][j - 1] != None and board[i][j - 1].state == 'static':
            
            return
        
        if board[i][j + 1] != None and board[i][j + 1].state == 'static':
            
            return
        
        for k in range(3):
            
            board[i][j - 1 + k] = blocks('T', 'moving', 3, 'purple')
        board[i + 1][j] = blocks('T', 'moving', 3, 'purple')
        board[i + 2][j] = board[i + 1][j + 1] = None 
        
        
    if rot == 3:
        
        if i > 17:
            
            return
        
        if board[i + 2][j + 1] != None and board[i + 2][j + 1].state == 'static':
            
            return
        
        if board[i + 1][j] != None and board[i + 1][j].state == 'static':
            
            return
        
        for k in range(3):
            
            board[i + k][j + 1] = blocks('T', 'moving', 4, 'purple')
        board[i + 1][j] = blocks('T', 'moving', 4, 'purple')
        board[i][j + 2] = board[i][j] =  None 
        
    
    if rot == 4:
        
        if j > 8:
            
            return
        
        if board[i + 1][j + 1] != None and board[i + 1][j + 1].state == 'static':
            
            return
        
        for k in range(3):
            
            board[i + 1][j - 1 + k] = blocks('T', 'moving', 1, 'purple')
        board[i][j] = blocks('T', 'moving', 1, 'purple')
        board[i + 2][j] =  None 
        
        
def rot_Z(i,j,rot):
    
    global board
    
    if rot == 1:
        
        if i > 17:
            
            return
        
        if board[i + 2][j] != None and board[i + 2][j].state == 'static':
            
            return
        
        if board[i + 1][j] != None and board[i + 1][j].state == 'static':
            
            return
        
        for k in range(2):
        
            board[i + 1 + k][j] = blocks('Z', 'moving', 2, 'white')
            board[i + k][j + 1] = blocks('Z', 'moving', 2, 'white')
        
        board[i][j] = board[i + 1][j + 2] = None
        
        
    if rot == 2:
        
        if j > 8:
            
            return
        
        if board[i][j - 1] != None and board[i][j - 1].state == 'static':
            
            return
        
        if board[i + 1][j + 1] != None and board[i + 1][j + 1].state == 'static':
            
            return
        
        for k in range(2):
        
            board[i][j - 1 + k] = blocks('Z', 'moving', 1, 'white')
            board[i + 1][j + k] = blocks('Z', 'moving', 1, 'white')
        
        board[i + 1][j - 1] = board[i + 2][j - 1] = None
            
        
def rot_S(i,j,rot):
    
    global board
    
    if rot == 1:
        
        if i > 17:
            
            return
        
        if board[i + 1][j + 1] != None and board[i + 1][j + 1].state == 'static':
            
            return
        
        if board[i + 2][j + 1] != None and board[i + 2][j + 1].state == 'static':
            
            return
        
        for k in range(2):
        
            board[i + k][j] = blocks('S', 'moving', 2, 'orange')
            board[i + k + 1][j + 1] = blocks('S', 'moving', 2, 'orange')
        
        board[i][j + 1] = board[i + 1][j - 1] = None
        
        
    if rot == 2:
        
        if j < 1:
            
            return
        
        if board[i + 1][j - 1] != None and board[i + 1][j - 1].state == 'static':
            
            return
        
        if board[i][j + 1] != None and board[i][j + 1].state == 'static':
            
            return
        
        for k in range(2):
        
            board[i][j + k] = blocks('S', 'moving', 1, 'orange')
            board[i + 1][j -1 + k] = blocks('S', 'moving', 1, 'orange')
        
        board[i + 1][j + 1] = board[i + 2][j + 1] = None
        
        
def rot_L(i,j,rot):
    
    global board
    
    if rot == 1:
        
        if i > 17:
            
            return
        
        if board[i][j - 2] != None and board[i][j - 2].state == 'static':
            
            return
        
        if board[i + 2][j - 2] != None and board[i + 2][j - 2].state == 'static':
            
            return
        
        if board[i + 2][j - 1] != None and board[i + 2][j - 1].state == 'static':
            
            return
        
        for k in range(3):
        
            board[i + k][j - 2] = blocks('L', 'moving', 2, 'green')
            
        board[i + 2][j - 1] = blocks('L', 'moving', 2, 'green')
        
        board[i][j] = board[i + 1][j] = board[i + 1][j - 1] = None
        
        
    if rot == 2:
        
        if j > 7:
            
            return
        
        if board[i][j + 1] != None and board[i][j + 1].state == 'static':
            
            return
        
        if board[i][j + 2] != None and board[i][j + 2].state == 'static':
            
            return
        
        for k in range(3):
        
            board[i][j + k] = blocks('L', 'moving', 3, 'green')
            
        board[i + 1][j] = blocks('L', 'moving', 3, 'green')
        
        board[i + 2][j] = board[i + 2][j + 1] = None
        
        
    if rot == 3:
        
        if i > 17:
            
            return
        
        if board[i + 1][j + 2] != None and board[i + 1][j + 2].state == 'static':
            
            return
        
        if board[i + 2][j + 2] != None and board[i + 2][j + 2].state == 'static':
            
            return
        
        for k in range(3):
        
            board[i + k][j + 2] = blocks('L', 'moving', 4, 'green')
            
        board[i][j + 1] = blocks('L', 'moving', 4, 'green')
        
        board[i][j] = board[i + 1][j] = None
        
        
    if rot == 4:
        
        if j < 1:
            
            return
        
        if board[i + 1][j] != None and board[i + 1][j].state == 'static':
            
            return
        
        if board[i + 1][j - 1] != None and board[i + 1][j - 1].state == 'static':
            
            return
        
        for k in range(3):
        
            board[i + 1][j - 1 + k] = blocks('L', 'moving', 1, 'green')
            
        board[i][j + 1] = blocks('L', 'moving', 1, 'green')
        
        board[i][j] = board[i + 2][j + 1] = None
        
               
def rot_J(i,j,rot):
    
    global board
    
    if rot == 1:
        
        if i > 17:
            
            return
        
        if board[i][j + 1] != None and board[i][j + 1].state == 'static':
            
            return
        
        if board[i][j + 2] != None and board[i][j + 2].state == 'static':
            
            return
        
        if board[i + 2][j + 1] != None and board[i + 2][j + 1].state == 'static':
            
            return
        
        for k in range(3):
        
            board[i + k][j + 1] = blocks('J', 'moving', 2, 'blue')
            
        board[i][j + 2] = blocks('J', 'moving', 2, 'blue')
        
        board[i][j] = board[i + 1][j] = board[i + 1][j + 2] = None
        
        
    if rot == 2:
        
        if j < 1:
            
            return
        
        if board[i][j - 1] != None and board[i][j - 1].state == 'static':
            
            return
        
        if board[i + 1][j + 1] != None and board[i + 1][j + 1].state == 'static':
            
            return
        
        for k in range(3):
        
            board[i][j - 1 + k] = blocks('J', 'moving', 3, 'blue')
            
        board[i + 1][j + 1] = blocks('J', 'moving', 3, 'blue')
        
        board[i + 1][j] = board[i + 2][j] = None
        
        
    if rot == 3:
        
        if i > 17:
            
            return
        
        if board[i + 1][j + 1] != None and board[i + 1][j + 1].state == 'static':
            
            return
        
        if board[i + 2][j + 1] != None and board[i + 2][j + 1].state == 'static':
            
            return
        
        if board[i + 2][j] != None and board[i + 2][j].state == 'static':
            
            return
        
        for k in range(3):
        
            board[i + k][j + 1] = blocks('J', 'moving', 4, 'blue')
            
        board[i + 2][j] = blocks('J', 'moving', 4, 'blue')
        
        board[i][j] = board[i][j + 2] = board[i + 1][j + 2] = None
        
        
    if rot == 4:
        
        if j > 8:
            
            return
        
        if board[i][j - 1] != None and board[i][j - 1].state == 'static':
            
            return
        
        if board[i + 1][j - 1] != None and board[i + 1][j - 1].state == 'static':
            
            return
        
        if board[i + 1][j + 1] != None and board[i + 1][j + 1].state == 'static':
            
            return
        
        for k in range(3):
        
            board[i + 1][j - 1 + k] = blocks('J', 'moving', 1, 'blue')
            
        board[i][j - 1] = blocks('J', 'moving', 1, 'blue')
        
        board[i][j] = board[i + 2][j] = board[i + 2][j - 1] = None
        

def rotate():
    
    "Rotates the current moving block-shape 90 degrees"
    
    global board

    for i in range(20):
        for j in range(10):
            
            if board[i][j] != None and board[i][j].state == 'moving':
                
                rotation = board[i][j].rotation
                
                if board[i][j].block == 'I':
                    
                    rot_I(i,j,rotation)
                    
                    return
                
                if board[i][j].block == 'O':
                    
                    return
                
                if board[i][j].block == 'T':
                    
                    rot_T(i,j,rotation)
                    
                    return
                
                if board[i][j].block == 'Z':
                    
                    rot_Z(i,j,rotation)
                    
                    return
                
                if board[i][j].block == 'S':
                    
                    rot_S(i,j,rotation)
                    
                    return
                
                if board[i][j].block == 'L':
                    
                    rot_L(i, j, rotation)
                    
                    return
                
                if board[i][j].block == 'J':
                    
                    rot_J(i, j, rotation)
                    
                    return
    
def level_up():
    
    "Increases the level by 1 based on how many line clears have occured"
    
    global level, n_tetris, speed, down, secs, turn
    
    if n_tetris > 10 * level:   # each level takes more line clears to go to the next
        
        level = level + 1
        
        speed = 0.5 + level * 0.5
        
        # because the falling speed of the blocks is dependent on the in-game seconds,
        # the turns are being reset to be only 1 less than the secs. This makes sure
        # that the secs and turns are increasing in the same way again with the new speed
        
        secs = math.floor(pg.time.get_ticks()/(1000/speed)) 
        
        turn = secs - 1
    


def tetris_check():
    
    "Checks if there are any full lines on the board and if so, removes them using tetris()"
    
    global board
    
    t = []
    
    for i in range(20):
        
        n = 0
        
        for j in range(10):
                
            if board[i][j] == None:
                
                break
            
            if board[i][j] != None and board[i][j].state == 'moving':
                
                break
            
            else:
                n = n + 1
                
                if n == 10: # meaning: if a line is full of static blocks
                
                    t.append(i) # appends the list with the line number
            
    if t == []:
        
        return
    
    else:
        
        tetris(t)
                
                
def tetris(t):
    
    "Removes the full lines on the board which are given as row-numbers"
    
    global board, points, level, n_tetris
    
    # the amount of lines that are being cleared at the same time have an effect on 
    # how many points are being awarded
    
    if len(t) == 1:
        
        points = points + level * 40
        
    if len(t) == 2:
        
        points = points + level * 100
        
    if len(t) == 3:
        
        points = points + level * 300
        
    if len(t) == 4:
        
        points = points + level * 1200
        
    n_tetris = n_tetris + len(t)

    for i in t:
        
        level_up() # checks if n_tetris is big enough to go up 1 level
        
        for j in range(10):
            
            board[i][j] = None
            
        # not only the blocks from the line clear(s) are being removed, also all the static
        # blocks above it are being moved down one level. The reversed iterations are 
        # to make sure that first the lowest blocks are moved down to avoid multiple blocks
        # in one space
            
        for k in reversed(range(i)):
            for l in reversed(range(10)):
                    
                if board[k][l] != None and board[k][l].state == 'static':
                    
                    board[k + 1][l] = board[k][l]
                    board[k][l] = None
                    
                    
def death_check():
    
    "Checks if there are static blocks at the top spaces of the board, if so, returns True"

    global board
    
    for i in reversed(range(2)):
        for j in reversed(range(4)):
            
            if board[i][j + 2] != None and board[i][j + 2].state == 'static':
                
                return True
    
            return False

                   
def reset():
    
    "Resets the board and the points to start a new game at level 1"

    global board, turn, level, n_tetris, points, highscore, secs
    
    if points > highscore:
        
        fout = open('tetris-highscore.txt', 'w') 
        fout.write(str(points)) # writes the new highscore on the txt-file
        
        highscore = points
        
    time.sleep(3)   # freezes the screen for 3 seconds

    board = [[None]*15, [None]*15, [None]*10, [None]*10, [None]*10, [None]*10, 
             [None]*10, [None]*10, [None]*10, [None]*10, [None]*10, [None]*10, 
             [None]*10, [None]*10, [None]*10, [None]*10, [None]*10, [None]*10, 
             [None]*10, [None]*10]     

    level = 1
    n_tetris = 0
    points = 0
        
    turn = secs - 1 # resets the turn to be only 1 less than the in-game seconds

    game_initiating_window()         
                    
    
def game():
    
    """
    
    The main function of the game which takes care of checking for deaths, tetrises,
    and keeping track of the time. It also prints the points, highscore and level on the
    screen.
    
    """
    
    global turn, board, points, level, speed, secs
    
    if death_check():
        
        reset()    
    
    speed = 0.5 + level * 0.5
    
    # the in-game time is in miliseconds and it is here changed into integer seconds
    # the higher the speed the faster the seconds go and the faster the secs become
    # bigger than the turns, making blocks fall faster
    
    secs = math.floor(pg.time.get_ticks()/(1000/speed))
    
    tetris_check()
    spawning_check()
    
    if secs > turn:
        
        turn = turn + 1
        print_screen()
        bring_down()
        print_board()
        
    font = pg.font.Font(None, 30)
    message1 = 'Points: ' + str(points)
    message2 = 'Level ' + str(level)
    message3 = 'Highscore: ' + str(highscore)
    text1 = font.render(message1, 1 , (255,255,255))
    text2 = font.render(message2, 1 , (255,255,255))
    text3 = font.render(message3, 1 , (255,255,255))
        
    screen.fill((0,0,0), (0, 700, 600, 100))    # only fills the screen below the board
    text_rect1 = text1.get_rect(center = (width / 2, 775-50))
    text_rect2 = text2.get_rect(center = (width / 2, 825-50))
    text_rect3 = text3.get_rect(center = (width / 2, 800-50))
    screen.blit(text1, text_rect1)
    screen.blit(text2, text_rect2)
    screen.blit(text3, text_rect3)
    pg.display.update()
    
           

game_initiating_window() # starts the game by printing the screen and the first block-shape

# the down-variable is used to keep bringing the blocks down while the down-arrow is being
# pressed and is changed to False when it's not being pressed 
 
down = False

"""

The last part of the code runs the game and takes care of any actions like pressing keys
and quiting the game. It also updates the screen each time a key is being pressed

"""
     
while(True):
    
    for event in pg.event.get():
        if event.type == pg.QUIT:   # pressing the quit-button on the game-window
            pg.quit()
            sys.exit()
    
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                move_left()
            if event.key == pg.K_RIGHT:
                move_right()
            if event.key == pg.K_DOWN:
                down = True
            if event.key == pg.K_SPACE:
                rotate()
                
        if event.type == pg.KEYUP:   # if the down-arrow is being released, down = False
            if event.key == pg.K_DOWN:
                down = False
                
            print_screen()
            print_board()
            
    if down == True:  # keeps bringing down the moving block-shape
        bring_down()
    
        print_screen()
        print_board()
                
    game()  # checks for death and line clears and keeps track of the time
        
    pg.display.update()
    CLOCK.tick(fps)     # increases the seconds in the game based on the fps
    