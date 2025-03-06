import pygame
import sys
import os
from time import sleep
from pygame.locals import *

os.chdir(os.path.dirname(os.path.abspath(__file__)))

pygame.init()

images = {
    "default": "default.png",
    "bar_chart": "bar_chart_selected.png",
    "pcp": "pcp_selected.png",
    "scatterplot": "scatterplot_selected.png",
    "globe": "globe_selected.png"
}

pcp_lines = [
    "africa.png",
    "asia.png",
    "south_america.png",
    "north_america.png",
    "europe.png",
    "oceania.png"
]
current_pcp_index = 0 

bar_chart_images = [
    "1995.png",
    "2005.png"
]
current_bar_chart_index = 0

joystick_movement_cooldown = 0.3  # Cooldown to prevent rapid cycling
last_move_time = 0

# Create a window
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gamepad Chart Selector")


def display_image(image_path):
    try:
        if not os.path.exists(image_path):
            print(f"Error: Image file not found: {image_path}")
            return
        img = pygame.image.load(image_path)
        img = img.convert_alpha()  # Maintain transparency and quality
        screen.fill((0, 0, 0))  # Clear screen before displaying new image
        img = pygame.transform.smoothscale(img, (WIDTH, HEIGHT))  # High-quality scaling
        screen.blit(img, (0, 0))
        pygame.display.flip()
    except pygame.error as e:
        print(f"Error loading image {image_path}: {e}")


state = 0
current_image = "default"
display_image(images[current_image])

# Gamepad setup
pygame.joystick.init()
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
else:
    print("No gamepad detected.")
    sys.exit()

# Main loop
running = True
while running:
    current_time = pygame.time.get_ticks() / 1000  # Get current time in seconds
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == JOYBUTTONDOWN:
            if event.button == 0:  # X button (confirm selection)
                print(f"Confirmed selection: {current_image}")
            elif event.button == 14:  # Right -> Bar Chart
                current_image = "bar_chart"
                display_image(bar_chart_images[current_bar_chart_index])
            elif event.button == 13:  # Left -> PCP
                current_image = "pcp"
                current_pcp_index = 0  # Reset selection when switching to PCP
                display_image(pcp_lines[current_pcp_index])
            elif event.button == 12:  # Down -> Scatterplot
                current_image = "scatterplot"
            elif event.button == 11:  # Up -> Globe
                current_image = "globe"
            display_image(images[current_image])
        
        # Handle Left Joystick movement when PCP is selected
        elif event.type == JOYAXISMOTION and current_image == "pcp":
            if event.axis == 1 and abs(event.value) > 0.5 and (current_time - last_move_time > joystick_movement_cooldown):  # Vertical movement cooldown
                if event.value < -0.5:  # Up
                    current_pcp_index = (current_pcp_index - 1) % len(pcp_lines)
                elif event.value > 0.5:  # Down
                    current_pcp_index = (current_pcp_index + 1) % len(pcp_lines)
                if 0 <= current_pcp_index < len(pcp_lines):
                    display_image(pcp_lines[current_pcp_index])
                last_move_time = current_time  # Update last movement time
        
        # Handle Right Joystick movement when Bar Chart is selected
        elif event.type == JOYAXISMOTION and current_image == "bar_chart":
            if event.axis == 2 and abs(event.value) > 0.5 and (current_time - last_move_time > joystick_movement_cooldown):  # Right joystick horizontal movement
                if event.value < -0.5:  # Left movement
                    current_bar_chart_index = max(0, current_bar_chart_index - 1)
                elif event.value > 0.5:  # Right movement
                    current_bar_chart_index = min(len(bar_chart_images) - 1, current_bar_chart_index + 1)
                display_image(bar_chart_images[current_bar_chart_index])
                last_move_time = current_time  # Update last movement time
    
    pygame.display.update()  
pygame.quit()
