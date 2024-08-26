'''
Snake Game
Run this file to start the game
'''
import pygame
import sys
import random
import json

# Initialize Pygame
pygame.init()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Game dimensions
GRID_WIDTH = 500
GRID_HEIGHT = 500
WINDOW_WIDTH = GRID_WIDTH + 200
WINDOW_HEIGHT = GRID_HEIGHT + 200
BORDER_THICKNESS = 10

# Grid settings
GRID_CELL_SIZE = 20
NUM_GRID_COLS = round(GRID_WIDTH / GRID_CELL_SIZE)
NUM_GRID_ROWS = round(GRID_HEIGHT / GRID_CELL_SIZE)

# Set up main display
pygame.display.set_caption('SNAKE')
game_screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

# Game variables
score = 0
direction = ""
direction_buffer = []
MAX_BUFFER_LENGTH = 2

def initialize_snake():
    """Initialize the snake at the center of the grid."""
    head_column_start_pixel = (round(NUM_GRID_COLS / 2) * GRID_CELL_SIZE) + 3 + 100
    head_row_start_pixel = (round(NUM_GRID_ROWS / 2) * GRID_CELL_SIZE) + 3 + 100
    snake_head = pygame.Rect(head_column_start_pixel, head_row_start_pixel, 14, 14)
    return [snake_head]

snake_array = initialize_snake()

def generate_food():
    """Generate a new food item at a random position."""
    random_col = random.randrange(NUM_GRID_COLS)
    random_row = random.randrange(NUM_GRID_ROWS)
    food_x = (random_col * GRID_CELL_SIZE) + 3 + 100
    food_y = (random_row * GRID_CELL_SIZE) + 3 + 100
    return pygame.Rect(food_x, food_y, 14, 14)

food = generate_food()

def update_snake_position(snake_part, direction):
    """Update the position of a snake part based on the direction."""
    if not direction:
        return snake_part
    direction_map = {
        "n": [0, -GRID_CELL_SIZE],
        "s": [0, GRID_CELL_SIZE],
        "e": [GRID_CELL_SIZE, 0],
        "w": [-GRID_CELL_SIZE, 0]
    }
    return snake_part.move(*direction_map[direction])

def is_food_valid(snake_list, food):
    """Check if the food is not colliding with the snake."""
    return not any(food.colliderect(part) for part in snake_list)

def move_snake_and_check_collision(snake_list, direction):
    """Move the snake, check for collisions, and update the game state."""
    global food, score
    game_screen.fill(BLACK)

    # Draw the border
    pygame.draw.rect(game_screen, WHITE, (100 - BORDER_THICKNESS, 100 - BORDER_THICKNESS, 
                                          GRID_WIDTH + 2*BORDER_THICKNESS, 
                                          GRID_HEIGHT + 2*BORDER_THICKNESS), BORDER_THICKNESS)

    # Move the snake
    new_snake_head = update_snake_position(snake_list[0], direction)
    snake_list.insert(0, new_snake_head)

    # Check for food collision
    if new_snake_head.colliderect(food):
        score += 5
        while True:
            new_food = generate_food()
            if is_food_valid(snake_list, new_food):
                food = new_food
                break
    else:
        snake_list.pop()

    # Draw snake and food
    for part in snake_list:
        pygame.draw.rect(game_screen, GREEN, part)
    pygame.draw.rect(game_screen, RED, food)

    # Render the score
    render_score(score)

def is_collision_with_border(head):
    """Check if the snake has collided with the border."""
    return (head.left < 100 or head.left >= WINDOW_WIDTH - 100 or
            head.top < 100 or head.top >= WINDOW_HEIGHT - 100)

def is_collision_with_self(snake_list):
    """Check if the snake has collided with itself."""
    return any(snake_list[0].colliderect(part) for part in snake_list[1:])

def update_high_scores(score):
    """Update the high scores file if the current score qualifies."""
    try:
        with open("high_scores.json", "r") as f:
            high_scores = json.load(f)
    except FileNotFoundError:
        high_scores = []

    if len(high_scores) < 10 or score > min(hs['score'] for hs in high_scores):
        user_name = text_input_box("Enter your name: ")
        if user_name is None:
            return False
        high_scores.append({"name": user_name, "score": score})
        high_scores = sorted(high_scores, key=lambda x: x['score'], reverse=True)[:10]

        with open("high_scores.json", "w") as f:
            json.dump(high_scores, f, indent=4)

        return True
    return False

def text_input_box(prompt):
    """Display a text input box for the user to enter their name."""
    input_box = pygame.Rect(WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2 - 20, 300, 40)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_active
    active = True
    text = ''
    font = pygame.font.Font(None, 32)
    
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))

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

        game_screen.blit(overlay, (0, 0))
        pygame.draw.rect(game_screen, color, input_box, border_radius=10)
        pygame.draw.rect(game_screen, WHITE, input_box, 2, border_radius=10)

        txt_surface = font.render(text, True, WHITE)
        text_width = txt_surface.get_width()
        text_x = input_box.x + (300 - text_width) // 2
        text_y = input_box.y + (40 - txt_surface.get_height()) // 2
        game_screen.blit(txt_surface, (text_x, text_y))

        prompt_font = pygame.font.Font(None, 36)
        prompt_text = prompt_font.render(prompt, True, WHITE)
        prompt_x = WINDOW_WIDTH // 2 - prompt_text.get_width() // 2
        prompt_y = input_box.y - 50
        game_screen.blit(prompt_text, (prompt_x, prompt_y))

        pygame.display.flip()
        clock.tick(30)

def show_game_over_screen(score):
    """Display the game over screen with high scores."""
    game_screen.fill(BLACK)
    font = pygame.font.Font(None, 36)

    game_over_text = font.render("GAME OVER", True, WHITE)
    game_screen.blit(game_over_text, (WINDOW_WIDTH // 2 - game_over_text.get_width() // 2, 150))

    try:
        with open("high_scores.json", "r") as f:
            high_scores = json.load(f)
    except FileNotFoundError:
        high_scores = []

    start_y = 200
    for index, entry in enumerate(high_scores, start=1):
        score_text = font.render(f"{index}. {entry['name']} - {entry['score']}", True, WHITE)
        game_screen.blit(score_text, (WINDOW_WIDTH // 2 - score_text.get_width() // 2, start_y))
        start_y += 30

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

def render_score(score):
    """Render the current score on the screen."""
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50))
    game_screen.blit(score_text, score_rect)

def main_game_loop():
    """Main game loop."""
    global direction, score
    active = True
    while active:
        move_snake_and_check_collision(snake_array, direction)

        if is_collision_with_border(snake_array[0]) or is_collision_with_self(snake_array):
            active = False

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

                if new_direction and (len(direction_buffer) < MAX_BUFFER_LENGTH):
                    direction_buffer.append(new_direction)

            if event.type == pygame.QUIT:
                return

        if direction_buffer:
            direction = direction_buffer.pop(0)

        pygame.display.flip()
        clock.tick(10)

    if update_high_scores(score):
        print("New Top 10 Score!")
    show_game_over_screen(score)

if __name__ == "__main__":
    main_game_loop()
    pygame.quit()
    sys.exit()