import pygame
import sys

# Step 1: Initialize Pygame
pygame.init()

# Screen settings
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Move the Rectangle")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 100)

# Rectangle settings
rect_width, rect_height = 100, 50
rect_x, rect_y = screen_width // 2, screen_height // 2
rect_speed = 5

# Initialize joystick
pygame.joystick.init()
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
else:
    joystick = None

# Step 2: Main game loop
running = True
while running:
    # Step 3: Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(WHITE)

    # Step 4: Update rectangle position
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or (joystick and joystick.get_axis(0) < -0.5):  # Left
        rect_x -= rect_speed
    if keys[pygame.K_RIGHT] or (joystick and joystick.get_axis(0) > 0.5):  # Right
        rect_x += rect_speed
    if keys[pygame.K_UP] or (joystick and joystick.get_axis(1) < -0.5):  # Up
        rect_y -= rect_speed
    if keys[pygame.K_DOWN] or (joystick and joystick.get_axis(1) > 0.5):  # Down
        rect_y += rect_speed

    # Draw the rectangle
    pygame.draw.rect(screen, BLUE, (rect_x, rect_y, rect_width, rect_height))

    # Refresh the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

# Step 5: Quit
pygame.quit()
sys.exit()
