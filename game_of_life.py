import pygame
import numpy as np
import sys

pygame.init()
pygame.display.set_caption('Game of Life')

box_w, box_h, box_e = 100, 100, 10
# width and height values boxwise
# also box_e is edge size

size = width, height = box_w * box_e + 1, box_h * box_e + 1
# width and height values pixelwise
screen = pygame.display.set_mode(size)
# create the program window

life_table = np.zeros((box_w, box_h), dtype=bool)
# This holds the living and dead cells (transpose of the original game screen)
neighbour_table = np.zeros((box_w, box_h), dtype=np.uint8)
# This holds the number of neighbours of boxes (also transpose of the original)

##############################################################
glider = False
if glider:
    top_left = 20, 20
    with open('glider.txt', 'r') as file:
        for index, line in enumerate(file):
            row = [int(x) for x in line.split(' ')]
            w = len(row)
            life_table[top_left[0]:top_left[0] + w,
                       top_left[1] + index] = np.array(row).T
##############################################################
# This block of code creates a "glider gun" as you start the program.
# To use this make variable glider True then top_left represent where
# will be the top left corner of the glider gun on the screen.
# When you use this first to not draw anything, you can but it may
# intersect and break it. If this is True as the program runs you'll
# see the screen empty, just press enter then it will show up.
# If you press enter again the program will restart but this time
# no glider gun, if you want it again reopen the program.

palette = {}
palette['GRAY'] = 200, 200, 200
palette['WHITE'] = 255, 255, 255
palette['BLACK'] = 0, 0, 0
palette['DARK_GRAY'] = 40, 40, 40
# palette holds the color values

while True:  # The main loop of the program
    screen.fill(palette['GRAY'])
    for row in range(box_e, height, box_e):
        pygame.draw.line(screen, palette['BLACK'], (0, row), (width, row))
    for col in range(box_e, width, box_e):
        pygame.draw.line(screen, palette['BLACK'], (col, 0), (col, height))
    # This block draws the default empty window with grids

    while True:  # The drawing loop
        exit_flag = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    exit_flag = True
            # if you press enter this loop will end and the operating loop
            # will start
            elif event.type == pygame.MOUSEBUTTONUP:
                if int(event.button) == 1:
                    x, y = pygame.mouse.get_pos()
                    box_x = x // box_e
                    box_y = y // box_e
                    life_table[box_x, box_y] = True
                    temp = pygame.Rect(
                        (box_x * box_e + 1, box_y * box_e + 1), (box_e - 1, box_e - 1))
                    pygame.draw.rect(screen, palette['DARK_GRAY'], temp)
                    del temp
                # With left click you draw the boxes and also you make
                # dead cells alive in life_table. We use the Rect
                # class only to draw a box on the screen
                elif int(event.button) == 3:
                    x, y = pygame.mouse.get_pos()
                    box_x = x // box_e
                    box_y = y // box_e
                    life_table[box_x, box_y] = False
                    temp = pygame.Rect(
                        (box_x * box_e + 1, box_y * box_e + 1), (box_e - 1, box_e - 1))
                    pygame.draw.rect(screen, palette['GRAY'], temp)
                    del temp
                # With right click as you draw boxes you can delete boxes the opposite logic
                # applies

        pygame.display.flip()  # Draws the changes

        if exit_flag:  # If enter is pressed this is true, this loop ends
            break

    while True:  # Operating loop, boxes are drawen now they will operate
        exit_flag = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    exit_flag = True
            # If enter is pressed this loop will end and the drawing loop
            # will come again.

        for box_x in range(box_w):
            for box_y in range(box_h):
                if(box_y < box_h - 1 and life_table[box_x, box_y + 1]):
                    neighbour_table[box_x, box_y] += 1
                if(box_x < box_w - 1 and box_y < box_h - 1 and life_table[box_x + 1, box_y + 1]):
                    neighbour_table[box_x, box_y] += 1
                if(box_x < box_w - 1 and life_table[box_x + 1, box_y]):
                    neighbour_table[box_x, box_y] += 1
                if(box_y > 0 and box_x < box_w - 1 and life_table[box_x + 1, box_y - 1]):
                    neighbour_table[box_x, box_y] += 1
                if(box_y > 0 and life_table[box_x, box_y - 1]):
                    neighbour_table[box_x, box_y] += 1
                if(box_x > 0 and box_y > 0 and life_table[box_x - 1, box_y - 1]):
                    neighbour_table[box_x, box_y] += 1
                if(box_x > 0 and life_table[box_x - 1, box_y]):
                    neighbour_table[box_x, box_y] += 1
                if(box_x > 0 and box_y < box_h - 1 and life_table[box_x - 1, box_y + 1]):
                    neighbour_table[box_x, box_y] += 1
        # This double loop block counts the number of neighbours for every box.
        # Some conditions are used so if for example a box is on an edge then
        # we don't want to count the neighbours behind the edge.

        for box_x in range(box_w):
            for box_y in range(box_h):
                if(neighbour_table[box_x, box_y] < 2):
                    life_table[box_x, box_y] = False
                elif(neighbour_table[box_x, box_y] == 3):
                    life_table[box_x, box_y] = True
                elif(neighbour_table[box_x, box_y] > 3):
                    life_table[box_x, box_y] = False
                neighbour_table[box_x, box_y] = 0
        # This double for block looks to the number of neighbours
        # for each box then desides if it will die or it will be born again
        # This rules are the main rules of game of life, this is where the
        # rules of cellular automation is implemented.

        screen.fill(palette['GRAY'])
        for row in range(box_e, height, box_e):
            pygame.draw.line(screen, palette['BLACK'], (0, row), (width, row))
        for col in range(box_e, width, box_e):
            pygame.draw.line(screen, palette['BLACK'], (col, 0), (col, height))
        for box_x in range(box_w):
            for box_y in range(box_h):
                if life_table[box_x][box_y]:
                    temp = pygame.Rect(
                        (box_x * box_e + 1, box_y * box_e + 1), (box_e - 1, box_e - 1))
                    pygame.draw.rect(screen, palette['DARK_GRAY'], temp)
                    del temp
        # This block of code first draws an empty screen with grids
        # then checks the alive cells from the life_table, draws the alive
        # ones.

        pygame.display.flip()  #  Draws the changes made

        # pygame.time.delay(10)
        # This delay is to see the blocks moving more clearlyi
        # you can change the delay as you wish.
        if exit_flag:
            # If enter is pressed the loop will end and
            # the program will start again
            break

    life_table[:, :] = 0  # The program will restart so we reset the life table
