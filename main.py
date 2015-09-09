import pygame
import random
from pygame import *


# Define constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
MOLE_WIDTH = 90
MOLE_HEIGHT = 81
FONT_SIZE = 50
LEVEL_SCORE_GAP = 5
GAME_TITLE = "Whack A Mole - Game Programming - Assignment 1"


class GameManager:
    def __init__(self):
        self.score = 0
        self.misses = 0
        self.level = 1
        # Initialize screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self.background = pygame.image.load("images/bg.png")
        # Font object for displaying text
        self.font_obj = pygame.font.SysFont(None, FONT_SIZE)
        # Initialize the mole's sprite sheet
        sprite_sheet = pygame.image.load("images/mole.png")
        self.mole = []
        self.mole.append(sprite_sheet.subsurface(169, 0, 90, 81))
        self.mole.append(sprite_sheet.subsurface(309, 0, 90, 81))
        self.mole.append(sprite_sheet.subsurface(449, 0, 90, 81))
        self.mole.append(sprite_sheet.subsurface(575, 0, 116, 81))
        self.mole.append(sprite_sheet.subsurface(717, 0, 116, 81))
        self.mole.append(sprite_sheet.subsurface(853, 0, 116, 81))
        # Init debugger
        self.debugger = Debugger("debug")

    def get_player_level(self):
        return 1 + int(self.score / LEVEL_SCORE_GAP)

    def update(self):
        # Update the player's score
        current_score_string = "SCORE: " + str(self.score)
        score_text = self.font_obj.render(current_score_string, True, (255, 255, 255))
        score_text_pos = score_text.get_rect()
        score_text_pos.centerx = self.background.get_rect().centerx
        score_text_pos.centery = 20
        self.screen.blit(score_text, score_text_pos)
        # Update the player's misses
        current_misses_string = "MISSES: " + str(self.misses)
        misses_text = self.font_obj.render(current_misses_string, True, (255, 255, 255))
        misses_text_pos = misses_text.get_rect()
        misses_text_pos.centerx = SCREEN_WIDTH / 5 * 4
        misses_text_pos.centery = 20
        self.screen.blit(misses_text, misses_text_pos)
        # Update the player's level
        current_level_string = "LEVEL: " + str(self.level)
        level_text = self.font_obj.render(current_level_string, True, (255, 255, 255))
        level_text_pos = level_text.get_rect()
        level_text_pos.centerx = SCREEN_WIDTH / 5 * 1
        level_text_pos.centery = 20
        self.screen.blit(level_text, level_text_pos)

    def start(self):
        cycle_time = 0
        num = -1
        loop = True
        is_down = False
        interval = 0.1
        frame_num = 0
        left = 0
        # Time control variables
        clock = pygame.time.Clock()

        for i in range(len(self.mole)):
            self.mole[i].set_colorkey((0, 0, 0))
            self.mole[i] = self.mole[i].convert_alpha()

        while loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = False
                if event.type == MOUSEBUTTONDOWN:
                    if is_mole_hit(mouse.get_pos(), hole_positions[frame_num]) and num > 0 and left == 0:
                        num = 3
                        left = 14
                        is_down = False
                        interval = 0
                        self.score += 1  # Increase player's score
                        self.level = self.get_player_level()  # Calculate player's level
                        self.update()
                    else:
                        self.misses += 1
                        self.update()

            if num > 5:
                self.screen.blit(self.background, (0, 0))
                self.update()
                num = -1
                left = 0
                
            if num == -1:
                self.screen.blit(self.background, (0, 0))
                self.update()
                num = 0
                is_down = False
                interval = 0.5
                frame_num = random.randint(0, 8)

            mil = clock.tick(FPS)
            sec = mil / 1000.0
            cycle_time += sec
            if cycle_time > interval:
                pic = self.mole[num]
                self.screen.blit(self.background, (0, 0))
                self.screen.blit(pic, (hole_positions[frame_num][0] - left, hole_positions[frame_num][1]))
                self.update()
                if is_down is False:
                    num += 1
                else:
                    num -= 1
                if num == 4:
                    interval = 0.3
                elif num == 3:
                    num -= 1
                    is_down = True
                    interval = 0.8 #TODO
                else:
                    interval = 0.1
                cycle_time = 0
            pygame.display.flip()


class Debugger:
    def __init__(self, mode):
        self.mode = mode

    def log(self, message):
        if self.mode is "debug":
            print("> DEBUG: " + str(message))


def is_mole_hit(mouse_position, current_hole_position):
    mouse_x = mouse_position[0]
    mouse_y = mouse_position[1]
    current_hole_x = current_hole_position[0]
    current_hole_y = current_hole_position[1]
    if (mouse_x > current_hole_x) and (mouse_x < current_hole_x + MOLE_WIDTH) and (mouse_y > current_hole_y) and (mouse_y < current_hole_y + MOLE_HEIGHT):
        return True
    else:
        return False

###############################################################
# Initialize the game
pygame.init()

# Positions of the holes in background
hole_positions = []
hole_positions.append((381, 295))
hole_positions.append((119, 366))
hole_positions.append((179, 169))
hole_positions.append((404, 479))
hole_positions.append((636, 366))
hole_positions.append((658, 232))
hole_positions.append((464, 119))
hole_positions.append((95, 43))
hole_positions.append((603, 11))

# Run the main loop
my_game = GameManager()
my_game.start()
# Exit the game if the main loop ends
pygame.quit()
