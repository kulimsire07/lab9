import pygame

# Инициализация Pygame
pygame.init()

# Определение размеров окна
WIDTH, HEIGHT = 500, 600
TOOLBAR_HEIGHT = 150
CANVAS_HEIGHT = HEIGHT - TOOLBAR_HEIGHT
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

# Определение цветов
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
COLORS = [BLACK, RED, GREEN, BLUE]

current_tool = "brush"  # По умолчанию инструмент "кисть"
current_color = BLACK   # Цвет по умолчанию - черный
brush_size = 5          # Размер кисти

drawing = False
start_pos = None

# Загрузка иконок инструментов
image_folder = "/Users/tursynk.e/Desktop/lab/lab9/paint/"
icons = {}
try:
    icons['right_triangle'] = pygame.image.load(image_folder + "right_triangle.png")
    icons['equilateral_triangle'] = pygame.image.load(image_folder + "equilateral_triangle.png")
    icons['rhombus'] = pygame.image.load(image_folder + "rhombus.png")
    icons['brush'] = pygame.image.load(image_folder + "brush.png")
    icons['eraser'] = pygame.image.load(image_folder + "eraser.png")
    icons['rectangle'] = pygame.image.load(image_folder + "rectangle.png")
    icons['circle'] = pygame.image.load(image_folder + "circle.png")
    icons['square'] = pygame.image.load(image_folder + "square.png")
except FileNotFoundError:
    print("Ошибка: один или несколько файлов не найдены!")
    pygame.quit()
    exit()

# Изменение размера иконок
icon_size = (50, 50)
for key in icons:
    icons[key] = pygame.transform.scale(icons[key], icon_size)

# Функции для рисования геометрических фигур
def draw_circle(surface, color, start, end):
    """Функция рисования круга"""
    radius = int(((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2) ** 0.5)
    pygame.draw.circle(surface, color, start, radius, 2)

def draw_rectangle(surface, color, start, end):
    """Функция рисования прямоугольника"""
    rect = pygame.Rect(start, (end[0] - start[0], end[1] - start[1]))
    pygame.draw.rect(surface, color, rect, 2)

def draw_square(surface, color, start, end):
    """Функция рисования квадрата"""
    side_length = min(abs(end[0] - start[0]), abs(end[1] - start[1]))
    rect = pygame.Rect(start, (side_length, side_length))
    pygame.draw.rect(surface, color, rect, 2)

def draw_right_triangle(surface, color, start, end):
    """Функция рисования прямоугольного треугольника"""
    points = [start, (start[0], end[1]), end]
    pygame.draw.polygon(surface, color, points, 2)

def draw_equilateral_triangle(surface, color, start, end):
    """Функция рисования равностороннего треугольника"""
    side_length = min(abs(end[0] - start[0]), abs(end[1] - start[1]))
    height = (3 ** 0.5 / 2) * side_length
    points = [start, (start[0] + side_length, start[1]), (start[0] + side_length / 2, start[1] - height)]
    pygame.draw.polygon(surface, color, points, 2)

def draw_rhombus(surface, color, start, end):
    """Функция рисования ромба"""
    width = abs(end[0] - start[0])
    height = abs(end[1] - start[1])
    points = [(start[0] + width / 2, start[1]), 
              (start[0] + width, start[1] + height / 2),
              (start[0] + width / 2, start[1] + height),
              (start[0], start[1] + height / 2)]
    pygame.draw.polygon(surface, color, points, 2)

# Основной цикл программы
running = True
clock = pygame.time.Clock()
canvas = pygame.Surface((WIDTH, CANVAS_HEIGHT))
canvas.fill(WHITE)

while running:
    screen.fill(WHITE)
    screen.blit(canvas, (0, 0))
    
    # Панель инструментов и цветов (в одном ряду)
    pygame.draw.rect(screen, (200, 200, 200), (0, CANVAS_HEIGHT, WIDTH, TOOLBAR_HEIGHT))

    # Отображаем иконки инструментов в первом ряду
    icons_list = [
        ('right_triangle', 10, CANVAS_HEIGHT + 10),
        ('equilateral_triangle', 70, CANVAS_HEIGHT + 10),
        ('rhombus', 130, CANVAS_HEIGHT + 10),
        ('square', 190, CANVAS_HEIGHT + 10),
        ('rectangle', 250, CANVAS_HEIGHT + 10),
        ('circle', 310, CANVAS_HEIGHT + 10),
    ]
    
    # Отображаем иконки фигур
    for icon_name, x_pos, y_pos in icons_list:
        screen.blit(icons[icon_name], (x_pos, y_pos))

    # Второй ряд с кистью, стеркой и выбором цветов
    screen.blit(icons['brush'], (10, CANVAS_HEIGHT + 70))  # Кисть
    screen.blit(icons['eraser'], (70, CANVAS_HEIGHT + 70))  # Стерка

    # Панель выбора цветов внизу
    color_offset = 150  # Отступ для цветов
    for i, color in enumerate(COLORS):
        pygame.draw.rect(screen, color, (color_offset + i * 60, CANVAS_HEIGHT + 70, 50, 50))
        if color == current_color:
            pygame.draw.rect(screen, BLACK, (color_offset + i * 60, CANVAS_HEIGHT + 70, 50, 50), 2)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if y < CANVAS_HEIGHT:
                drawing = True
                start_pos = event.pos
            else:
                # Обработка кликов по инструментам
                tool_height = 50  # Высота каждого инструмента
                tools_x = [10, 70, 130, 190, 250, 310]
                tools = ["right_triangle", "equilateral_triangle", "rhombus", "square", "rectangle", "circle"]
                for i, tool_x in enumerate(tools_x):
                    if tool_x <= x <= tool_x + icon_size[0] and CANVAS_HEIGHT + 10 <= y <= CANVAS_HEIGHT + 60:
                        current_tool = tools[i]
                        break

                # Обработка кликов по цветам
                for i, color in enumerate(COLORS):
                    if color_offset + i * 60 <= x <= color_offset + (i + 1) * 60 and CANVAS_HEIGHT + 70 <= y <= CANVAS_HEIGHT + 120:
                        current_color = color
                        break

                # Обработка кликов по кисти и стерке
                if 10 <= x <= 60 and CANVAS_HEIGHT + 70 <= y <= CANVAS_HEIGHT + 120:
                    current_tool = "brush"
                elif 70 <= x <= 120 and CANVAS_HEIGHT + 70 <= y <= CANVAS_HEIGHT + 120:
                    current_tool = "eraser"
        
        if event.type == pygame.MOUSEBUTTONUP and drawing:
            drawing = False
            if current_tool == "circle":
                draw_circle(canvas, current_color, start_pos, event.pos)
            elif current_tool == "rectangle":
                draw_rectangle(canvas, current_color, start_pos, event.pos)
            elif current_tool == "square":
                draw_square(canvas, current_color, start_pos, event.pos)
            elif current_tool == "right_triangle":
                draw_right_triangle(canvas, current_color, start_pos, event.pos)
            elif current_tool == "equilateral_triangle":
                draw_equilateral_triangle(canvas, current_color, start_pos, event.pos)
            elif current_tool == "rhombus":
                draw_rhombus(canvas, current_color, start_pos, event.pos)
        
        if event.type == pygame.MOUSEMOTION and drawing:
            if current_tool == "brush":
                pygame.draw.circle(canvas, current_color, event.pos, brush_size)
            elif current_tool == "eraser":
                pygame.draw.circle(canvas, WHITE, event.pos, brush_size)

    pygame.display.update()
    clock.tick(60)

pygame.quit()

