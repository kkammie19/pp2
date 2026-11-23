
import pygame
from clock import MickeyClock

# Инициализация Pygame
pygame.init()

# Размер окна
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700

# Создание окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mickey's Clock")

# Создаем часы
mickey_clock = MickeyClock(screen)

# Контроль FPS
frame_clock = pygame.time.Clock()
FPS = 60

running = True

while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Белый фон
    screen.fill((255, 255, 255))

    # Рисуем часы
    mickey_clock.draw()

    # Обновляем экран
    pygame.display.flip()

    # Ограничиваем FPS
    frame_clock.tick(FPS)

pygame.quit()
