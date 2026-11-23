
import pygame
from ball import Ball

# Инициализация Pygame
pygame.init()

# Размер окна
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Создание окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Moving Ball")

# Цвета
WHITE = (255, 255, 255)

# Создаём шарик
ball = Ball()

# Контроль FPS
clock = pygame.time.Clock()
FPS = 60

# Основной игровой цикл
running = True

while running:
    # Обрабатываем события
    for event in pygame.event.get():

        # Закрытие окна
        if event.type == pygame.QUIT:
            running = False

        # Нажатие клавиш
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:
                ball.move(0, -ball.speed, SCREEN_WIDTH, SCREEN_HEIGHT)

            elif event.key == pygame.K_DOWN:
                ball.move(0, ball.speed, SCREEN_WIDTH, SCREEN_HEIGHT)

            elif event.key == pygame.K_LEFT:
                ball.move(-ball.speed, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

            elif event.key == pygame.K_RIGHT:
                ball.move(ball.speed, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

    # Белый фон
    screen.fill(WHITE)

    # Рисуем шарик
    ball.draw(screen)

    # Обновляем экран
    pygame.display.flip()

    # Ограничиваем FPS
    clock.tick(FPS)

# Закрываем Pygame
pygame.quit()
