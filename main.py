import pygame
import random
from pygame import *


# Define constants
FPS = 60
MOLE_WIDTH = 90
MOLE_HEIGHT = 81


class Debugger:
    def __init__(self, mode):
        self.mode = mode

    def log(self, message):
        if self.mode is "debug":
            print("> DEBUG: " + message)


def is_mole_hit(mouse_position, current_hole_position):
    mouse_x = mouse_position[0]
    mouse_y = mouse_position[1]
    current_hole_x = current_hole_position[0]
    current_hole_y = current_hole_position[1]
    if (mouse_x > current_hole_x) and (mouse_x < current_hole_x + MOLE_WIDTH) and (mouse_y > current_hole_y) and (mouse_y < current_hole_y + MOLE_HEIGHT):
        return True
    else:
        return False


def game():
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Whack A Mole - Game Programming - Assignment 1')
    background = pygame.image.load('images/bg.png')
    screen.blit(background, (0, 0))
    cycle_time = 0
    num = -1
    loop = True
    down = False
    interval = 0.1
    frame_num = 0
    
    for i in range(len(mole)):
        mole[i].set_colorkey((0, 0, 0))
        mole[i] = mole[i].convert_alpha()

    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
            if event.type == MOUSEBUTTONDOWN:
                if is_mole_hit(mouse.get_pos(), pos[frame_num]):
                    debugger.log("Hit the mole !")

        if num == -1:
            screen.blit(background, (0, 0))
            num = 0
            down = False
            interval = 0.5
            frame_num = random.randint(0, 8)
            
        mil = clock.tick(FPS)
        sec = mil / 1000.0
        cycle_time += sec
        if cycle_time > interval:
            pic = mole[num]
            screen.blit(background, (0, 0))
            screen.blit(pic, pos[frame_num])
            if down is False:
                num += 1
            else:
                num -= 1
            if num > 2:
                num -= 1
                down = True
                interval = 0.3
            else:
                interval = 0.1
            cycle_time = 0
        pygame.display.flip()

# Initialize the game
pygame.init()
clock = pygame.time.Clock()
delay_time = 0.2
sprite_sheet = pygame.image.load("images/mole.png")
mole = []
mole.append(sprite_sheet.subsurface(169, 0, 90, 81))
mole.append(sprite_sheet.subsurface(309, 0, 90, 81))
mole.append(sprite_sheet.subsurface(449, 0, 90, 81))
# Init debugger
debugger = Debugger("debug")

# Positions of the holes in background
pos = []
pos.append((381, 295))
pos.append((119, 366))
pos.append((179, 169))
pos.append((404, 479))
pos.append((636, 366))
pos.append((658, 232))
pos.append((464, 119))
pos.append((95, 43))
pos.append((603, 11))

# Run the main loop
game()
# Exit the game if the main loop ends
pygame.quit()
