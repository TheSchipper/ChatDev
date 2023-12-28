'''
This is the main file of the game. It initializes the game window, creates the game objects, and handles the game loop.
'''
import pygame
import random
import math
from pygame.math import Vector2
# Initialize the game
pygame.init()
# Set up the game window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Gravity Game")
# Define colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
# Define the gravity constant
GRAVITY = 0.1
# Define the class for the smaller circles
class Circle:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.velocity_x = random.uniform(-1, 1)
        self.velocity_y = random.uniform(-1, 1)
        self.position = Vector2(self.x, self.y)
    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def collides_with(self, other_circle):
        distance = self.position.distance_to(other_circle.position)
        return distance <= self.radius + other_circle.radius
# Define the class for the larger red circle
class RedCircle:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
    def apply_gravity(self, circle):
        dx = circle.x - self.x
        dy = circle.y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance > 0:
            force = GRAVITY / (distance ** 2)
            circle.velocity_x -= force * dx
            circle.velocity_y -= force * dy
# Create the smaller circles
circles = []
for _ in range(25):
    x = random.randint(0, screen_width)
    y = random.randint(0, screen_height)
    radius = random.randint(10, 30)
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    circle = Circle(x, y, radius, color)
    circles.append(circle)
# Create the larger red circle
red_circle = RedCircle(screen_width // 2, screen_height // 2, 50, RED)
# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Update the circles
    for circle in circles:
        circle.update()
        red_circle.apply_gravity(circle)
        # Check for collision with the red circle
        dx = circle.x - red_circle.x
        dy = circle.y - red_circle.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance < circle.radius + red_circle.radius:
            circles.remove(circle)
        # Check for collisions between small circles
        for i in range(len(circles)):
            for j in range(i + 1, len(circles)):
                if circles[i].collides_with(circles[j]):
                    try:
                        circles.remove(circle[i])
                        circles.remove(circle[j])
                    except:
                        pass
    # Clear the screen
    screen.fill(BLACK)
    # Draw the circles
    for circle in circles:
        circle.draw()
    red_circle.draw()
    # Update the display
    pygame.display.flip()
# Quit the game
pygame.quit()