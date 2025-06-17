import pygame
import sys
import os
import re
import subprocess
import runpy
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Window settings
WIDTH, HEIGHT = 1220, 780
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sketch Viewer")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "template")
print(f"🔍 Looking for images in: {IMAGE_DIR}")


# Load and sort .png images with number-based prefixes
images = {}
pattern = re.compile(r"^(\d+)_.*\.png$")

for file in os.listdir(IMAGE_DIR):
    if file.endswith(".png"):
        match = pattern.match(file)
        if match:
            key = os.path.splitext(file)[0]
            images[key] = os.path.join(IMAGE_DIR, file)

# Sort by numeric prefix (before the underscore)
images = dict(sorted(images.items(), key=lambda item: int(item[0].split('_')[0])))

print(f"✅ Loaded {len(images)} images.")

# Start with the first image
current_image = "1_Globe_Start"

# Path to scatterplot building mode script
SCATTER_SCRIPT = os.path.abspath(os.path.join(BASE_DIR, "scatter_dynamic_demoV6.py"))
BAR_CHART_SCRIPT = os.path.abspath(os.path.join(BASE_DIR, "bar_chart_dynamicV3.py"))

def run_scatter_dynamic_demo():
    """Run the scatter plot building mode script in the same process."""
    try:
        runpy.run_path(SCATTER_SCRIPT, run_name="__main__")
    except SystemExit:
        pass
    except Exception as e:
        print(f"Error running scatter plot demo: {e}")
    finally:
        global screen
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Sketch Viewer")

def run_bar_chart_dynamic():
    """Run the bar chart dynamic script in the same process."""
    try:
        runpy.run_path(BAR_CHART_SCRIPT, run_name="__main__")
    except SystemExit:
        pass
    except Exception as e:
        print(f"Error running bar chart demo: {e}")
    finally:
        global screen
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Sketch Viewer")

# Function to display an image
def display_image(image_key):
    image_path = images.get(image_key)
    if not image_path or not os.path.exists(image_path):
        print(f"❌ File not found: {image_path}")
        return
    try:
        img = pygame.image.load(image_path).convert_alpha()
        img = pygame.transform.smoothscale(img, (WIDTH, HEIGHT))
        screen.fill((0, 0, 0))
        screen.blit(img, (0, 0))

        # Show hint for entering the dynamic/adaptive mode
        lower_key = image_key.lower()
        if "scatterplot" in lower_key or "bar" in lower_key:
            font = pygame.font.SysFont(None, 28)
            hint = font.render("Share-Button to start and end dynamic mode", True, (255, 255, 255))

            overlay_height = 40
            overlay = pygame.Surface((WIDTH, overlay_height))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            overlay_rect = overlay.get_rect(bottomleft=(0, HEIGHT))

            screen.blit(overlay, overlay_rect)
            hint_rect = hint.get_rect(center=(WIDTH // 2, HEIGHT - overlay_height // 2))
            screen.blit(hint, hint_rect)

        pygame.display.flip()
    except pygame.error as e:
        print(f"Error loading image {image_path}: {e}")

# Show the initial image
display_image(current_image)

NAVIGATION_MAP = {
    "1_Globe_Start": { 
        "TRIANGLE": "2_Globe_Selected",
        "DPAD_RIGHT": "7_Scatterplot_Start",
        "DPAD_UP": "39_PCP_1",
        "DPAD_DOWN": "80_Bar"
    },
    "2_Globe_Selected": { 
        "TRIANGLE": "1_Globe_Start",
        "RIGHT_STICK_RIGHT": "3_Globe_Selected_Long45",
        "LEFT_STICK_RIGHT": "5_Globe_Selected_Year2060"
    },
    "3_Globe_Selected_Long45": { 
        "RIGHT_STICK_RIGHT": "4_Globe_Selected_Long90",
        "RIGHT_STICK_LEFT": "2_Globe_Selected",
        "TRIANGLE": "1_Globe_Start"
    },
    "4_Globe_Selected_Long90": { 
        "RIGHT_STICK_LEFT": "3_Globe_Selected_Long45",
        "TRIANGLE": "1_Globe_Start"
    },
    "5_Globe_Selected_Year2060": { 
        "LEFT_STICK_RIGHT": "6_Globe_Selected_Year2099",
        "LEFT_STICK_LEFT": "2_Globe_Selected",
        "TRIANGLE": "1_Globe_Start"
    },
    "6_Globe_Selected_Year2099": { 
        "LEFT_STICK_LEFT": "5_Globe_Selected_Year2060",
        "TRIANGLE": "1_Globe_Start"
    },

    "7_Scatterplot_Start": { 
        "DPAD_RIGHT": "1_Globe_Start",
        "DPAD_UP": "39_PCP_1",
        "DPAD_DOWN": "80_Bar",
        "TRIANGLE": "8_Scatterplot_Selected"
    },

    "8_Scatterplot_Selected": { 
        "TRIANGLE": "7_Scatterplot_Start",
        "LEFT_STICK_RIGHT": "9_Scatterplot_Selected_Year2060",
        "L3_R3": "11_Scatterplot_BuildingMode_1"
    },
    "9_Scatterplot_Selected_Year2060": { 
        "LEFT_STICK_RIGHT": "10_Scatterplot_Selected_Year2099",
        "LEFT_STICK_LEFT": "8_Scatterplot_Selected",
        "L3_R3": "11_Scatterplot_BuildingMode_1",
        "TRIANGLE": "7_Scatterplot_Start"
    },
    "10_Scatterplot_Selected_Year2099": { 
        "LEFT_STICK_LEFT": "9_Scatterplot_Selected_Year2060",
        "L3_R3": "11_Scatterplot_BuildingMode_1",
        "TRIANGLE": "7_Scatterplot_Start"
    },
    "11_Scatterplot_BuildingMode_1": { 
        "CIRCLE": "12_Scatterplot_BuildingMode_1_Circle_Object_1",
        "L3_R3": "8_Scatterplot_Selected"
    },
    "12_Scatterplot_BuildingMode_1_Circle_Object_1": {  
        "LEFT_STICK_LEFT_THEN_UP": "13_Scatterplot_BuildingMode_1_Circle_Object_2"
    },
    "13_Scatterplot_BuildingMode_1_Circle_Object_2": {
        "L3": "14_Scatterplot_BuildingMode_1_Circle_Object_Committed"
    },
    "14_Scatterplot_BuildingMode_1_Circle_Object_Committed": {
        "SQUARE": "15_Scatterplot_BuildingMode_1_Square_Object_1"
    },

    "15_Scatterplot_BuildingMode_1_Square_Object_1": { 
        "LEFT_STICK_LEFT_THEN_UP": "16_Scatterplot_BuildingMode_Square_Object_2"
    },
    "16_Scatterplot_BuildingMode_Square_Object_2": {
        "DPAD_RIGHT": "17_Scatterplot_BuildingMode_1_Square_Object_3"
    },
    "17_Scatterplot_BuildingMode_1_Square_Object_3": {
        "RIGHT_STICK_RIGHT": "18_Scatterplot_BuildingMode_1_Square_Object_4"
    },

    "18_Scatterplot_BuildingMode_1_Square_Object_4": {
        "R1": "19_Scatterplot_BuildingMode_1_Square_Object_5"
    },
    "19_Scatterplot_BuildingMode_1_Square_Object_5": {
        "L1": "18_Scatterplot_BuildingMode_1_Square_Object_4",
        "L3": "20_Scatterplot_BuildingMode_1_Square_Object_Committed"
    },
    "20_Scatterplot_BuildingMode_1_Square_Object_Committed": {
        "TRIANGLE": "21_Scatterplot_BuildingMode_1_Triangle_Object_1"
    },
    "21_Scatterplot_BuildingMode_1_Triangle_Object_1": { 
        "LEFT_STICK_LEFT_THEN_UP": "22_Scatterplot_BuildingMode_1_Triangle_Object_2"
    },
    "22_Scatterplot_BuildingMode_1_Triangle_Object_2": {
        "R3": "23_Scatterplot_BuildingMode_1_Triangle_Object_2"
    },
     "23_Scatterplot_BuildingMode_1_Triangle_Object_2": { 
        "L3": "24_Scatterplot_BuildingMode_1_Triangle_Object_Committed"
    },
      "24_Scatterplot_BuildingMode_1_Triangle_Object_Committed": { 
        "L3_R3": "25_Scatterplot_2"
    },
    "25_Scatterplot_2": {
        "L3_R3": "26_Scatterplot_BuildingMode_2"
    },
    "26_Scatterplot_BuildingMode_2": {
        "X": "27_Scatterplot_BuildingMode_2_Plus_Object_1"
    },
    "27_Scatterplot_BuildingMode_2_Plus_Object_1": {
        "LEFT_STICK_DOWN": "28_Scatterplot_BuildingMode_2_Plus_Object_1"
    },
    "28_Scatterplot_BuildingMode_2_Plus_Object_1": {
        "L3": "29_Scatterplot_BuildingMode_2_Plus_Object_Committed"
    },
    "29_Scatterplot_BuildingMode_2_Plus_Object_Committed": {
        "SQUARE": "30_Scatterplot_BuildingMode_2_Square_Object_1"
    },
    "30_Scatterplot_BuildingMode_2_Square_Object_1": {
        "LEFT_STICK_RIGHT": "31_Scatterplot_BuildingMode_2_Square_Object_2"
    },
    "31_Scatterplot_BuildingMode_2_Square_Object_2": {
        "DPAD_DOWN": "32_Scatterplot_BuildingMode_2_Plus_Object_3"
    },
    "32_Scatterplot_BuildingMode_2_Plus_Object_3": {
        "OPTIONS": "33_Scatterplot_BuildingMode_2_Plus_Object_3",
        "DPAD_UP": "31_Scatterplot_BuildingMode_2_Square_Object_2"
    },
    "33_Scatterplot_BuildingMode_2_Plus_Object_3": {
        "DPAD_UP": "34_Scatterplot_BuildingMode_2_Square_Object_3"
    },
    "34_Scatterplot_BuildingMode_2_Square_Object_3": {
        "L3_R3": "35_Scatterplot_3"
    },
    "35_Scatterplot_3": {
        "DPAD_DOWN": "36_Scatterplot_4"
    },
    "36_Scatterplot_4": {
        "X": "37_Scatterplot_5"
    },
    "37_Scatterplot_5": {
        "TRIANGLE": "7_Scatterplot_Start"
    },
    "39_PCP_1": { 
        "DPAD_RIGHT": "1_Globe_Start",
        "DPAD_UP": "7_Scatterplot_Start",
        "DPAD_DOWN": "80_Bar",
        "TRIANGLE": "40_PCP_2"
    },
    "40_PCP_2": {
        "LEFT_STICK_RIGHT": "41_PCP_Year_2040",
        "TRIANGLE": "39_PCP_1",
        "L2": "43_PCP_Swapping_1",
    },
    "41_PCP_Year_2040": {
        "LEFT_STICK_RIGHT": "42_PCP_Year_2099",
        "LEFT_STICK_LEFT": "40_PCP_2",
        "TRIANGLE": "39_PCP_1"
        #"L2": "43_PCP_Swapping_1"
    },
    "42_PCP_Year_2099": {
        "LEFT_STICK_LEFT": "41_PCP_Year_2040",
        "TRIANGLE": "39_PCP_1"
        #"L2": "43_PCP_Swapping_1"
    },
    "43_PCP_Swapping_1": {
        "CIRCLE_L1": "44_PCP_Swapping_2",
        "RIGHT_STICK_UP": "48_PCP_Axis1_Scaled_1",
        "TRIANGLE": "39_PCP_1"
    },

    "44_PCP_Swapping_2": {
        "L2": "45_PCP_Swapping_3",
        "TRIANGLE": "39_PCP_1"
    },
    "45_PCP_Swapping_3": {
        "L2": "44_PCP_Swapping_2",
        "CIRCLE_L1": "40_PCP_2", #43 is the same as 47
        "TRIANGLE": "39_PCP_1"
    },
    "48_PCP_Axis1_Scaled_1": {
        "L1": "49_PCP_Axis1_Scaled_2",
        "TRIANGLE": "39_PCP_1"
    },
    "49_PCP_Axis1_Scaled_2": {
        "RIGHT_STICK_UP": "50_PCP_Axes1_and_2_Scaled_1",
        "TRIANGLE": "39_PCP_1"
    },
    "50_PCP_Axes1_and_2_Scaled_1": {
        "L2": "51_PCP_Axes1_and_2_Scaled_1"
    },
    "51_PCP_Axes1_and_2_Scaled_1": {
        "L3_R3": "52_PCP_Intervalmode_0"
    },
    "52_PCP_Intervalmode_0": {
        "SQUARE": "53_PCP_Intervalmode_1"
    },
    "53_PCP_Intervalmode_1": {
        "L2": "54_PCP_Intervalmode_2_enlarge"
    },
    "54_PCP_Intervalmode_2_enlarge": {
        "R1": "55_PCP_Intervalmode_3_enlarge",
        "L1": "53_PCP_Intervalmode_1"
    },
    "55_PCP_Intervalmode_3_enlarge": {
        "R2": "54_PCP_Intervalmode_2_enlarge",
        "LEFT_STICK_DOWN": "56_PCP_Intervalmode_4_shiftinterval_1"
    },
    "56_PCP_Intervalmode_4_shiftinterval_1": {
        "L3": "57_PCP_Intervalmode_4_Snapmode_next_Point"
    },
    "57_PCP_Intervalmode_4_Snapmode_next_Point": {
        "R1": "58_PCP_Intervalmode_5_Snapmode_next_point"
    },
    "58_PCP_Intervalmode_5_Snapmode_next_point": {
        "L3": "59_PCP_Intervalmode_5_Snapmode_next_axis_point"
    },
    "59_PCP_Intervalmode_5_Snapmode_next_axis_point": {
        "L2": "60_PCP_Intervalmode_6_snapmode_next_axis_point"
    },
    "60_PCP_Intervalmode_6_snapmode_next_axis_point": {
        "R3": "61_PCP_Intervalmode_X_Invert_Interval"
    },
    "61_PCP_Intervalmode_X_Invert_Interval": {
        "OPTIONS": "62_PCP_Quickselect_Big"
    },
    "62_PCP_Quickselect_Big": {
        "L3_R3": "63_PCP_Selected_Quickselect_big"
    },
    "63_PCP_Selected_Quickselect_big": {
        "X": "64_PCP_Quickselect_big",
        "TRIANGLE": "39_PCP_1"
    },
    "64_PCP_Quickselect_big": {
        "X_L2": "65_PCP_Quickselect_big" 
    },
    "65_PCP_Quickselect_big": {
        "X_R1": "66_PCP_Quickselect_big_Enlarge"
    },
    "66_PCP_Quickselect_big_Enlarge": {
        "X_RELEASE": "67_PCP_Quickselect_big"
    },
    "67_PCP_Quickselect_big": {
        "SQUARE": "68_PCP_Quickselect_small_1" 
    },
    "68_PCP_Quickselect_small_1": {
        "SQUARE_L2": "69_PCP_Quickselect_small_2"
    },
    "69_PCP_Quickselect_small_2": {
        "SQUARE_LEFT_STICK_DOWN": "70_PCP_Quickselect_small_3"
    },
    "70_PCP_Quickselect_small_3": {
        "SQUARE_R1": "71_PCP_Quickselect_small_4"
    },

    "71_PCP_Quickselect_small_4": {
        "SQUARE_RELEASE": "72_PCP_Quickselect_small_5"
    },
    "72_PCP_Quickselect_small_5": {
        "L2": "73_PCP_Quickselect_small_6" 
    },
    "73_PCP_Quickselect_small_6": {
        "L3_R3": "74_PCP_Quickselect_small_7"
    },
    "74_PCP_Quickselect_small_7": {
        "DPAD_DOWN": "75_PCP_Quickselect_small_8"
    },

    "75_PCP_Quickselect_small_8": {
        "DPAD_UP": "76_PCP_Quickselect_small_9"
    },
    "76_PCP_Quickselect_small_9": {
        "OPTIONS": "77_PCP_Quickselect_small_10",
        "DPAD_DOWN": "75_PCP_Quickselect_small_8"
    },
    "77_PCP_Quickselect_small_10": {
        "L3_R3": "78_PCP_Quickselect_small_11"
    },
    "78_PCP_Quickselect_small_11": {
        "TRIANGLE": "39_PCP_1"
    },
    "80_Bar": { 
        "DPAD_RIGHT": "1_Globe_Start",
        "DPAD_UP": "7_Scatterplot_Start",
        "DPAD_DOWN": "39_PCP_1",
        "TRIANGLE": "81_Bar_Selected"
    },
    "81_Bar_Selected": {
        "TRIANGLE": "80_Bar",
        "L3": "82_Bar_Sync_1",
        "TRIANGLE": "80_Bar"
    },
    "82_Bar_Sync_1": {
        "LEFT_STICK_RIGHT": "83_Bar_Sync_2",
        "TRIANGLE": "80_Bar"
    },
    "83_Bar_Sync_2": {
        "LEFT_STICK_RIGHT": "84_Bar_Sync_3",
        "LEFT_STICK_LEFT": "82_Bar_Sync_1",
        "TRIANGLE": "80_Bar"
    },
    "84_Bar_Sync_3": {
        "LEFT_STICK_LEFT": "83_Bar_Sync_2",
        "LEFT_STICK_RIGHT": "85_Bar_Sync_4",
        "TRIANGLE": "80_Bar"
    },
    "85_Bar_Sync_4": {
        "LEFT_STICK_LEFT": "84_Bar_Sync_3",
        "LEFT_STICK_RIGHT": "87_Bar_Sync_6", #85 and 86 are the same image
        "TRIANGLE": "80_Bar"
    },
    "87_Bar_Sync_6": {
        "LEFT_STICK_LEFT": "85_Bar_Sync_4",
        "LEFT_STICK_RIGHT": "88_Bar_Sync_7",
        "TRIANGLE": "80_Bar"
    },
    "88_Bar_Sync_7": {
        "LEFT_STICK_LEFT": "87_Bar_Sync_6",
        "LEFT_STICK_RIGHT": "89_Bar_Sync_8",
        "TRIANGLE": "80_Bar"
    },
    "89_Bar_Sync_8": {
        "LEFT_STICK_LEFT": "88_Bar_Sync_7",
        "LEFT_STICK_RIGHT": "90_Bar_Sync_9",
        "TRIANGLE": "80_Bar"
    },
    "90_Bar_Sync_9": {
        "LEFT_STICK_LEFT": "89_Bar_Sync_8",
        "LEFT_STICK_RIGHT": "91_Bar_Sync_10",
        "TRIANGLE": "80_Bar"
    },
    "91_Bar_Sync_10": {
        "LEFT_STICK_LEFT": "90_Bar_Sync_9",
        "X": "92_Bar_Sync_Selected_1",
        "TRIANGLE": "80_Bar"
    },
    "92_Bar_Sync_Selected_1": {
        "X": "91_Bar_Sync_10",
        "L3_R3": "93_Bar_Sync_IntervalMode_1",
        "TRIANGLE": "80_Bar"
    },
    "93_Bar_Sync_IntervalMode_1": {
        "R1": "94_Bar_Sync_IntervalMode_2"
    },
    "94_Bar_Sync_IntervalMode_2": {
        "L1": "95_Bar_Sync_IntervalMode_3"
    },
    "95_Bar_Sync_IntervalMode_3": {
        "L2": "96_Bar_Sync_IntervalMode_4"
    },
    "96_Bar_Sync_IntervalMode_4": {
        "L3_R3": "97_Bar_Sync"
    },
    "97_Bar_Sync": {
        "R1": "98_Bar_Sync",
        "TRIANGLE": "80_Bar"
    },
    "98_Bar_Sync": {
        "X": "99_Bar_Sync",
        "TRIANGLE": "80_Bar"
    },
    "99_Bar_Sync": {
        "L3_R3": "100_Bar_Sync_IntervalMode_5",
        "TRIANGLE": "80_Bar"
    },
    "100_Bar_Sync_IntervalMode_5": {
        "R3": "101_Bar_Sync_IntervalMode_4"
    },
    "101_Bar_Sync_IntervalMode_4": {
        "L3_R3": "102_Bar_Sync_IntervalMode_4"
    },
    "102_Bar_Sync_IntervalMode_4": {
        "L3": "103_Bar_Sync_IntervalMode_4"
    },
    "103_Bar_Sync_IntervalMode_4": {
        "TRIANGLE": "80_Bar" #80 and 104 are the same
    }
}

# Gamepad setup
pygame.joystick.init()
if pygame.joystick.get_count() == 0:
    print("❌ No gamepad detected.")
    sys.exit()
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Joystick cooldown settings
joystick_cooldown = 0.3 
last_joystick_move = 0
left_move_registered = False
right_left_move_registered = False
left_left_move_registered = False
left_stick_pressed = False
right_stick_pressed = False
combo_triggered = False
right_left_registered = False
right_stick_gesture_cooldown = 0.5 
last_right_left_time = 0
r2_triggered = False
l2_triggered = False
right_down_move_registered = False
circle_pressed = False
l1_pressed = False
circle_l1_combo_triggered = False
right_up_move_registered = False
left_down_move_registered = False
x_pressed = False
l2_pressed = False
x_l2_combo_triggered = False
r1_pressed = False
x_r1_combo_triggered = False
square_pressed = False
square_l2_combo_triggered = False
square_left_down_combo_triggered = False
square_r1_combo_triggered = False
left_left_registered = False
last_left_left_time = 0
left_stick_gesture_cooldown = 0.5  





# Main loop
running = True
clock = pygame.time.Clock()

while running:
    current_time = pygame.time.get_ticks() / 1000  # convert to seconds

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        elif event.type == JOYBUTTONDOWN:
            if event.button == 4:
                lower_title = current_image.lower()
                if "scatterplot" in lower_title:
                    run_scatter_dynamic_demo()
                    display_image(current_image)
                elif "bar" in lower_title:
                    run_bar_chart_dynamic()
                    display_image(current_image)

            if event.button == 3:  # 🔺 Triangle
                if current_image in NAVIGATION_MAP and "TRIANGLE" in NAVIGATION_MAP[current_image]:
                    current_image = NAVIGATION_MAP[current_image]["TRIANGLE"]
                    display_image(current_image)
                    print(f"🔺 Triangle → Showing image {current_image}")
                    
            # D-Pad RIGHT       
            if event.button == 14:
                if current_image in NAVIGATION_MAP and "DPAD_RIGHT" in NAVIGATION_MAP[current_image]:
                    current_image = NAVIGATION_MAP[current_image]["DPAD_RIGHT"]
                    display_image(current_image)
                    print(f"➡️ D-Pad RIGHT → Showing image {current_image}")

            # D-Pad UP
            elif event.button == 11:
                if current_image in NAVIGATION_MAP and "DPAD_UP" in NAVIGATION_MAP[current_image]:
                    current_image = NAVIGATION_MAP[current_image]["DPAD_UP"]
                    display_image(current_image)
                    print(f"⬆️ D-Pad UP → Showing image {current_image}")
                    
            # D-Pad DOWN        
            elif event.button == 12:
                if current_image in NAVIGATION_MAP and "DPAD_DOWN" in NAVIGATION_MAP[current_image]:
                    current_image = NAVIGATION_MAP[current_image]["DPAD_DOWN"]
                    display_image(current_image)
                    print(f"⬇️ D-Pad DOWN → Showing image {current_image}")

            


            elif event.button == 7:  # L3
                left_stick_pressed = True
                if right_stick_pressed and not combo_triggered:
                    if current_image in NAVIGATION_MAP and "L3_R3" in NAVIGATION_MAP[current_image]:
                        current_image = NAVIGATION_MAP[current_image]["L3_R3"]
                        display_image(current_image)
                        print(f"🎮 L3 + R3 → Showing image {current_image}")
                        combo_triggered = True

                elif not right_stick_pressed:  # handle solo L3
                    if current_image in NAVIGATION_MAP and "L3" in NAVIGATION_MAP[current_image]:
                        current_image = NAVIGATION_MAP[current_image]["L3"]
                        display_image(current_image)
                        print(f"🎮 L3 → Showing image {current_image}")
                        
                        
            elif event.button == 8:  # R3
                right_stick_pressed = True
                if left_stick_pressed and not combo_triggered:
                    if current_image in NAVIGATION_MAP and "L3_R3" in NAVIGATION_MAP[current_image]:
                        current_image = NAVIGATION_MAP[current_image]["L3_R3"]
                        display_image(current_image)
                        print(f"🎮 L3 + R3 → Showing image {current_image}")
                        combo_triggered = True

                # Otherwise, check for solo R3
                elif current_image in NAVIGATION_MAP and "R3" in NAVIGATION_MAP[current_image]:
                    current_image = NAVIGATION_MAP[current_image]["R3"]
                    display_image(current_image)
                    print(f"🎮 R3 → Showing image {current_image}")

            

            elif event.button == 1:  # ⭕ Circle
                circle_pressed = True
                
                # Combo check: Circle + L1
                if l1_pressed and not circle_l1_combo_triggered:
                    if current_image in NAVIGATION_MAP and "CIRCLE_L1" in NAVIGATION_MAP[current_image]:
                        current_image = NAVIGATION_MAP[current_image]["CIRCLE_L1"]
                        display_image(current_image)
                        print(f"⭕ + L1 → Showing image {current_image}")
                        circle_l1_combo_triggered = True
                        
                        
                # Normal Circle action
                elif current_image in NAVIGATION_MAP and "CIRCLE" in NAVIGATION_MAP[current_image]:
                    current_image = NAVIGATION_MAP[current_image]["CIRCLE"]
                    display_image(current_image)
                    print(f"⭕ Circle → Showing image {current_image}")



            elif event.button == 2:  # 🟦 Square
                square_pressed = True

            # Combo: SQUARE + R1
                if r1_pressed and not square_r1_combo_triggered:
                    if current_image in NAVIGATION_MAP and "SQUARE_R1" in NAVIGATION_MAP[current_image]:
                        current_image = NAVIGATION_MAP[current_image]["SQUARE_R1"]
                        display_image(current_image)
                        print(f"🟦 + R1 → Showing image {current_image}")
                        square_r1_combo_triggered = True

            # Solo Square
                elif current_image in NAVIGATION_MAP and "SQUARE" in NAVIGATION_MAP[current_image]:
                    current_image = NAVIGATION_MAP[current_image]["SQUARE"]
                    display_image(current_image)
                    print(f"🟦 Square → Showing image {current_image}")





            elif event.button == 0:  # X
                x_pressed = True
                if l2_pressed and not x_l2_combo_triggered:
                    if current_image in NAVIGATION_MAP and "X_L2" in NAVIGATION_MAP[current_image]:
                        current_image = NAVIGATION_MAP[current_image]["X_L2"]
                        display_image(current_image)
                        print(f"✖️ + L2 → Showing image {current_image}")
                        x_l2_combo_triggered = True

                elif r1_pressed and not x_r1_combo_triggered:
                    if current_image in NAVIGATION_MAP and "X_R1" in NAVIGATION_MAP[current_image]:
                        current_image = NAVIGATION_MAP[current_image]["X_R1"]
                        display_image(current_image)
                        print(f"✖️ + R1 → Showing image {current_image}")
                        x_r1_combo_triggered = True

                elif current_image in NAVIGATION_MAP and "X" in NAVIGATION_MAP[current_image]:
                    current_image = NAVIGATION_MAP[current_image]["X"]
                    display_image(current_image)
                    print(f"✖️ X → Showing image {current_image}")



            elif event.button == 9:  # L1
                l1_pressed = True
                
                # Combo check: L1 + Circle
                if circle_pressed and not circle_l1_combo_triggered:
                    if current_image in NAVIGATION_MAP and "CIRCLE_L1" in NAVIGATION_MAP[current_image]:
                        current_image = NAVIGATION_MAP[current_image]["CIRCLE_L1"]
                        display_image(current_image)
                        print(f"⭕ + L1 → Showing image {current_image}")
                        circle_l1_combo_triggered = True
                        
                # Normal L1 action
                elif current_image in NAVIGATION_MAP and "L1" in NAVIGATION_MAP[current_image]:
                    current_image = NAVIGATION_MAP[current_image]["L1"]
                    display_image(current_image)
                    print(f"👈 L1 → Showing image {current_image}")



            elif event.button == 6:  # Options button
                if current_image in NAVIGATION_MAP and "OPTIONS" in NAVIGATION_MAP[current_image]:
                    current_image = NAVIGATION_MAP[current_image]["OPTIONS"]
                    display_image(current_image)
                    print(f"Options → Showing image {current_image}")


            elif event.button == 10:  # R1
                r1_pressed = True
                if x_pressed and not x_r1_combo_triggered:
                    if current_image in NAVIGATION_MAP and "X_R1" in NAVIGATION_MAP[current_image]:
                        current_image = NAVIGATION_MAP[current_image]["X_R1"]
                        display_image(current_image)
                        print(f"✖️ + R1 → Showing image {current_image}")
                        x_r1_combo_triggered = True

                # Combo: SQUARE + R1
                elif square_pressed and not square_r1_combo_triggered:
                    if current_image in NAVIGATION_MAP and "SQUARE_R1" in NAVIGATION_MAP[current_image]:
                        current_image = NAVIGATION_MAP[current_image]["SQUARE_R1"]
                        display_image(current_image)
                        print(f"🟦 + R1 → Showing image {current_image}")
                        square_r1_combo_triggered = True

                # Solo R1 action
                elif current_image in NAVIGATION_MAP and "R1" in NAVIGATION_MAP[current_image]:
                    current_image = NAVIGATION_MAP[current_image]["R1"]
                    display_image(current_image)
                    print(f"R1 → Showing image {current_image}")

                    





        elif event.type == JOYBUTTONUP:
            if event.button == 7:
                left_stick_pressed = False
            elif event.button == 8:
                right_stick_pressed = False
            combo_triggered = False

            if event.button == 1:
                circle_pressed = False
            elif event.button == 9:
                l1_pressed = False
            elif event.button == 0:
                x_pressed = False
                x_l2_combo_triggered = False
                x_r1_combo_triggered = False  # reset

                if current_image in NAVIGATION_MAP and "X_RELEASE" in NAVIGATION_MAP[current_image]:
                    current_image = NAVIGATION_MAP[current_image]["X_RELEASE"]
                    display_image(current_image)
                    print(f"✖️ Released → Showing image {current_image}")

            elif event.button == 10:
                r1_pressed = False
            
            elif event.button == 2:
                square_pressed = False
                square_l2_combo_triggered = False
                square_r1_combo_triggered = False
                square_left_down_combo_triggered = False

                if current_image in NAVIGATION_MAP and "SQUARE_RELEASE" in NAVIGATION_MAP[current_image]:
                    current_image = NAVIGATION_MAP[current_image]["SQUARE_RELEASE"]
                    display_image(current_image)
                    print(f"🟦 Released → Showing image {current_image}")

            if left_stick_y < 0.3:
                left_down_move_registered = False
                square_left_down_combo_triggered = False 
                
            circle_l1_combo_triggered = False




    # Detect right stick right movement (axis 2)
    right_stick_x = joystick.get_axis(2)
    right_stick_y = joystick.get_axis(3)

    if right_stick_x > 0.5 and (current_time - last_joystick_move > joystick_cooldown):
        if current_image in NAVIGATION_MAP and "RIGHT_STICK_RIGHT" in NAVIGATION_MAP[current_image]:
            current_image = NAVIGATION_MAP[current_image]["RIGHT_STICK_RIGHT"]
            display_image(current_image)
            print(f"🎮 Right Stick RIGHT → Showing image {current_image}")
            last_joystick_move = current_time

        # Detect right stick left movement (axis 2)
    if right_stick_x < -0.5 and not right_left_move_registered and (current_time - last_joystick_move > joystick_cooldown):
        if current_image in NAVIGATION_MAP and "RIGHT_STICK_LEFT" in NAVIGATION_MAP[current_image]:
            current_image = NAVIGATION_MAP[current_image]["RIGHT_STICK_LEFT"]
            display_image(current_image)
            print(f"🎮 Right Stick LEFT → Showing image {current_image}")
            last_joystick_move = current_time
            right_left_move_registered = True
            
        # Reset the left move flag when stick returns to center
    if right_stick_x > -0.3:
        right_left_move_registered = False


    # Right Stick Gesture: LEFT then UP
    if right_stick_x < -0.5 and not right_left_registered and (current_time - last_joystick_move > joystick_cooldown):
        right_left_registered = True
        last_right_left_time = current_time
        print("✅ Right stick LEFT registered, waiting for UP...")

    # Step 2: Detect UP after LEFT within cooldown window
    if right_left_registered and right_stick_y < -0.5 and (current_time - last_right_left_time < right_stick_gesture_cooldown):
        if current_image in NAVIGATION_MAP and "RIGHT_STICK_LEFT_THEN_UP" in NAVIGATION_MAP[current_image]:
            current_image = NAVIGATION_MAP[current_image]["RIGHT_STICK_LEFT_THEN_UP"]
            display_image(current_image)
            print(f"🎮 Right Stick LEFT + UP → Showing image {current_image}")
            right_left_registered = False
            last_joystick_move = current_time

    # Reset if no UP follows LEFT in time
    if current_time - last_right_left_time >= right_stick_gesture_cooldown:
        right_left_registered = False

    # Detect RIGHT STICK DOWN
    if right_stick_y > 0.5 and not right_down_move_registered and (current_time - last_joystick_move > joystick_cooldown):
        if current_image in NAVIGATION_MAP and "RIGHT_STICK_DOWN" in NAVIGATION_MAP[current_image]:
            current_image = NAVIGATION_MAP[current_image]["RIGHT_STICK_DOWN"]
            display_image(current_image)
            print(f"🎮 Right Stick DOWN → Showing image {current_image}")
            last_joystick_move = current_time
            right_down_move_registered = True

    # Reset the flag when stick returns to neutral
    if right_stick_y < 0.3:
        right_down_move_registered = False


    # Detect RIGHT STICK UP
    if right_stick_y < -0.5 and not right_up_move_registered and (current_time - last_joystick_move > joystick_cooldown):
        if current_image in NAVIGATION_MAP and "RIGHT_STICK_UP" in NAVIGATION_MAP[current_image]:
            current_image = NAVIGATION_MAP[current_image]["RIGHT_STICK_UP"]
            display_image(current_image)
            print(f"🎮 Right Stick UP → Showing image {current_image}")
            last_joystick_move = current_time
            right_up_move_registered = True

    # Reset when stick returns to neutral
    if right_stick_y > -0.3:
        right_up_move_registered = False


    clock.tick(60)

    # Detect left stick right movement (axis 0)
    left_stick_x = joystick.get_axis(0)
    left_stick_y = joystick.get_axis(1)

    if left_stick_x > 0.5 and not left_move_registered and (current_time - last_joystick_move > joystick_cooldown):
        if current_image in NAVIGATION_MAP and "LEFT_STICK_RIGHT" in NAVIGATION_MAP[current_image]:
            current_image = NAVIGATION_MAP[current_image]["LEFT_STICK_RIGHT"]
            display_image(current_image)
            print(f"🎮 Left Stick RIGHT → Showing image {current_image}")
            last_joystick_move = current_time
            left_move_registered = True
            
            
    # Reset the flag when the stick returns to center
    if left_stick_x < 0.3:
        left_move_registered = False


    # Detect left stick left movement (axis 0)
    if left_stick_x < -0.5 and not left_left_move_registered and (current_time - last_joystick_move > joystick_cooldown):
        if current_image in NAVIGATION_MAP and "LEFT_STICK_LEFT" in NAVIGATION_MAP[current_image]:
            current_image = NAVIGATION_MAP[current_image]["LEFT_STICK_LEFT"]
            display_image(current_image)
            print(f"🎮 Left Stick LEFT → Showing image {current_image}")
            last_joystick_move = current_time
            left_left_move_registered = True

    # Reset the left move flag when stick returns to center
    if left_stick_x > -0.3:
        left_left_move_registered = False

    # Step 1: Detect LEFT STICK LEFT as the beginning of the gesture
    if left_stick_x < -0.5 and not left_left_registered and (current_time - last_joystick_move > joystick_cooldown):
        left_left_registered = True
        last_left_left_time = current_time
        print("✅ Left stick LEFT registered, waiting for UP...")

    # Step 2: Detect UP within time window to complete gesture
    if left_left_registered and left_stick_y < -0.5 and (current_time - last_left_left_time < left_stick_gesture_cooldown):
        if current_image in NAVIGATION_MAP and "LEFT_STICK_LEFT_THEN_UP" in NAVIGATION_MAP[current_image]:
            current_image = NAVIGATION_MAP[current_image]["LEFT_STICK_LEFT_THEN_UP"]
            display_image(current_image)
            print(f"🎮 Left Stick LEFT + UP → Showing image {current_image}")
            last_joystick_move = current_time
        left_left_registered = False  # Reset after gesture

    # Timeout reset if UP not followed in time
    if current_time - last_left_left_time >= left_stick_gesture_cooldown:
        left_left_registered = False



    # Detect LEFT STICK DOWN
    if left_stick_y > 0.5 and not left_down_move_registered and (current_time - last_joystick_move > joystick_cooldown):
        left_down_move_registered = True

       # Combo: SQUARE + Left Stick Down
        if square_pressed and not square_left_down_combo_triggered:
            if current_image in NAVIGATION_MAP and "SQUARE_LEFT_STICK_DOWN" in NAVIGATION_MAP[current_image]:
                current_image = NAVIGATION_MAP[current_image]["SQUARE_LEFT_STICK_DOWN"]
                display_image(current_image)
                print(f"🟦 + 🎮 Left Stick DOWN → Showing image {current_image}")
                square_left_down_combo_triggered = True
                last_joystick_move = current_time
      # Solo action (only if combo didn’t trigger)
        elif current_image in NAVIGATION_MAP and "LEFT_STICK_DOWN" in NAVIGATION_MAP[current_image]:
            current_image = NAVIGATION_MAP[current_image]["LEFT_STICK_DOWN"]
            display_image(current_image)
            print(f"🎮 Left Stick DOWN → Showing image {current_image}")
            last_joystick_move = current_time




    # Detect R2 (axis 5)
    r2_value = joystick.get_axis(5)
    if r2_value > 0.5 and not r2_triggered and (current_time - last_joystick_move > joystick_cooldown):
        if current_image in NAVIGATION_MAP and "R2" in NAVIGATION_MAP[current_image]:
            current_image = NAVIGATION_MAP[current_image]["R2"]
            display_image(current_image)
            print(f"🎮 R2 Trigger → Showing image {current_image}")
            last_joystick_move = current_time
            r2_triggered = True

    # Reset trigger flag when R2 is released
    if r2_value < 0.3:
        r2_triggered = False


    # Detect L2 (axis 4)
    l2_value = joystick.get_axis(4)

    # L2 Solo Trigger
    if l2_value > 0.5 and not l2_triggered and (current_time - last_joystick_move > joystick_cooldown):
        if current_image in NAVIGATION_MAP and "L2" in NAVIGATION_MAP[current_image]:
            current_image = NAVIGATION_MAP[current_image]["L2"]
            display_image(current_image)
            print(f"🎮 L2 Trigger → Showing image {current_image}")
            last_joystick_move = current_time
            l2_triggered = True

    # Track L2 "press" state for combo logic (X + L2)
    if l2_value > 0.5:
        l2_pressed = True
    else:
        l2_pressed = False
        x_l2_combo_triggered = False  # Reset combo flag

    # Reset L2 trigger (solo press) flag
    if l2_value < 0.3:
        l2_triggered = False


    # Combo: X + L2 (regardless of order)
    if x_pressed and l2_pressed and not x_l2_combo_triggered:
        if current_image in NAVIGATION_MAP and "X_L2" in NAVIGATION_MAP[current_image]:
            current_image = NAVIGATION_MAP[current_image]["X_L2"]
            display_image(current_image)
            print(f"✖️ + L2 → Showing image {current_image}")
            last_joystick_move = current_time
            x_l2_combo_triggered = True

    if square_pressed and l2_pressed and not square_l2_combo_triggered:
        if current_image in NAVIGATION_MAP and "SQUARE_L2" in NAVIGATION_MAP[current_image]:
            current_image = NAVIGATION_MAP[current_image]["SQUARE_L2"]
            display_image(current_image)
            print(f"🟦 + L2 → Showing image {current_image}")
            last_joystick_move = current_time
            square_l2_combo_triggered = True



pygame.quit()
