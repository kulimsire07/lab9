import pygame
import random
import time
vhbj bhvj
pygame.init()

# Set screen dimensions
WIDTH, HEIGHT = 720, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 190, 0)  # Background
RED = (255, 0, 0)  # Food
PURPLE = (128, 0, 128)  # Snake

# Initialize game clock
clock = pygame.time.Clock()

# Snake settings
snake_pos = [100, 50]  # Head position
snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]  # Initial body
direction = 'RIGHT'  # Default movement
change_to = direction
snake_speed = 10  # Increased initial speed

# Food settings
food_pos = [random.randrange(1, (WIDTH // 10)) * 10, random.randrange(1, (HEIGHT // 10)) * 10]
food_spawn = True
food_weight = random.choice([1, 2, 3])  # Food gives 1, 2, or 3 points
food_timer = time.time()  # Start timer for food
food_lifetime = 8  # Food disappears after 8 seconds (increased time)

# Score
score = 0
count_food = 0  # Counter for increasing speed

# Function to display the score
def show_score():
    font = pygame.font.Font(None, 30)
    score_surface = font.render(f'Score: {score}', True, WHITE)
    screen.blit(score_surface, (10, 10))

# Function to end the game
def game_over():
    font = pygame.font.Font(None, 50)
    over_surface = font.render(f'Game Over! Score: {score}', True, RED)
    screen.blit(over_surface, (WIDTH / 4, HEIGHT / 4))
    pygame.display.update()
    time.sleep(2)
    pygame.quit()
    exit()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'DOWN':
                change_to = 'UP'
            if event.key == pygame.K_DOWN and direction != 'UP':
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT and direction != 'RIGHT':
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT and direction != 'LEFT':
                change_to = 'RIGHT'

    # Update direction
    direction = change_to

    # Move snake in the current direction
    if direction == 'UP':
        snake_pos[1] -= 10
    if direction == 'DOWN':
        snake_pos[1] += 10
    if direction == 'LEFT':
        snake_pos[0] -= 10
    if direction == 'RIGHT':
        snake_pos[0] += 10

    # Add new head position
    snake_body.insert(0, list(snake_pos))

    # Check if snake eats food
    if snake_pos == food_pos:
        score += food_weight  # Increase score based on food weight
        count_food += 1  # Increase food counter
        food_spawn = False  # Food disappears
    else:
        snake_body.pop()  # Remove tail

    # Generate new food if eaten or expired
    if not food_spawn or time.time() - food_timer > food_lifetime:
        food_pos = [random.randrange(1, (WIDTH // 10)) * 10, random.randrange(1, (HEIGHT // 10)) * 10]
        food_weight = random.choice([1, 2, 3])  # New random weight
        food_timer = time.time()  # Reset timer
        food_spawn = True

    # Clear screen
    screen.fill(GREEN)

    # Draw the snake
    for pos in snake_body:
        pygame.draw.rect(screen, PURPLE, pygame.Rect(pos[0], pos[1], 10, 10))

    # Draw the food
    pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    # Display score
    show_score()

    # Check for collisions with walls
    if snake_pos[0] < 0 or snake_pos[0] > WIDTH - 10 or snake_pos[1] < 0 or snake_pos[1] > HEIGHT - 10:
        game_over()

    # Check for collisions with itself
    if snake_pos in snake_body[1:]:
        game_over()

    # Increase speed after every 4 food items
    if count_food == 4:
        snake_speed += 2  # Slight increase in speed
        count_food = 0  # Reset counter

    # Refresh screen
    pygame.display.update()
    clock.tick(snake_speed)
