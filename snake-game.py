import pygame
import sys
import random
from pygame.locals import *

pygame.init()
pygame.mixer.init() # initialize mixer

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TITLE = "Snake Game"

# create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(TITLE)

# game variables and constants
CELL_SIZE = 10
direction = 1 #1 is up, 2 is right, 3 is down, 4 is left
update_snake = 0
score = 0 # initialize score

snake_pos = [[int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2)]] # head of snake
snake_pos.append([int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2) + CELL_SIZE]) # body segment 
snake_pos.append([int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2) + CELL_SIZE * 2]) # body segment 
snake_pos.append([int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2) + CELL_SIZE * 3]) # body segment 

BG = (255, 200, 150)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BODY_INNER = (50, 175, 25)
BODY_OUTER = (100, 100, 200)
APPLE_COLOR = (255, 0, 0)

# define apple position
apple_pos = [random.randint(0, SCREEN_WIDTH // CELL_SIZE - 1) * CELL_SIZE,
            random.randint(0, SCREEN_HEIGHT // CELL_SIZE - 1) * CELL_SIZE]

# font for score
font = pygame.font.SysFont(None, 35)

# load and play background music
pygame.mixer.music.load('atomic-cat.ogg')

pygame.mixer.music.set_volume(0.5) # set initial volume to 50%

pygame.mixer.music.play(-1) # play the music in a loop

def draw_screen():
    screen.fill(BG)

def draw_apple():
    pygame.draw.rect(screen, APPLE_COLOR, (apple_pos[0], apple_pos[1], CELL_SIZE, CELL_SIZE))

def draw_score():
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, [10, 10])

running = True
while running:
    draw_screen()
    draw_apple()
    draw_score()

    # loop through events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction !=3: # up
                direction = 1
            elif event.key == pygame.K_RIGHT and direction != 4: # right
                direction = 2
            elif event.key == pygame.K_DOWN and direction != 1: # down
                direction = 3
            elif event.key == pygame.K_LEFT and direction != 2: # left
                direction = 4
    
    # add timer
    if update_snake > 99:
        update_snake = 0

        # move the snake 
        head_x, head_y = snake_pos[0]

        if direction == 1: # up
            head_y -= CELL_SIZE
        elif direction == 2: # right
            head_x += CELL_SIZE
        elif direction == 3: # down
            head_y += CELL_SIZE
        elif direction == 4: # left
            head_x -= CELL_SIZE

        # update the snake's position
        snake_pos.insert(0, [head_x, head_y]) # add new head
        snake_pos.pop() # remove the last segment

        # check for collision with apple
        if snake_pos[0] == apple_pos:
            apple_pos = [random.randint(0, SCREEN_WIDTH // CELL_SIZE - 1) * CELL_SIZE,
                         random.randint(0, SCREEN_HEIGHT // CELL_SIZE - 1) * CELL_SIZE]
            snake_pos.append(snake_pos[-1]) # add new segment to snake
            score += 1 # increment score if snake eats apple

        # check for collision with screen boundaries
        if head_x < 0 or head_x >= SCREEN_WIDTH or head_y < 0 or head_y >= SCREEN_HEIGHT:
            running = False # Exit the game
    # draw snake
    for i in range(len(snake_pos)):
        segment = snake_pos[i]
        if i == 0: # head
            pygame.draw.rect(screen, BODY_OUTER, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))
 
            pygame.draw.rect(screen, RED, (segment[0] + 1, segment[1] + 1, CELL_SIZE - 2, CELL_SIZE - 2))
        else: # body
            pygame.draw.rect(screen, BODY_OUTER, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))
 
            pygame.draw.rect(screen, BODY_INNER, (segment[0] + 1, segment[1] + 1, CELL_SIZE - 2, CELL_SIZE - 2))

    # update display
    pygame.display.flip()

    update_snake += 1

# exit pygame
pygame.quit()
sys.exit()
