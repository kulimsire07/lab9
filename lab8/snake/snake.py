import pygame
import random
import time

pygame.init()

# Устанавливаем размеры экрана игры
w, h = (720, 480)

# Определение цветов для использования в игре
white = (255, 255, 255)
green = (0, 190, 0)
red = (255, 0, 0)
purple = (128, 0, 128)

# Настройка экрана
screen = pygame.display.set_mode((w, h))

# Создаем объект для контроля FPS
clock = pygame.time.Clock()

# Начальная позиция головы змеи
snakepos = [100, 50]

# Начальное тело змеи
snakebody = [[100, 50], [90, 50], [80, 50], [70, 50]]

# Позиция яблока
apple_pos = [random.randrange(1, (w // 10)) * 10, random.randrange(1, (h // 10)) * 10]

# Флаг для отслеживания появления яблока
app_spawn = True

# Направление змеи
direction = 'RIGHT'
change_to = direction

# Начальный счет
score = 0
count_app = 0

# Начальная скорость змеи
snake_speed = 5

# Функция для отображения счета
def score_show(color, font, size):
    score_font = pygame.font.Font(font, 30)
    score_surf = score_font.render(f'SCORE:{score}', True, white)
    screen.blit(score_surf, (10, 10))

# Функция для завершения игры
def game_over():
    my_font = pygame.font.Font(None, 50)
    over = my_font.render(f'YOUR SCORE IS:{score}', True, red)
    screen.blit(over, (w / 4, h / 4))
    pygame.display.update()
    time.sleep(2)
    pygame.quit()
    exit()

# Основной игровой цикл
while True:
    for event in pygame.event.get():  # Получаем все события
        if event.type == pygame.KEYDOWN:  # Если нажата клавиша
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'

    # Устанавливаем направление змеи
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'

    # Изменяем координаты головы змеи в зависимости от направления
    if direction == 'UP':
        snakepos[1] -= 10
    if direction == 'DOWN':
        snakepos[1] += 10
    if direction == 'LEFT':
        snakepos[0] -= 10
    if direction == 'RIGHT':
        snakepos[0] += 10

    # Добавляем новую позицию головы змеи в начало списка
    snakebody.insert(0, list(snakepos))

    # Проверка, если змея съела яблоко
    if snakepos == apple_pos:
        score += 10
        count_app += 1
        app_spawn = False
    else:
        snakebody.pop()  # Удаляем последний сегмент змеи

    # Если яблоко съедено, создаем новое яблоко
    if not app_spawn:
        apple_pos = [random.randrange(1, (w // 10)) * 10, random.randrange(1, (h // 10)) * 10]
    app_spawn = True

    # Заполняем экран фоном
    screen.fill(green)

    # Рисуем каждый сегмент змеи
    for pos in snakebody:
        pygame.draw.rect(screen, purple, pygame.Rect(pos[0], pos[1], 10, 10))

    # Рисуем яблоко
    pygame.draw.rect(screen, red, pygame.Rect(apple_pos[0], apple_pos[1], 10, 10))

    # Проверка на выход змеи за границы экрана
    if snakepos[0] < 0 or snakepos[0] > w - 10 or snakepos[1] < 0 or snakepos[1] > h - 10:
        game_over()

    # Проверка на столкновение змеи с собой
    if snakepos in snakebody[1:]:
        game_over()

    # Увеличиваем скорость после 4 съеденных яблок
    if count_app == 4:
        snake_speed += 3
        count_app = 0

    # Отображаем текущий счет
    score_show(red, None, 30)

    # Обновляем экран
    pygame.display.update()

    # Ограничиваем количество кадров в секунду
    clock.tick(snake_speed)