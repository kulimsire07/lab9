import pygame

# Инициализация Pygame
pygame.init()

# Константы экрана
WIDTH, HEIGHT = 500, 600
TOOLBAR_HEIGHT = 100
CANVAS_HEIGHT = HEIGHT - TOOLBAR_HEIGHT
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
COLORS = [BLACK, RED, GREEN, BLUE]

# Настройки рисования
current_tool = "brush"
current_color = BLACK
brush_size = 5

drawing = False
start_pos = None

# Загрузка иконок
brush_icon = pygame.image.load("brush.png")
eraser_icon = pygame.image.load("eraser.png")
rectangle_icon = pygame.image.load("rectangle.png")
circle_icon = pygame.image.load("circle.png")
brush_icon = pygame.transform.scale(brush_icon, (50, 50))
eraser_icon = pygame.transform.scale(eraser_icon, (50, 50))
rectangle_icon = pygame.transform.scale(rectangle_icon, (50, 50))
circle_icon = pygame.transform.scale(circle_icon, (50, 50))

# Функции рисования
def draw_circle(surface, color, start, end):
    radius = int(((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2) ** 0.5)
    pygame.draw.circle(surface, color, start, radius, 2)

def draw_rectangle(surface, color, start, end):
    rect = pygame.Rect(start, (end[0] - start[0], end[1] - start[1]))
    pygame.draw.rect(surface, color, rect, 2)

# Основной игровой цикл
running = True
clock = pygame.time.Clock()
canvas = pygame.Surface((WIDTH, CANVAS_HEIGHT))
canvas.fill(WHITE)

while running:
    screen.fill(WHITE)
    screen.blit(canvas, (0, 0))
    pygame.draw.rect(screen, (200, 200, 200), (0, CANVAS_HEIGHT, WIDTH, TOOLBAR_HEIGHT))
    
    # Отображение кнопок инструментов
    screen.blit(brush_icon, (10, CANVAS_HEIGHT + 10))
    screen.blit(eraser_icon, (70, CANVAS_HEIGHT + 10))
    screen.blit(rectangle_icon, (130, CANVAS_HEIGHT + 10))
    screen.blit(circle_icon, (190, CANVAS_HEIGHT + 10))
    
    # Отображение кнопок цветов
    for i, color in enumerate(COLORS):
        pygame.draw.rect(screen, color, (250 + i * 60, CANVAS_HEIGHT + 10, 50, 50))
        if color == current_color:
            pygame.draw.rect(screen, BLACK, (250 + i * 60, CANVAS_HEIGHT + 10, 50, 50), 2)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if y < CANVAS_HEIGHT:
                drawing = True
                start_pos = event.pos
            else:
                # Выбор инструмента
                if 10 <= x <= 60:
                    current_tool = "brush"
                elif 70 <= x <= 120:
                    current_tool = "eraser"
                elif 130 <= x <= 180:
                    current_tool = "rectangle"
                elif 190 <= x <= 240:
                    current_tool = "circle"
                # Выбор цвета
                for i, color in enumerate(COLORS):
                    if 250 + i * 60 <= x <= 300 + i * 60:
                        current_color = color
                        break
        
        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            if current_tool == "circle":
                draw_circle(canvas, current_color, start_pos, event.pos)
            elif current_tool == "rectangle":
                draw_rectangle(canvas, current_color, start_pos, event.pos)
        
        if event.type == pygame.MOUSEMOTION and drawing:
            if current_tool == "brush":
                pygame.draw.circle(canvas, current_color, event.pos, brush_size)
            elif current_tool == "eraser":
                pygame.draw.circle(canvas, WHITE, event.pos, brush_size)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

