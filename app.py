'''
RUN THIS FILE TO START THE GAME
'''
import pygame
import sys
import random

print("...")
print('...')
print("starting snake")

pygame.init()

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)

window_width = 500
window_height = 500

# Set up the display
pygame.display.set_caption('SNAKE')
window_size = (window_width, window_height)
screen = pygame.display.set_mode(window_size)

# Set up grid
num_grid_cols = round(window_width / 20)
num_grid_rows = round(window_height / 20)
grid = [[0 for _ in range(num_grid_cols)] for _ in range(num_grid_rows)]

# Initialize fps clock
clock = pygame.time.Clock()

# Initialize snake array
snake_array = []

# Set initial random snake starting point
head_column_start_pixel = (round(num_grid_cols / 2) * 20) + 3
head_row_start_pixel = (round(num_grid_rows / 2) * 20) + 3
snake_head = pygame.Rect(head_column_start_pixel, head_row_start_pixel, 14, 14)
snake_array.append(snake_head)

# Set initial food
random_food_column = random.randrange(num_grid_cols)
random_food_row = random.randrange(num_grid_rows)
random_food_column_start_pixel = (random_food_column * 20) + 3
random_food_row_start_pixel = (random_food_row * 20) + 3
food = pygame.Rect(random_food_column_start_pixel, random_food_row_start_pixel, 14, 14)

# Set initial direction
direction = ""

'''
FUNCTIONS
'''
def update_snake_head_position(part, direction):
    if direction == "":
        return part
    direction_object = {
        "n": [0, -20],
        "s": [0, 20],
        "e": [20, 0],
        "w": [-20, 0]
    }
    new_snake_part_pos = part.move(
        direction_object[direction][0],
        direction_object[direction][1]
    )

    return new_snake_part_pos

def generate_new_food():
    rand_col = random.randrange(num_grid_cols)
    rand_row = random.randrange(num_grid_rows)
    random_col_start_pixel = (rand_col * 20) + 3
    random__row_start_pixel = (rand_row * 20) + 3
    return pygame.Rect(random_col_start_pixel, random__row_start_pixel, 14, 14)

def validate_food(snake_list, food):
    for i in snake_list:
        if food.colliderect(i):
            return False
        
    return True

def render_objects_and_move_snake(snake_list, direction):
    global food
    screen.fill(black)

    # Push new snake head to front of list and pop last from list
    new_snake_head = update_snake_head_position(snake_list[0], direction)
    snake_list.insert(0, new_snake_head)

    if new_snake_head.colliderect(food):
        print("food eaten!")
        valid_food = False
        while not valid_food:
            new_food = generate_new_food()
            if validate_food(snake_list, new_food):
                valid_food = True
        food = new_food
    else:
        snake_list.pop()

    for i in snake_list:
        pygame.draw.rect(screen, green, i)

    pygame.draw.rect(screen, red, food)

def check_head_for_border(head):
    if head.left < 0 or head.left >= window_width:
        return True
    if head.top < 0 or head.top >= window_height:
        return True
    return False

def check_head_for_snake_collision(snake_list):
    head = snake_list[0]

    for i in snake_list[1:]:
        if head.colliderect(i):
            return True
    return False


direction_buffer = []
max_buffer_length = 2

active = True
while active:
    # Render positions
    render_objects_and_move_snake(snake_array, direction)

    if check_head_for_border(snake_array[0]):
        active = False
    
    if check_head_for_snake_collision(snake_array):
        active = False

    # Loop for key input with direction buffer for better input handling
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            new_direction = None
            if event.key == pygame.K_UP and direction != "s":
                new_direction = "n"
            elif event.key == pygame.K_DOWN and direction != "n":
                new_direction = "s"
            elif event.key == pygame.K_LEFT and direction != "e":
                new_direction = "w"
            elif event.key == pygame.K_RIGHT and direction != "w":
                new_direction = "e"

            if new_direction and (len(direction_buffer) < max_buffer_length):
                direction_buffer.append(new_direction)

        # Handler for pressing X on window
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if direction_buffer:
        direction = direction_buffer.pop(0)

    # Update head position
    pygame.display.flip()
    clock.tick(10)

print('YOU LOSE')
pygame.quit()
sys.exit()


    
