import pygame
import math
import datetime
import os


class MickeyClock:
    def __init__(self, screen):
        self.screen = screen

        # Load clock image using the path of this file
        image_path = os.path.join(
            os.path.dirname(__file__),
            "images",
            "mickey_clock.jpg"
        )

        self.image = pygame.image.load(image_path)

        # Resize the clock image
        self.image = pygame.transform.scale(self.image, (600, 600))

        # Clock center
        self.center_x = 400
        self.center_y = 350

    def draw_hand(self, angle, length, color, width):
        # Convert angle to radians
        angle_rad = math.radians(angle - 90)

        # Calculate hand endpoint
        end_x = self.center_x + length * math.cos(angle_rad)
        end_y = self.center_y + length * math.sin(angle_rad)

        # Draw the hand
        pygame.draw.line(
            self.screen,
            color,
            (self.center_x, self.center_y),
            (end_x, end_y),
            width
        )

    def draw(self):
        # Display the clock image
        self.screen.blit(
            self.image,
            (self.center_x - 300, self.center_y - 300)
        )

        # Get current system time
        now = datetime.datetime.now()

        seconds = now.second
        minutes = now.minute

        # Calculate angles
        second_angle = seconds * 6
        minute_angle = minutes * 6 + seconds * 0.1

        # Left hand - seconds
        self.draw_hand(
            second_angle, 190,
            (220, 30, 30), 6
        )

        # Right hand - minutes
        self.draw_hand(
            minute_angle, 140,
            (30, 30, 30), 10
        )

        # Draw center circle
        pygame.draw.circle(
            self.screen,
            (30, 30, 30),
            (self.center_x, self.center_y),
            12
        )