'''
RUN THIS FILE TO START THE GAME
'''
import pygame
import sys
import random
import json

pygame.init()

# Initialize score
score = 0

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)

# Game grid size
game_grid_width = 500
game_grid_height = 500

# Window size (including border)
window_width = game_grid_width + 200  # 100px on each side
window_height = game_grid_height + 200  # 100px on each side

# Set up main display
pygame.display.set_caption('SNAKE')

# Set up the game display
window_size = (window_width, window_height)
game_screen = pygame.display.set_mode(window_size)

# Border thickness
border_thickness = 10

# Set up grid
num_grid_cols = round(game_grid_width / 20)
num_grid_rows = round(game_grid_height / 20)
grid = [[0 for _ in range(num_grid_cols)] for _ in range(num_grid_rows)]

# Initialize fps clock
clock = pygame.time.Clock()

# Initialize snake array
snake_array = []

# Adjust the starting position of the snake
head_column_start_pixel = (round(num_grid_cols / 2) * 20) + 3 + 100  # Add 100 for the left border
head_row_start_pixel = (round(num_grid_rows / 2) * 20) + 3 + 100  # Add 100 for the top border
snake_head = pygame.Rect(head_column_start_pixel, head_row_start_pixel, 14, 14)
snake_array.append(snake_head)

# Set initial food
random_food_column = random.randrange(num_grid_cols)
random_food_row = random.randrange(num_grid_rows)
random_food_column_start_pixel = (random_food_column * 20) + 3 + 100  # Add 100 for the left border
random_food_row_start_pixel = (random_food_row * 20) + 3 + 100  # Add 100 for the top border
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

# Adjust the food position
def generate_new_food():
    rand_col = random.randrange(num_grid_cols)
    rand_row = random.randrange(num_grid_rows)
    random_col_start_pixel = (rand_col * 20) + 3 + 100  # Add 100 for the left border
    random_row_start_pixel = (rand_row * 20) + 3 + 100  # Add 100 for the top border
    return pygame.Rect(random_col_start_pixel, random_row_start_pixel, 14, 14)

def validate_food(snake_list, food):
    for i in snake_list:
        if food.colliderect(i):
            return False
        
    return True

def render_objects_and_move_snake(snake_list, direction):
    global food, score
    game_screen.fill(black)

    # Draw the white border
    pygame.draw.rect(game_screen, white, (100 - border_thickness, 100 - border_thickness, 
                                          game_grid_width + 2*border_thickness, 
                                          game_grid_height + 2*border_thickness), border_thickness)

    # Push new snake head to front of list and pop last from list
    new_snake_head = update_snake_head_position(snake_list[0], direction)
    snake_list.insert(0, new_snake_head)

    if new_snake_head.colliderect(food):
        print("food eaten!")
        score += 5
        print(score)
        valid_food = False
        while not valid_food:
            new_food = generate_new_food()
            if validate_food(snake_list, new_food):
                valid_food = True
        food = new_food
    else:
        snake_list.pop()

    for i in snake_list:
        pygame.draw.rect(game_screen, green, i)

    pygame.draw.rect(game_screen, red, food)

    # Render the score
    render_score(score)

# Modify the check_head_for_border function
def check_head_for_border(head):
    if head.left < 100 or head.left >= window_width - 100:
        return True
    if head.top < 100 or head.top >= window_height - 100:
        return True
    return False

def check_head_for_snake_collision(snake_list):
    head = snake_list[0]

    for i in snake_list[1:]:
        if head.colliderect(i):
            return True
    return False

# 10 high score limit enforced in this fn
def check_if_new_high_score(score):
    try:
        with open("high_scores.json", "r") as f:
            high_scores = json.load(f)
    except FileNotFoundError:
        high_scores = []

    if len(high_scores) < 10 or score > min(hs['score'] for hs in high_scores):
        user_name = text_input_box("Enter your name: ")  # Use Pygame text input
        if user_name is None:
            return False  # Handle the case where the player closes the window
        high_scores.append({"name": user_name, "score": score})
        high_scores = sorted(high_scores, key=lambda x: x['score'], reverse=True)[:10]  # Keep top 10 scores only

        with open("high_scores.json", "w") as f:
            json.dump(high_scores, f, indent=4)

        return True
    return False

def text_input_box(prompt):
    input_box_width = 300
    input_box_height = 40
    input_box = pygame.Rect(window_width // 2 - input_box_width // 2, 
                            window_height // 2 - input_box_height // 2, 
                            input_box_width, input_box_height)
    
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = True
    text = ''
    font = pygame.font.Font(None, 32)
    
    overlay = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))  # Semi-transparent black overlay

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                active = input_box.collidepoint(event.pos)
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        return text
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        game_screen.blit(overlay, (0, 0))  # Add semi-transparent overlay

        # Render the input box
        pygame.draw.rect(game_screen, color, input_box, border_radius=10)
        pygame.draw.rect(game_screen, white, input_box, 2, border_radius=10)  # White border

        # Render the current text
        txt_surface = font.render(text, True, white)
        text_width = txt_surface.get_width()
        text_x = input_box.x + (input_box_width - text_width) // 2
        text_y = input_box.y + (input_box_height - txt_surface.get_height()) // 2
        game_screen.blit(txt_surface, (text_x, text_y))

        # Display the prompt
        prompt_font = pygame.font.Font(None, 36)
        prompt_text = prompt_font.render(prompt, True, white)
        prompt_x = window_width // 2 - prompt_text.get_width() // 2
        prompt_y = input_box.y - 50
        game_screen.blit(prompt_text, (prompt_x, prompt_y))

        pygame.display.flip()
        clock.tick(30)

def show_game_over_screen(score):
    game_screen.fill(black)
    font = pygame.font.Font(None, 36)

    # Display a simple game over message
    game_over_text = font.render("GAME OVER", True, white)
    game_screen.blit(game_over_text, (window_width // 2 - game_over_text.get_width() // 2, 150))

    # Load and display high scores
    try:
        with open("high_scores.json", "r") as f:
            high_scores = json.load(f)
    except FileNotFoundError:
        high_scores = []

    start_y = 200
    for index, entry in enumerate(high_scores, start=1):
        score_text = font.render(f"{index}. {entry['name']} - {entry['score']}", True, white)
        game_screen.blit(score_text, (window_width // 2 - score_text.get_width() // 2, start_y))
        start_y += 30

    pygame.display.flip()

    # Loop until an exit event or a return key press
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return  # Exit the function if the QUIT event is triggered
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return  # Exit the function if the Return key is pressed

def render_score(score):
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, white)
    score_rect = score_text.get_rect(center=(window_width // 2, window_height - 50))
    game_screen.blit(score_text, score_rect)


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

    if not active:
        if check_if_new_high_score(score):
            print("New Top 10 Score!")
        show_game_over_screen(score)  # Display the game over screen
        break  # Exit the loop after showing the game over screen

pygame.quit()
sys.exit()


    
