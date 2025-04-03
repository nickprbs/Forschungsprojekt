import pygame
import sys
import os
from pygame.locals import *

# Set working directory to script location
os.chdir(os.path.dirname(os.path.abspath(__file__)))

pygame.init()

# Image paths 
images = {
    "all_charts": "sketches/all_charts.png",
    "globe_selected": "sketches/globe_selected.png",
    "bar_chart_selected": "sketches/bar_chart_selected.png",
    "pcp_selected": "sketches/pcp_selected.png",
    "scatterplot_selected": "sketches/scatterplot_selected.png",
    "globe": "sketches/temp_globe.png",
    "rainfall_globe": "sketches/rainfall_globe.png",
    "bar_chart": "sketches/bar_chart.png",
    "pcp": "sketches/pcp.png",
    "scatterplot": "sketches/scatterplot_1950.png",
    "bar3and6_info": "sketches/bar3and6_selected_info.png"
}

# Bar chart sub-selections
bar_image_paths = [f"sketches/bar{i}_selected.png" for i in range(1, 10)]
current_bar_index = 0

# Compare bar3 with 4–7
compare_mode = False
compare_index = 0
compare_images = [
    "sketches/bar3and4_selected.png",
    "sketches/bar3and5_selected.png",
    "sketches/bar3and6_selected.png",
    "sketches/bar3and7_selected.png"
]

# Scatterplot years
scatterplot_years = [
    "sketches/scatterplot_1950.png",
    "sketches/scatterplot_1980.png",
    "sketches/scatterplot_2010.png",
    "sketches/scatterplot_2040.png"
]
scatterplot_index = 0

WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gamepad Chart Selector")

selected_chart = None
current_image = "all_charts"

# Cooldown settings
joystick_cooldown = 0.3
last_joystick_move = 0

def display_image(image_path):
    try:
        if not os.path.exists(image_path):
            print(f"❌ File not found: {image_path}")
            return
        img = pygame.image.load(image_path).convert_alpha()
        screen.fill((0, 0, 0))
        img = pygame.transform.smoothscale(img, (WIDTH, HEIGHT))
        screen.blit(img, (0, 0))
        pygame.display.flip()
    except pygame.error as e:
        print(f"Error loading image {image_path}: {e}")

# Show all_charts on startup
display_image(images[current_image])

# Gamepad setup
pygame.joystick.init()
if pygame.joystick.get_count() == 0:
    print("No gamepad detected.")
    sys.exit()
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Main loop
running = True
while running:
    current_time = pygame.time.get_ticks() / 1000  # seconds

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        elif event.type == JOYBUTTONDOWN:
            # Confirm selection with X (button 0)
            if event.button == 0 and selected_chart:
                print(f"✅ Showing: {selected_chart}")
                if selected_chart == "scatterplot":
                    scatterplot_index = 0
                display_image(images[selected_chart])
                current_image = selected_chart

            # D-Pad buttons
            elif event.button == 14:  # Right → bar chart
                selected_chart = "bar_chart"
                display_image(images["bar_chart_selected"])

            elif event.button == 13:  # Left → PCP
                selected_chart = "pcp"
                display_image(images["pcp_selected"])

            elif event.button == 12:  # Down → scatterplot
                selected_chart = "scatterplot"
                display_image(images["scatterplot_selected"])

            elif event.button == 11:  # Up → globe
                selected_chart = "globe"
                display_image(images["globe_selected"])

            # Triangle → Toggle temp/rainfall globe
            elif event.button == 3:
                if selected_chart == "globe":
                    if current_image == "globe":
                        current_image = "rainfall_globe"
                        display_image(images["rainfall_globe"])
                    elif current_image == "rainfall_globe":
                        current_image = "globe"
                        display_image(images["globe"])

            # Circle → Show info when on bar3and6_selected
            elif event.button == 1:
                if selected_chart == "bar_chart" and compare_mode and compare_index == 2:
                    if current_image != "bar3and6_info":
                        display_image(images["bar3and6_info"])
                        current_image = "bar3and6_info"
                    else:
                        display_image(compare_images[2])  # bar3and6_selected
                        current_image = "bar_chart"

    # Right joystick: scroll between bar1–bar9
    if selected_chart == "bar_chart" and current_image == "bar_chart":
        axis_value = joystick.get_axis(2)  # Right stick horizontal
        if abs(axis_value) > 0.5 and (current_time - last_joystick_move > joystick_cooldown):
            if axis_value > 0.5:
                current_bar_index = (current_bar_index + 1) % len(bar_image_paths)
            elif axis_value < -0.5:
                current_bar_index = (current_bar_index - 1) % len(bar_image_paths)

            display_image(bar_image_paths[current_bar_index])
            last_joystick_move = current_time

            # Enable compare mode only when bar3 is selected (index 2)
            compare_mode = (current_bar_index == 2)
            compare_index = 0  # reset compare index on re-enter

    # Left joystick: compare bar3 with 4–7
    if selected_chart == "bar_chart" and current_image == "bar_chart" and compare_mode:
        axis_value = joystick.get_axis(0)  # Left stick horizontal
        if abs(axis_value) > 0.5 and (current_time - last_joystick_move > joystick_cooldown):
            if axis_value > 0.5:
                compare_index = min(compare_index + 1, len(compare_images) - 1)
            elif axis_value < -0.5:
                compare_index = max(compare_index - 1, 0)

            display_image(compare_images[compare_index])
            last_joystick_move = current_time

    # Right joystick: scroll scatterplot years
    if selected_chart == "scatterplot" and current_image == "scatterplot":
        axis_value = joystick.get_axis(2)  # Right stick horizontal
        if abs(axis_value) > 0.5 and (current_time - last_joystick_move > joystick_cooldown):
            if axis_value > 0.5:
                scatterplot_index = min(scatterplot_index + 1, len(scatterplot_years) - 1)
            elif axis_value < -0.5:
                scatterplot_index = max(scatterplot_index - 1, 0)

            display_image(scatterplot_years[scatterplot_index])
            last_joystick_move = current_time

    pygame.display.update()

pygame.quit()
