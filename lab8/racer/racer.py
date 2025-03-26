import pygame
import random
import os


pygame.init()


WIDTH, HEIGHT = 500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer Game")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


player_image = pygame.image.load("Player.png")
enemy_image = pygame.image.load("Enemy.png")
road_image = pygame.image.load("AnimatedStreet.png")
coin_image = pygame.image.load("coin.png")
coin_image = pygame.transform.scale(coin_image, (20, 20)) 

player_width, player_height = 50, 80
player_x, player_y = WIDTH // 2 - player_width // 2, HEIGHT - 100
player_speed = 5

# Дорога (движущийся фон)
road_y = 0
road_speed = 5

# Вражеская машина
enemy_width, enemy_height = 50, 80
enemy_x = random.randint(50, WIDTH - 50 - enemy_width)
enemy_y = -100
enemy_speed = 5

# Монеты
coin_size = 20
coins = []
coin_spawn_time = 0
coin_spawn_delay = 1000  


score = 0
font = pygame.font.Font(None, 36)

# Звуки
pygame.mixer.init()
pygame.mixer.music.load("racer_background.wav")
pygame.mixer.music.play(-1)  

print("Файл racer_crash.wav существует:", os.path.isfile("racer_crash.wav"))
try:
    crash_sound = pygame.mixer.Sound("racer_crash.wav")
    print("Звук аварии успешно загружен")
except pygame.error:
    print("Ошибка загрузки racer_crash.wav")
    crash_sound = None

running = True
clock = pygame.time.Clock()
while running:
    screen.fill(WHITE)  
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
   
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
        player_x += player_speed
    
   
    road_y += road_speed
    if road_y >= HEIGHT:
        road_y = 0  
    
    
    enemy_y += enemy_speed
    if enemy_y > HEIGHT:
        enemy_y = -100
        enemy_x = random.randint(50, WIDTH - 50 - enemy_width)
    
    
    if (player_x < enemy_x + enemy_width and
        player_x + player_width > enemy_x and
        player_y < enemy_y + enemy_height and
        player_y + player_height > enemy_y):
        print("Столкновение! Попытка воспроизведения звука.")
        if crash_sound:
            crash_sound.play()
            print("Звук аварии воспроизведён")
        else:
            print("Звук аварии не загружен")
        running = False
    
  
    if pygame.time.get_ticks() - coin_spawn_time > coin_spawn_delay:
        coin_x = random.randint(0, WIDTH - coin_size)
        coins.append([coin_x, -coin_size])
        coin_spawn_time = pygame.time.get_ticks()
    
   
    for coin in coins[:]:
        coin[1] += 5
        if coin[1] > HEIGHT:
            coins.remove(coin)
    
   
    for coin in coins[:]:
        if (player_x < coin[0] + coin_size and
            player_x + player_width > coin[0] and
            player_y < coin[1] + coin_size and
            player_y + player_height > coin[1]):
            coins.remove(coin)
            score += 1
    
   
    screen.blit(road_image, (0, road_y))
    screen.blit(road_image, (0, road_y - HEIGHT))  
    
    
    screen.blit(player_image, (player_x, player_y))
    screen.blit(enemy_image, (enemy_x, enemy_y))
    
    
    for coin in coins:
        screen.blit(coin_image, (coin[0], coin[1]))
    
    
    score_text = font.render(f"Coins: {score}", True, BLACK)
    screen.blit(score_text, (WIDTH - 100, 10))
    
    pygame.display.flip()
    clock.tick(30) 
pygame.time.delay(1000)  


pygame.quit()
