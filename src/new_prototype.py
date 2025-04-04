import pygame
import sys
import os
from pygame.locals import *

# Set working directory to script location
os.chdir(os.path.dirname(os.path.abspath(__file__)))

pygame.init()

# Load all sketches from 1.jpeg to 44.jpeg
images = {str(i): f"new_sketches/{i}.jpeg" for i in range(1, 45)}

WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sketch Viewer")

# Start with sketch 1
current_image = "1"

def display_image(image_path):
    if not os.path.exists(image_path):
        print(f"\u274c File not found: {image_path}")
        return
    try:
        img = pygame.image.load(image_path).convert_alpha()
        img = pygame.transform.smoothscale(img, (WIDTH, HEIGHT))
        screen.fill((0, 0, 0))
        screen.blit(img, (0, 0))
        pygame.display.flip()
    except pygame.error as e:
        print(f"Error loading image {image_path}: {e}")

display_image(images[current_image])

# Gamepad setup
pygame.joystick.init()
if pygame.joystick.get_count() == 0:
    print("No gamepad detected.")
    sys.exit()
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Track joystick press state
left_stick_pressed = False
right_stick_pressed = False
combo_triggered = False

# Cooldown for analog movements (to avoid rapid fire)
joystick_cooldown = 0.3
last_joystick_move = 0
left_move_registered = False
right_move_registered = False

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    current_time = pygame.time.get_ticks() / 1000

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        elif event.type == JOYBUTTONDOWN:

            if event.button == 0:  # X button
                if current_image == "19":
                    current_image = "20"
                    display_image(images[current_image])
                    print("❌ X button → Showing image 20")
                elif current_image == "35":
                    current_image = "36"
                    display_image(images[current_image])
                    print("❌ X button → Showing image 36")


            elif event.button == 6:  # Options button
                if current_image == "21":
                    current_image = "22"
                    display_image(images[current_image])
                    print("⚙️ Options button → Showing image 22")

            elif event.button == 2:  # Square
                if current_image == "1":
                    current_image = "3"
                elif current_image == "2":
                    current_image = "4"
                elif current_image == "7":
                    current_image = "8"
                elif current_image == "17":
                    current_image = "18"
                elif current_image == "26":
                    current_image = "27"
                elif current_image in ["34", "44"]:
                    current_image = "35"
                if current_image in images:
                    display_image(images[current_image])
                    print(f"🟦 Square → Showing image {current_image}")

            elif event.button == 3:  # Triangle
                if current_image == "12":
                    current_image = "13"
                elif current_image in ["25", "4"]:
                    current_image = "2"
                elif current_image in ["33", "27"]:
                    current_image = "26"
                elif current_image == "43":
                    current_image = "34"
                else:
                    current_image = "1"
                display_image(images[current_image])
                print(f"🔺 Triangle → Showing image {current_image}")

            elif event.button == 11:  # D-Pad UP
                if current_image == "1":
                    current_image = "2"
                elif current_image == "20":
                    current_image = "21"
                elif current_image == "24":
                    current_image = "25"
                display_image(images[current_image])
                print(f"⬆️ D-Pad UP → Showing image {current_image}")

            elif event.button == 12:  # D-Pad DOWN
                if current_image == "13":
                    current_image = "14"
                elif current_image == "22":
                    current_image = "23"
                elif current_image == "30":
                    current_image = "31"
                elif current_image == "26":
                    current_image = "34"
                display_image(images[current_image])
                print(f"⬇️ D-Pad DOWN → Showing image {current_image}")

            elif event.button == 14:  # D-Pad RIGHT
                if current_image == "9":
                    current_image = "10"
                    display_image(images[current_image])
                    print("➡️ D-Pad RIGHT → Showing image 10")
                elif current_image == "18":
                    current_image = "19"
                elif current_image == "2":
                    current_image = "26"
                display_image(images[current_image])
                print(f"➡️ D-Pad RIGHT → Showing image {current_image}")

            elif event.button == 13:  # D-Pad LEFT
                if current_image == "27":
                    current_image = "28"
                    display_image(images[current_image])
                    print("⬅️ D-Pad LEFT → Showing image 28")

            elif event.button == 10:  # R1
                if current_image == "10":
                    current_image = "11"
                    display_image(images[current_image])
                    print("👉 R1 → Showing image 11")
                elif current_image == "29":
                    current_image = "30"
                    display_image(images[current_image])
                    print("👉 R1 → Showing image 30")
                    print("👉 R1 → Showing image 11")
                elif current_image == "37":
                    current_image = "36"
                    display_image(images[current_image])
                    print("👉 R1 → Showing image 36")
                elif current_image == "39":
                    current_image = "40"
                    display_image(images[current_image])
                    print("👉 R1 → Showing image 40")


            elif event.button == 7:  # L3
                if current_image == "42":
                   current_image = "43"
                   display_image(images[current_image])
                   print("🎮 L3 → Showing image 43")
                left_stick_pressed = True
                if right_stick_pressed and not combo_triggered:
                    if current_image == "4":
                        current_image = "5"
                    elif current_image == "15":
                        current_image = "16"
                    elif current_image == "16":
                        current_image = "17"
                    elif current_image == "23":
                        current_image = "24"
                    elif current_image == "28":
                        current_image = "29"
                    elif current_image == "31":
                        current_image = "32"
                    elif current_image == "41":
                        current_image = "42"
                        
                    display_image(images[current_image])
                    print(f"🎮 L3 + R3 → Showing image {current_image}")
                    combo_triggered = True

            elif event.button == 8:  # R3
                right_stick_pressed = True
                if current_image == "34" and not left_stick_pressed:
                    current_image = "44"
                    display_image(images[current_image])
                    print("🎮 R3 → Showing image 44")
                    combo_triggered = True
                elif left_stick_pressed and not combo_triggered:
                    if current_image == "4":
                        current_image = "5"
                    elif current_image == "15":
                        current_image = "16"
                    elif current_image == "16":
                        current_image = "17"
                    elif current_image == "23":
                        current_image = "24"
                    elif current_image == "28":
                        current_image = "29"
                    elif current_image == "31":
                        current_image = "32"
                    elif current_image == "36":
                        current_image = "38"
                    elif current_image == "41":
                        current_image = "42"
                    display_image(images[current_image])
                    print(f"🎮 L3 + R3 → Showing image {current_image}")
                    combo_triggered = True

            elif event.button == 9:  # L1
                if current_image == "29":
                    current_image = "30"
                    display_image(images[current_image])
                    print("👈 L1 → Showing image 30")
                elif current_image == "36":
                    current_image = "37"
                    display_image(images[current_image])
                    print("👈 L1 → Showing image 37")
                elif current_image == "38":
                    current_image = "39"
                    display_image(images[current_image])
                    print("👈 L1 → Showing image 39")


            elif event.button == 1:  # Circle
                if current_image == "5":
                    current_image = "6"
                    display_image(images[current_image])
                    print("⭕ Circle → Showing image 6")

        elif event.type == JOYBUTTONUP:
            if event.button == 7:
                left_stick_pressed = False
            elif event.button == 8:
                right_stick_pressed = False
            combo_triggered = False

    r2_value = joystick.get_axis(5)
    if r2_value > 0.5:
        if current_image == "11":
            current_image = "12"
        elif current_image == "40":
            current_image = "41"
        display_image(images[current_image])
        print(f"👉 R2 (axis 5) → Showing image {current_image}")

    left_x = joystick.get_axis(0)
    left_y = joystick.get_axis(1)

    if current_image in ["6", "8"]:
        if left_x < -0.5:
            left_move_registered = True
        if left_move_registered and left_y < -0.5 and (current_time - last_joystick_move > joystick_cooldown):
            if current_image == "6":
                current_image = "7"
            elif current_image == "8":
                current_image = "9"
            display_image(images[current_image])
            print(f"🎮 Left stick LEFT + UP → Showing image {current_image}")
            left_move_registered = False
            last_joystick_move = current_time

    if current_image == "18":
        if left_x > 0.5:
            right_move_registered = True
        if right_move_registered and left_y < -0.5 and (current_time - last_joystick_move > joystick_cooldown):
            current_image = "19"
            display_image(images[current_image])
            print("🎮 Left stick RIGHT + UP → Showing image 19")
            right_move_registered = False
            last_joystick_move = current_time

    if current_image not in ["6", "8"]:
        left_move_registered = False
    if current_image != "18":
        right_move_registered = False

    if current_image == "14" and left_y < -0.5 and (current_time - last_joystick_move > joystick_cooldown):
        current_image = "15"
        display_image(images[current_image])
        print("⬆️ Left stick UP → Showing image 15")
        last_joystick_move = current_time
        last_joystick_move = current_time

    if current_image == "13" and left_x < -0.5 and (current_time - last_joystick_move > joystick_cooldown):
        current_image = "14"
        display_image(images[current_image])
        print("🎮 Left stick LEFT → Showing image 14")
        last_joystick_move = current_time

    if current_image == "32" and left_x < -0.5 and (current_time - last_joystick_move > joystick_cooldown):
        current_image = "33"
        display_image(images[current_image])
        print("🎮 Left stick LEFT → Showing image 33")
        last_joystick_move = current_time

        clock.tick(60)

pygame.quit()