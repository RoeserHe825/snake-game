import pygame
import sys
import random
from pygame.locals import *

pygame.init()
pygame.mixer.init()  # initialize mixer

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TITLE = "Snake Game"
CELL_SIZE = 10  
FPS = 10  # frame rate

# Colors
BG = (255, 200, 150)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BODY_INNER = (50, 175, 25)
BODY_OUTER = (100, 100, 200)
APPLE_COLOR = (255, 0, 0)

# Font for score
font = pygame.font.SysFont(None, 35)

def draw_screen(screen):
    screen.fill(BG)

def draw_apple(screen, apple_pos):
    pygame.draw.rect(screen, APPLE_COLOR, (apple_pos[0], apple_pos[1], CELL_SIZE, CELL_SIZE))

def draw_score(screen, score):
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, [10, 10])

def run_snake_game():
    # Create game window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    
    # Game variables
    direction = 1  # 1 is up, 2 is right, 3 is down, 4 is left
    score = 0  # initialize score
    running = True
    
    # Initialize snake position
    snake_pos = [[int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2)]]  # head of snake
    snake_pos.append([int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2) + CELL_SIZE])  # body segment
    snake_pos.append([int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2) + CELL_SIZE * 2])  # body segment
    snake_pos.append([int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2) + CELL_SIZE * 3])  # body segment
    
    # Define apple position
    apple_pos = [random.randint(0, (SCREEN_WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
                random.randint(0, (SCREEN_HEIGHT // CELL_SIZE) - 1) * CELL_SIZE]
    
    try:
        # Try to load and play background music
        pygame.mixer.music.load('atomic-cat.ogg')
        pygame.mixer.music.set_volume(0.5)  # set initial volume to 50%
        pygame.mixer.music.play(-1)  # play the music in a loop
    except pygame.error as e:
        # Handle the error if the background music file is not found or cannot be played
        print(f'Error loading or playing music in Snake game: {e}')
    
    # Game loop
    clock = pygame.time.Clock()
    while running:
        
        draw_screen(screen)
        draw_apple(screen, apple_pos)
        draw_score(screen, score)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != 3:  # up
                    direction = 1
                elif event.key == pygame.K_RIGHT and direction != 4:  # right
                    direction = 2
                elif event.key == pygame.K_DOWN and direction != 1:  # down
                    direction = 3
                elif event.key == pygame.K_LEFT and direction != 2:  # left
                    direction = 4  # Fixed: Added missing direction assignment
        
        # Move the snake
        head_x, head_y = snake_pos[0]
        if direction == 1:  # up
            head_y -= CELL_SIZE
        elif direction == 2:  # right
            head_x += CELL_SIZE
        elif direction == 3:  # down
            head_y += CELL_SIZE
        elif direction == 4:  # left
            head_x -= CELL_SIZE
        
        # Update the snake's position
        snake_pos.insert(0, [head_x, head_y])  # add new head
        
        # Check for collision with apple
        if snake_pos[0][0] == apple_pos[0] and snake_pos[0][1] == apple_pos[1]:
            apple_pos = [random.randint(0, (SCREEN_WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
                        random.randint(0, (SCREEN_HEIGHT // CELL_SIZE) - 1) * CELL_SIZE]
            score += 1  # add score if snake eats apple
        else:
            snake_pos.pop()  # remove the last segment if no apple eaten
        
        # Check for collision with screen boundaries
        if head_x < 0 or head_x >= SCREEN_WIDTH or head_y < 0 or head_y >= SCREEN_HEIGHT:
            running = False  # Exit the game
        
        # Check for collision with self
        for segment in snake_pos[1:]:
            if head_x == segment[0] and head_y == segment[1]:
                running = False
        
        # Draw snake
        for i, segment in enumerate(snake_pos):
            if i == 0:  # head
                pygame.draw.rect(screen, BODY_OUTER, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(screen, RED, (segment[0] + 1, segment[1] + 1, CELL_SIZE - 2, CELL_SIZE - 2))
            else:  # body
                pygame.draw.rect(screen, BODY_OUTER, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(screen, BODY_INNER, (segment[0] + 1, segment[1] + 1, CELL_SIZE - 2, CELL_SIZE - 2))
        
        # update the display and control frame rate
        pygame.display.flip()
        clock.tick(FPS)

def main_menu():
    # Initialize the menu window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Main Menu')
    
    font = pygame.font.SysFont('Arial', 40)
    button_color = (100, 100, 200)
    text_color = (255, 255, 255)
    
    # Define the 'PLAY' button
    play_button_rect = pygame.Rect(0, SCREEN_HEIGHT // 3, 200, 50)
    play_button_rect.centerx = SCREEN_WIDTH // 2  # center the button horizontally
    play_text = font.render('PLAY', True, text_color)  # create the button text
    play_text_rect = play_text.get_rect(center=play_button_rect.center)  # center the text inside the button
    
    # Define the 'EXIT' button
    exit_button_rect = pygame.Rect(0, SCREEN_HEIGHT // 2, 200, 50)
    exit_button_rect.centerx = SCREEN_WIDTH // 2  # center the button horizontally
    exit_button_rect.y = SCREEN_HEIGHT // 2 + 20  # adjust vertical position
    exit_text = font.render('EXIT', True, text_color)  # create the button text
    exit_text_rect = exit_text.get_rect(center=exit_button_rect.center)  # center the text inside the button
    
    running_menu = True  # variable to control the menu loop
    clock = pygame.time.Clock()  
    
    while running_menu:
        screen.fill(BG)
        
        pygame.draw.rect(screen, button_color, play_button_rect)  # draw the 'PLAY' button
        screen.blit(play_text, play_text_rect)  # draw the 'PLAY' button text
        
        pygame.draw.rect(screen, button_color, exit_button_rect)  # draw the 'EXIT' button
        screen.blit(exit_text, exit_text_rect)  # draw the 'EXIT' button text
        
        # Loop through events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_menu = False  # exit the menu if the user closes the window
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # check for left mouse button click
                    mouse_pos = pygame.mouse.get_pos()  # get position of the mouse click
                    if play_button_rect.collidepoint(mouse_pos):  # check if 'PLAY' button was clicked
                        run_snake_game()  # start the snake game
                    elif exit_button_rect.collidepoint(mouse_pos):  # check if 'EXIT' button was clicked
                        running_menu = False  # exit the menu
        
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main_menu()
    pygame.quit()
    sys.exit()
