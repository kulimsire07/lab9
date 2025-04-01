import pygame
import random
import os

pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load images
player_image = pygame.image.load("Player.png")
enemy_image = pygame.image.load("Enemy.png")
road_image = pygame.image.load("AnimatedStreet.png")
coin_image = pygame.image.load("coin.png")
coin_image = pygame.transform.scale(coin_image, (20, 20))

# Player settings
player_width, player_height = 50, 80
player_x, player_y = WIDTH // 2 - player_width // 2, HEIGHT - 100
player_speed = 5

# Road settings (centered)
road_width = road_image.get_width()
road_x = (WIDTH - road_width) // 2  # Center road
road_y = 0
road_speed = 5

# Enemy car settings
enemy_width, enemy_height = 50, 80
enemy_x = road_x + (road_width // 2) - (enemy_width // 2)
enemy_y = -100
enemy_speed = 5

# Coin settings
coins = []
coin_spawn_time = 0
coin_spawn_delay = 1000  # Time between coin spawns in milliseconds
coin_weights = [1, 2, 3]  # Different coin values

# Score system
score = 0
font = pygame.font.Font(None, 36)

# Load sounds
pygame.mixer.init()
pygame.mixer.music.load("racer_background.wav")
pygame.mixer.music.play(-1)  # Loop background music

try:
    crash_sound = pygame.mixer.Sound("racer_crash.wav")
except pygame.error:
    crash_sound = None

running = True
clock = pygame.time.Clock()
while running:
    screen.fill(WHITE)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > road_x:  # Keep player inside the road
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < road_x + road_width - player_width:
        player_x += player_speed
    
    # Move road
    road_y += road_speed
    if road_y >= HEIGHT:
        road_y = 0  # Reset road position
    
    # Move enemy
    enemy_y += enemy_speed
    if enemy_y > HEIGHT:
        enemy_y = -100
        enemy_x = random.randint(road_x, road_x + road_width - enemy_width)
    
    # Check for collision with enemy
    if (player_x < enemy_x + enemy_width and
        player_x + player_width > enemy_x and
        player_y < enemy_y + enemy_height and
        player_y + player_height > enemy_y):
        if crash_sound:
            crash_sound.play()
        running = False
    
    # Spawn coins
    if pygame.time.get_ticks() - coin_spawn_time > coin_spawn_delay:
        coin_x = random.randint(road_x, road_x + road_width - coin_image.get_width())
        coin_weight = random.choice(coin_weights)
        coins.append([coin_x, -coin_image.get_height(), coin_weight])
        coin_spawn_time = pygame.time.get_ticks()
    
    # Move coins
    for coin in coins[:]:
        coin[1] += 5
        if coin[1] > HEIGHT:
            coins.remove(coin)
    
    # Check for collision with coins
    for coin in coins[:]:
        if (player_x < coin[0] + coin_image.get_width() and
            player_x + player_width > coin[0] and
            player_y < coin[1] + coin_image.get_height() and
            player_y + player_height > coin[1]):
            coins.remove(coin)
            score += coin[2]  # Increase score by coin's weight
    
    # Increase enemy speed after collecting N coins
    if score >= 10:
        enemy_speed = 7
    if score >= 20:
        enemy_speed = 9
    
    # Draw road (centered)
    screen.blit(road_image, (road_x, road_y))  # Centered road
    screen.blit(road_image, (road_x, road_y - HEIGHT))  # Moving road effect
    
    # Draw player
    screen.blit(player_image, (player_x, player_y))
    
    # Draw enemy
    screen.blit(enemy_image, (enemy_x, enemy_y))
    
    # Draw coins
    for coin in coins:
        screen.blit(coin_image, (coin[0], coin[1]))
    
    # Display score
    score_text = font.render(f"Coins: {score}", True, BLACK)
    screen.blit(score_text, (WIDTH - 120, 10))
    
    pygame.display.flip()
    clock.tick(30)

pygame.time.delay(1000)  # Pause before closing
pygame.quit()
