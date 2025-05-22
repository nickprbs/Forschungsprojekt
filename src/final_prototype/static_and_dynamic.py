import pygame
import sys
import os
import re
from pygame.locals import *

def run_static_viewer():
    pygame.init()
    WIDTH, HEIGHT = 1220, 780
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sketch Viewer")

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    IMAGE_DIR = os.path.join(BASE_DIR, "template")

    images = {}
    pattern = re.compile(r"^(\d+)_.*\.png$")
    for file in os.listdir(IMAGE_DIR):
        if file.endswith(".png"):
            match = pattern.match(file)
            if match:
                key = os.path.splitext(file)[0]
                images[key] = os.path.join(IMAGE_DIR, file)
    images = dict(sorted(images.items(), key=lambda item: int(item[0].split('_')[0])))

    def display_image(image_path):
        img = pygame.image.load(image_path).convert_alpha()
        img = pygame.transform.smoothscale(img, (WIDTH, HEIGHT))
        screen.fill((0, 0, 0))
        screen.blit(img, (0, 0))
        pygame.display.flip()

    current_image = "1_Globe_Start"
    display_image(images[current_image])

    NAVIGATION_MAP = {
    "1_Globe_Start": {
        "TRIANGLE": "2_Globe_Selected",
        "DPAD_RIGHT": "7_Scatterplot_Start",
        "DPAD_UP": "35_PCP_1",
        "DPAD_DOWN": "76_Bar"
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
        "DPAD_UP": "35_PCP_1",
        "DPAD_DOWN": "76_Bar",
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
        "L3_R3": "SWITCH_TO_DYNAMIC"
    },
    "12_Scatterplot_BuildingMode_1_Circle_Object_1": {
        "RIGHT_STICK_LEFT_THEN_UP": "13_Scatterplot_BuildingMode_1_Circle_Object_2"
    },
    "13_Scatterplot_BuildingMode_1_Circle_Object_2": {
        "SQUARE": "14_Scatterplot_BuildingMode_1_Square_Object_1"
    },
    "14_Scatterplot_BuildingMode_1_Square_Object_1": {
        "RIGHT_STICK_LEFT_THEN_UP": "15_Scatterplot_BuildingMode_Square_Object_2"
    },
    "15_Scatterplot_BuildingMode_Square_Object_2": {
        "DPAD_RIGHT": "16_Scatterplot_BuildingMode_1_Square_Object_3"
    },
    "16_Scatterplot_BuildingMode_1_Square_Object_3": {
        "LEFT_STICK_RIGHT": "17_Scatterplot_BuildingMode_1_Square_Object_4"
    },
    "17_Scatterplot_BuildingMode_1_Square_Object_4": {
        "R2": "18_Scatterplot_BuildingMode_1_Square_Object_5"
    },
    "18_Scatterplot_BuildingMode_1_Square_Object_5": {
        "L2": "17_Scatterplot_BuildingMode_1_Square_Object_4",
        "TRIANGLE": "19_Scatterplot_BuildingMode_1_Triangle_Object_1"
    },
    "19_Scatterplot_BuildingMode_1_Triangle_Object_1": {
        "RIGHT_STICK_LEFT_THEN_UP": "20_Scatterplot_BuildingMode_1_Triangle_Object_2"
    },
    "20_Scatterplot_BuildingMode_1_Triangle_Object_2": {
        "L3": "21_Scatterplot_BuildingMode_1_Triangle_Object_2"
    },
    "21_Scatterplot_BuildingMode_1_Triangle_Object_2": {
        "L3_R3": "22_Scatterplot_2"
    },
    "22_Scatterplot_2": {
        "L3_R3": "23_Scatterplot_BuildingMode_2"
    },
    "23_Scatterplot_BuildingMode_2": {
        "X": "24_Scatterplot_BuildingMode_2_Plus_Object_1"
    },
    "24_Scatterplot_BuildingMode_2_Plus_Object_1": {
        "RIGHT_STICK_DOWN": "25_Scatterplot_BuildingMode_2_Plus_Object_1"
    },
    "25_Scatterplot_BuildingMode_2_Plus_Object_1": {
        "SQUARE": "26_Scatterplot_BuildingMode_2_Square_Object_1"
    },
    "26_Scatterplot_BuildingMode_2_Square_Object_1": {
        "RIGHT_STICK_RIGHT": "27_Scatterplot_BuildingMode_2_Square_Object_2"
    },
    "27_Scatterplot_BuildingMode_2_Square_Object_2": {
        "L1": "28_Scatterplot_BuildingMode_2_Plus_Object_3"
    },
    "28_Scatterplot_BuildingMode_2_Plus_Object_3": {
        "OPTIONS": "29_Scatterplot_BuildingMode_2_Plus_Object_3",
        "R1": "27_Scatterplot_BuildingMode_2_Square_Object_2"
    },
    "29_Scatterplot_BuildingMode_2_Plus_Object_3": {
        "R1": "30_Scatterplot_BuildingMode_2_Square_Object_3"
    },
    "30_Scatterplot_BuildingMode_2_Square_Object_3": {
        "L3_R3": "31_Scatterplot_3"
    },
    "31_Scatterplot_3": {
        "R1": "32_Scatterplot_4"
    },
    "32_Scatterplot_4": {
        "X": "33_Scatterplot_5"
    },
    "33_Scatterplot_5": {
        "TRIANGLE": "7_Scatterplot_Start"
    },
     "35_PCP_1": {
        "DPAD_RIGHT": "1_Globe_Start",
        "DPAD_UP": "7_Scatterplot_Start",
        "DPAD_DOWN": "76_Bar",
        "TRIANGLE": "36_PCP_2"
    },
    "36_PCP_2": {
        "LEFT_STICK_RIGHT": "37_PCP_Year_2040",
        "TRIANGLE": "35_PCP_1",
        "L2": "39_PCP_Swapping_1",
    },
    "37_PCP_Year_2040": {
        "LEFT_STICK_RIGHT": "38_PCP_Year_2099",
        "LEFT_STICK_LEFT": "36_PCP_2",
        "TRIANGLE": "35_PCP_1",
        "L2": "39_PCP_Swapping_1"
    },
    "38_PCP_Year_2099": {
        "LEFT_STICK_LEFT": "37_PCP_Year_2040",
        "TRIANGLE": "35_PCP_1",
        "L2": "39_PCP_Swapping_1"
    },
    "39_PCP_Swapping_1": {
        "CIRCLE_L1": "40_PCP_Swapping_2",
        "RIGHT_STICK_UP": "44_PCP_Axis1_Scaled_1"
    },
    "40_PCP_Swapping_2": {
        "L2": "41_PCP_Swapping_3"
    },
    "41_PCP_Swapping_3": {
        "L2": "40_PCP_Swapping_2",
        "CIRCLE_L1": "36_PCP_2"
    },
    "44_PCP_Axis1_Scaled_1": {
        "L1": "45_PCP_Axis1_Scaled_2"
    },
    "45_PCP_Axis1_Scaled_2": {
        "RIGHT_STICK_UP": "46_PCP_Axes1_and_2_Scaled_1"
    },
    "46_PCP_Axes1_and_2_Scaled_1": {
        "L2": "47_PCP_Axes1_and_2_Scaled_1"
    },
    "47_PCP_Axes1_and_2_Scaled_1": {
        "L3_R3": "48_PCP_Intervalmode_0"
    },
    "48_PCP_Intervalmode_0": {
        "L3_R3": "49_PCP_Intervalmode_1"
    },
    "49_PCP_Intervalmode_1": {
        "L2": "50_PCP_Intervalmode_2_enlarge"
    },
    "50_PCP_Intervalmode_2_enlarge": {
        "R1": "51_PCP_Intervalmode_3_enlarge",
        "L1": "49_PCP_Intervalmode_1"
    },
    "51_PCP_Intervalmode_3_enlarge": {
        "R2": "50_PCP_Intervalmode_2_enlarge",
        "LEFT_STICK_DOWN": "52_PCP_Intervalmode_4_shiftinterval_1"
    },
    "52_PCP_Intervalmode_4_shiftinterval_1": {
        "L3": "53_PCP_Intervalmode_4_Snapmode_next_Point"
    },
    "53_PCP_Intervalmode_4_Snapmode_next_Point": {
        "R2": "54_PCP_Intervalmode_5_Snapmode_next_point"
    },
    "54_PCP_Intervalmode_5_Snapmode_next_point": {
        "L3": "55_PCP_Intervalmode_5_Snapmode_next_axis_point"
    },
    "55_PCP_Intervalmode_5_Snapmode_next_axis_point": {
        "L1": "56_PCP_Intervalmode_6_snapmode_next_axis_point"
    },
    "56_PCP_Intervalmode_6_snapmode_next_axis_point": {
        "L3": "57_PCP_Intervalmode_X_Invert_Interval"
    },
    "57_PCP_Intervalmode_X_Invert_Interval": {
        "OPTIONS": "58_PCP_Quickselect_Big"
    },
    "58_PCP_Quickselect_Big": {
        "L3_R3": "59_PCP_Selected_Quickselect_big"
    },
    "59_PCP_Selected_Quickselect_big": {
        "L3_R3": "60_PCP_Quickselect_big" #??????
    },
    "60_PCP_Quickselect_big": {
        "X_L2": "61_PCP_Quickselect_big" 
    },
    "61_PCP_Quickselect_big": {
        "X_R1": "62_PCP_Quickselect_big_Enlarge"
    },
    "62_PCP_Quickselect_big_Enlarge": {
        "X_RELEASE": "63_PCP_Quickselect_big"
    },
    "63_PCP_Quickselect_big": {
        "L3_R3": "64_PCP_Quickselect_small" #????
    },
    "64_PCP_Quickselect_small": {
        "SQUARE_L2": "65_PCP_Quickselect_small"
    },
    "65_PCP_Quickselect_small": {
        "SQUARE_LEFT_STICK_DOWN": "66_PCP_Quickselect_small"
    },
    "66_PCP_Quickselect_small": {
        "SQUARE_R1": "67_PCP_Quickselect_small"
    },
    "67_PCP_Quickselect_small": {
        "SQUARE_RELEASE": "68_PCP_Quickselect_small"
    },
    "68_PCP_Quickselect_small": {
        "L2": "69_PCP_Quickselect_small" #????
    },
    "69_PCP_Quickselect_small": {
        "L3_R3": "70_PCP_Quickselect_small"
    },
    "70_PCP_Quickselect_small": {
        "DPAD_DOWN": "71_PCP_Quickselect_small"
    },
    "71_PCP_Quickselect_small": {
        "DPAD_UP": "72_PCP_Quickselect_small"
    },
    "72_PCP_Quickselect_small": {
        "OPTIONS": "73_PCP_Quickselect_small",
        "DPAD_DOWN": "71_PCP_Quickselect_small"
    },
    "73_PCP_Quickselect_small": {
        "L3_R3": "74_PCP_Quickselect_small"
    },
    "74_PCP_Quickselect_small": {
        "TRIANGLE": "35_PCP_1"
    },
    


    "76_Bar": {
        "DPAD_RIGHT": "1_Globe_Start",
        "DPAD_UP": "7_Scatterplot_Start",
        "DPAD_DOWN": "35_PCP_1",
        "TRIANGLE": "77_Bar_Selected"
    },
    "77_Bar_Selected": {
        "TRIANGLE": "76_Bar",
        "R3": "78_Bar_Sync_1"
    },
    "78_Bar_Sync_1": {
        "LEFT_STICK_RIGHT": "79_Bar_Sync_2"
    },
    "79_Bar_Sync_2": {
        "LEFT_STICK_RIGHT": "80_Bar_Sync_3",
        "LEFT_STICK_LEFT": "78_Bar_Sync_1"
    },
    "80_Bar_Sync_3": {
        "LEFT_STICK_LEFT": "79_Bar_Sync_2",
        "LEFT_STICK_RIGHT": "81_Bar_Sync_4"
    },
    "81_Bar_Sync_4": {
        "LEFT_STICK_LEFT": "80_Bar_Sync_3",
        "LEFT_STICK_RIGHT": "83_Bar_Sync_6" #81 and 82 are the same image
    },
    "83_Bar_Sync_6": {
        "LEFT_STICK_LEFT": "81_Bar_Sync_4",
        "LEFT_STICK_RIGHT": "84_Bar_Sync_7" 
    },
    "84_Bar_Sync_7": {
        "LEFT_STICK_LEFT": "83_Bar_Sync_6",
        "LEFT_STICK_RIGHT": "85_Bar_Sync_8" 
    },
    "85_Bar_Sync_8": {
        "LEFT_STICK_LEFT": "84_Bar_Sync_7",
        "LEFT_STICK_RIGHT": "86_Bar_Sync_9" 
    },
    "86_Bar_Sync_9": {
        "LEFT_STICK_LEFT": "85_Bar_Sync_8",
        "LEFT_STICK_RIGHT": "87_Bar_Sync_10" 
    },
    "87_Bar_Sync_10": {
        "LEFT_STICK_LEFT": "86_Bar_Sync_9",
        "X": "88_Bar_Sync_Selected_1"
    },
    "88_Bar_Sync_Selected_1": {
        "X": "87_Bar_Sync_10",
        "L3_R3": "89_Bar_Sync_IntervalMode_1"
    },
    "89_Bar_Sync_IntervalMode_1": {
        "R1": "90_Bar_Sync_IntervalMode_2"
    },
    "90_Bar_Sync_IntervalMode_2": {
        "L1": "91_Bar_Sync_IntervalMode_3"
    },
    "91_Bar_Sync_IntervalMode_3": {
        "L2": "92_Bar_Sync_IntervalMode_4"
    },
    "92_Bar_Sync_IntervalMode_4": {
        "L3_R3": "93_Bar_Sync"
    },
    "93_Bar_Sync": {
        "LEFT_STICK_RIGHT": "94_Bar_Sync_IntervalMode_4"
    }
}

    pygame.joystick.init()
    if pygame.joystick.get_count() == 0:
        print("No gamepad detected.")
        return "quit"
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    combo_triggered = False
    left_stick_pressed = right_stick_pressed = False
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
    
    
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                return "quit"
            elif event.type == JOYBUTTONDOWN:
                if event.button == 7:
                    left_stick_pressed = True
                elif event.button == 8:
                    right_stick_pressed = True


                if left_stick_pressed and right_stick_pressed and not combo_triggered:
                    if current_image in NAVIGATION_MAP and "L3_R3" in NAVIGATION_MAP[current_image]:
                        target = NAVIGATION_MAP[current_image]["L3_R3"]
                        if target == "SWITCH_TO_DYNAMIC":
                            return "switch_to_dynamic"
                        current_image = target
                        display_image(images[current_image])
                        combo_triggered = True

                          # 🎮 Solo L3
                          
                elif event.button == 7 and not right_stick_pressed and not combo_triggered:
                    if current_image in NAVIGATION_MAP and "L3" in NAVIGATION_MAP[current_image]:
                        current_image = NAVIGATION_MAP[current_image]["L3"]
                        display_image(images[current_image])
                        print(f"🎮 L3 → Showing image {current_image}")

    # 🎮 Solo R3
                elif event.button == 8 and not left_stick_pressed and not combo_triggered:
                    if current_image in NAVIGATION_MAP and "R3" in NAVIGATION_MAP[current_image]:
                        current_image = NAVIGATION_MAP[current_image]["R3"]
                        display_image(images[current_image])
                        print(f"🎮 R3 → Showing image {current_image}")


                elif event.type == JOYBUTTONDOWN:
                    if event.button == 3:  # 🔺 Triangle
                        if current_image in NAVIGATION_MAP and "TRIANGLE" in NAVIGATION_MAP[current_image]:
                            current_image = NAVIGATION_MAP[current_image]["TRIANGLE"]
                            display_image(images[current_image])
                            print(f"🔺 Triangle → Showing image {current_image}")
                    
                 # D-Pad RIGHT       
                    if event.button == 14:
                        if current_image in NAVIGATION_MAP and "DPAD_RIGHT" in NAVIGATION_MAP[current_image]:
                            current_image = NAVIGATION_MAP[current_image]["DPAD_RIGHT"]
                            display_image(images[current_image])
                            print(f"➡️ D-Pad RIGHT → Showing image {current_image}")

            # D-Pad UP
                    elif event.button == 11:
                        if current_image in NAVIGATION_MAP and "DPAD_UP" in NAVIGATION_MAP[current_image]:
                            current_image = NAVIGATION_MAP[current_image]["DPAD_UP"]
                            display_image(images[current_image])
                            print(f"⬆️ D-Pad UP → Showing image {current_image}")
                    
            # D-Pad DOWN        
                    elif event.button == 12:
                        if current_image in NAVIGATION_MAP and "DPAD_DOWN" in NAVIGATION_MAP[current_image]:
                            current_image = NAVIGATION_MAP[current_image]["DPAD_DOWN"]
                            display_image(images[current_image])
                            print(f"⬇️ D-Pad DOWN → Showing image {current_image}")

            


                    
                    

            

                    elif event.button == 1:  # ⭕ Circle
                        circle_pressed = True
                
                # Combo check: Circle + L1
                        if l1_pressed and not circle_l1_combo_triggered:
                            if current_image in NAVIGATION_MAP and "CIRCLE_L1" in NAVIGATION_MAP[current_image]:
                                current_image = NAVIGATION_MAP[current_image]["CIRCLE_L1"]
                                display_image(images[current_image])
                                print(f"⭕ + L1 → Showing image {current_image}")
                                circle_l1_combo_triggered = True
                        
                        
                # Normal Circle action
                        elif current_image in NAVIGATION_MAP and "CIRCLE" in NAVIGATION_MAP[current_image]:
                            current_image = NAVIGATION_MAP[current_image]["CIRCLE"]
                            display_image(images[current_image])
                            print(f"⭕ Circle → Showing image {current_image}")



                    elif event.button == 2:  # 🟦 Square
                        square_pressed = True

            # Combo: SQUARE + R1
                        if r1_pressed and not square_r1_combo_triggered:
                            if current_image in NAVIGATION_MAP and "SQUARE_R1" in NAVIGATION_MAP[current_image]:
                                current_image = NAVIGATION_MAP[current_image]["SQUARE_R1"]
                                display_image(images[current_image])
                                print(f"🟦 + R1 → Showing image {current_image}")
                                square_r1_combo_triggered = True

            # Solo Square
                        elif current_image in NAVIGATION_MAP and "SQUARE" in NAVIGATION_MAP[current_image]:
                            current_image = NAVIGATION_MAP[current_image]["SQUARE"]
                            display_image(images[current_image])
                            print(f"🟦 Square → Showing image {current_image}")





                    elif event.button == 0:  # X
                        x_pressed = True
                        if l2_pressed and not x_l2_combo_triggered:
                            if current_image in NAVIGATION_MAP and "X_L2" in NAVIGATION_MAP[current_image]:
                                current_image = NAVIGATION_MAP[current_image]["X_L2"]
                                display_image(images[current_image])
                                print(f"✖️ + L2 → Showing image {current_image}")
                                x_l2_combo_triggered = True

                        elif r1_pressed and not x_r1_combo_triggered:
                            if current_image in NAVIGATION_MAP and "X_R1" in NAVIGATION_MAP[current_image]:
                                current_image = NAVIGATION_MAP[current_image]["X_R1"]
                                display_image(images[current_image])
                                print(f"✖️ + R1 → Showing image {current_image}")
                                x_r1_combo_triggered = True

                        elif current_image in NAVIGATION_MAP and "X" in NAVIGATION_MAP[current_image]:
                            current_image = NAVIGATION_MAP[current_image]["X"]
                            display_image(images[current_image])
                            print(f"✖️ X → Showing image {current_image}")



                    elif event.button == 9:  # L1
                        l1_pressed = True
                
                # Combo check: L1 + Circle
                        if circle_pressed and not circle_l1_combo_triggered:
                            if current_image in NAVIGATION_MAP and "CIRCLE_L1" in NAVIGATION_MAP[current_image]:
                                current_image = NAVIGATION_MAP[current_image]["CIRCLE_L1"]
                                display_image(images[current_image])
                                print(f"⭕ + L1 → Showing image {current_image}")
                                circle_l1_combo_triggered = True
                        
                # Normal L1 action
                        elif current_image in NAVIGATION_MAP and "L1" in NAVIGATION_MAP[current_image]:
                            current_image = NAVIGATION_MAP[current_image]["L1"]
                            display_image(images[current_image])
                            print(f"👈 L1 → Showing image {current_image}")



                        elif event.button == 6:  # Options button
                            if current_image in NAVIGATION_MAP and "OPTIONS" in NAVIGATION_MAP[current_image]:
                                current_image = NAVIGATION_MAP[current_image]["OPTIONS"]
                                display_image(images[current_image])
                                print(f"Options → Showing image {current_image}")


                    elif event.button == 10:  # R1
                        r1_pressed = True
                        if x_pressed and not x_r1_combo_triggered:
                            if current_image in NAVIGATION_MAP and "X_R1" in NAVIGATION_MAP[current_image]:
                                current_image = NAVIGATION_MAP[current_image]["X_R1"]
                                display_image(images[current_image])
                                print(f"✖️ + R1 → Showing image {current_image}")
                                x_r1_combo_triggered = True

                # Combo: SQUARE + R1
                        elif square_pressed and not square_r1_combo_triggered:
                            if current_image in NAVIGATION_MAP and "SQUARE_R1" in NAVIGATION_MAP[current_image]:
                                current_image = NAVIGATION_MAP[current_image]["SQUARE_R1"]
                                display_image(images[current_image])
                                print(f"🟦 + R1 → Showing image {current_image}")
                                square_r1_combo_triggered = True

                # Solo R1 action
                        elif current_image in NAVIGATION_MAP and "R1" in NAVIGATION_MAP[current_image]:
                            current_image = NAVIGATION_MAP[current_image]["R1"]
                            display_image(images[current_image])
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
                            display_image(images[current_image])
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
                            display_image(images[current_image])
                            print(f"🟦 Released → Showing image {current_image}")

                    if left_stick_y < 0.3:
                        left_down_move_registered = False
                        square_left_down_combo_triggered = False 
                
                    circle_l1_combo_triggered = False

        clock.tick(60)

    return "quit"


def run_dynamic_environment():
    import math
    import pygame
    import sys
    import os

    allow_return_to_static = False  # Only enable this after your interaction logic completes

    # Konfiguration
    WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    IMAGE_DIR = os.path.join(BASE_DIR, "template")
    BG_GRAY_PATH = os.path.join(IMAGE_DIR, "bg_gray.png")
    BG_COLOR_PATH = os.path.join(IMAGE_DIR, "bg_color.png")
    SHAPE_INITIAL_SIZE = 100
    MIN_SHAPE_SIZE = 10
    DEADZONE = 0.1
    BASE_MOVE_SPEED = 300
    BASE_SCALE_SPEED = 100
    ROTATION_SPEED = 90
    NODE_MOVE_SPEED = 200
    OUTLINE_WIDTH = 4
    NODE_RADIUS = OUTLINE_WIDTH * 2
    ICON_LIGHTBLUE_COLOR = (50, 50, 255)
    ICON_GRAY_COLOR = (100, 100, 100)
    ICON_RED_COLOR = (255, 0, 0)
    invert = False

    BUTTON_CROSS = 0
    BUTTON_CIRCLE = 1
    BUTTON_SQUARE = 2
    BUTTON_TRIANGLE = 3
    BUTTON_L3 = 7
    BUTTON_L1 = 9
    BUTTON_R1 = 10
    BUTTON_DPAD_RIGHT = 14
    BUTTON_DPAD_LEFT = 13
    BUTTON_R3 = 8
    BUTTON_DPAD_DOWN = 12
    BUTTON_DPAD_UP = 11
    BUTTON_OPTIONS = 6

    AXIS_LS_X, AXIS_LS_Y = 0, 1
    AXIS_RS_X, AXIS_RS_Y = 2, 3
    AXIS_L2, AXIS_R2 = 4, 5

    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    bg_gray = pygame.image.load(BG_GRAY_PATH).convert()
    bg_gray = pygame.transform.scale(bg_gray, (WINDOW_WIDTH, WINDOW_HEIGHT))
    bg_color = pygame.image.load(BG_COLOR_PATH).convert()
    bg_color = pygame.transform.scale(bg_color, (WINDOW_WIDTH, WINDOW_HEIGHT))

    pygame.joystick.init()
    if pygame.joystick.get_count() == 0:
        print("Kein Controller gefunden!")
        sys.exit()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    
    
    active_shape = None
    placed_shapes = []
    placed_regions = []
    placed_icons = []
    editing_index = None     # aktueller Index in placed_shapes
    editing_backup = None    # Backup von region, icon, shape_data
    lock = 0 # for preventing mode-switching
    new_cluster = True

    active_cluster = {
    'placed_shapes': [],
    'placed_regions': [],
    'placed_icons': [],
    }
    clusters = [active_cluster] # Liste von Clustern: [('placed_shapes_cluster0', 'placed_regions_cluster0', 'placed_icons_cluster0'), ...]
    cluster_cursor = 0 
    building_mode = False

    def select_cluster(cluster_cursor):
        global active_cluster, placed_shapes, placed_regions, placed_icons, new_cluster
        if cluster_cursor < len(clusters):
            new_cluster = True if cluster_cursor == 0 else False
            for k, icon in enumerate(clusters[cluster_cursor]['placed_icons']):
                # Get shape data to recreate with new color
                shape_data = clusters[cluster_cursor]['placed_shapes'][k]
                if shape_data['type'] == 'square':
                    new_surface = create_outline('square', shape_data['width'], shape_data['height'], ICON_LIGHTBLUE_COLOR)
                else:
                    new_surface = create_outline(shape_data['type'], shape_data['scale'], None, ICON_LIGHTBLUE_COLOR)
                # Apply rotation
                new_surface = pygame.transform.rotate(new_surface, shape_data['angle'])
                # Replace the surface
                icon['surface'] = new_surface
            for r in clusters[cluster_cursor]['placed_regions']:
                r['surface'].set_alpha(255)
            active_cluster = clusters.pop(cluster_cursor)
            if active_cluster is not None:
                placed_shapes = active_cluster['placed_shapes']
                placed_regions = active_cluster['placed_regions']
                placed_icons = active_cluster['placed_icons']
            # Grau färben aller anderen Cluster 
            for cluster in clusters:
                cluster['visible'] = False
                for k,icon in enumerate(cluster['placed_icons']):
                    # Get shape data to recreate with new color
                    shape_data = cluster['placed_shapes'][k]
                    if shape_data['type'] == 'square':
                        new_surface = create_outline('square', shape_data['width'], shape_data['height'], ICON_GRAY_COLOR)
                    else:
                        new_surface = create_outline(shape_data['type'], shape_data['scale'], None, ICON_GRAY_COLOR)
                    # Apply rotation
                    new_surface = pygame.transform.rotate(new_surface, shape_data['angle'])
                    # Replace the surface
                    icon['surface'] = new_surface
                for r in cluster['placed_regions']:
                    r['surface'].set_alpha(0)
        else:
            active_cluster = None

    # Maske für Formen
    def create_mask(shape_type, width, height=None):
        if height is None:
            height = width
        mask = pygame.Surface((int(width), int(height)), pygame.SRCALPHA)
        if shape_type == 'square':
            # Rechteckige Maske (für Quadrat/Rechteck)
            mask.fill((255,255,255,255))
        elif shape_type == 'circle':
            pygame.draw.ellipse(mask, (255,255,255,255), (0,0,int(width),int(height)))
        elif shape_type == 'triangle':
            h_val = height * math.sqrt(3) / 2
            y = (height - h_val) / 2
            pts = [(width//2, int(y)), (0, int(y+h_val)), (width, int(y+h_val))]
            pygame.draw.polygon(mask, (255,255,255,255), pts)
        elif shape_type == 'plus':
            bar_w = width // 4; c_x = width // 2
            bar_h = height // 4; c_y = height // 2
            pygame.draw.rect(mask, (255,255,255,255), (c_x-bar_w//2, 0, bar_w, height))
            pygame.draw.rect(mask, (255,255,255,255), (0, c_y-bar_h//2, width, bar_h))
        return mask

    # Outline für Formen
    def create_outline(shape_type, width, height=None, color=(0,0,255)):
        if height is None:
            height = width
        surf = pygame.Surface((int(width), int(height)), pygame.SRCALPHA)
        if shape_type == 'square':
            pygame.draw.rect(surf, color, surf.get_rect(), width=OUTLINE_WIDTH)
        elif shape_type == 'circle':
            pygame.draw.ellipse(surf, color, surf.get_rect(), width=OUTLINE_WIDTH)
        elif shape_type == 'triangle':
            h_val = height * math.sqrt(3) / 2
            y = (height - h_val) / 2
            pts = [(width//2, int(y)), (0, int(y+h_val)), (width, int(y+h_val))]
            pygame.draw.polygon(surf, color, pts, width=OUTLINE_WIDTH)
        elif shape_type == 'plus':
            bar_w = width // 4; c_x = width // 2
            bar_h = height // 4; c_y = height // 2
            pygame.draw.rect(surf, color, (c_x-bar_w//2, 0, bar_w, height), width=OUTLINE_WIDTH)
            pygame.draw.rect(surf, color, (0, c_y-bar_h//2, width, bar_h), width=OUTLINE_WIDTH)
        return surf

    # Neues Shape instanziieren
    def spawn_shape(shape_type):
        shape = {'type': shape_type, 'angle': 0}
        if shape_type == 'square':
            shape['width'] = float(SHAPE_INITIAL_SIZE)
            shape['height'] = float(SHAPE_INITIAL_SIZE)
        else:
            shape['scale'] = float(SHAPE_INITIAL_SIZE)
        shape['selected_node'] = 0 
        shape['rect'] = pygame.Rect(0, 0, SHAPE_INITIAL_SIZE, SHAPE_INITIAL_SIZE)
        shape['rect'].center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
        return shape

    # Form festsetzen
    def commit_shape(shape):
        center = shape['rect'].center
        # Erzeuge Maske und Outline
        if shape['type'] == 'square':
            w, h = int(shape['width']), int(shape['height'])
            mask = create_mask('square', w, h)
            outline = create_outline('square', w, h)
        else:
            size = int(shape['scale'])
            mask = create_mask(shape['type'], size)
            outline = create_outline(shape['type'], size)
        mask_r = pygame.transform.rotate(mask, shape['angle'])
        out_r = pygame.transform.rotate(outline, shape['angle'])
        # Region und Icon speichern
        region = pygame.Surface(mask_r.get_size(), pygame.SRCALPHA)
        rect_r = region.get_rect(center=center)
        tmp = pygame.Surface(mask_r.get_size(), pygame.SRCALPHA)
        if invert:
            tmp.blit(bg_gray, (0,0), area=rect_r)
        else:
            tmp.blit(bg_color, (0,0), area=rect_r)
        region.blit(tmp, (0,0))
        region.blit(mask_r, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
        region.blit(out_r, (0,0))
        placed_regions.append({'surface': region, 'rect': rect_r})
        icon = create_outline(shape['type'], w, h, ICON_LIGHTBLUE_COLOR) if shape['type']=='square' else create_outline(shape['type'], size, None, ICON_LIGHTBLUE_COLOR)
        icon_r = pygame.transform.rotate(icon, shape['angle'])
        placed_icons.append({'surface': icon_r, 'rect': icon_r.get_rect(center=center)})
        shape_data = {
            'type':    shape['type'],
            'angle':   shape['angle'],
            'rect_center': center,
            # je nach Form
            **({'width': shape['width'], 'height': shape['height']} if shape['type']=='square' else {'scale': shape['scale']})
        }
        placed_shapes.append(shape_data)

    def select_shape(idx):
        """Holt die Shape-Daten aus placed_* und legt active_shape zum Bearbeiten an."""
        global active_shape, editing_index, editing_backup
        # Backup rausziehen
        editing_index  = idx
        editing_backup = {
            'region': placed_regions.pop(idx),
            'icon':   placed_icons.pop(idx),
            'shape_data': placed_shapes.pop(idx)
        }
        data = editing_backup['shape_data']
        # active_shape neu aufbauen
        active_shape = {'type': data['type'], 'angle': data['angle'], 'selected_node': 0}
        if data['type']=='square':
            active_shape['width']  = float(data['width'])
            active_shape['height'] = float(data['height'])
        else:
            active_shape['scale']  = float(data['scale'])
        # Rect initial position
        w = int(active_shape.get('width', active_shape.get('scale')))
        h = int(active_shape.get('height', active_shape.get('scale')))
        active_shape['rect'] = pygame.Rect(0,0,w,h)
        active_shape['rect'].center = data['rect_center']

    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        if active_shape:
            # Rotation
            if joystick.get_button(BUTTON_L1):
                active_shape['angle'] = (active_shape['angle'] + ROTATION_SPEED * dt) % 360
            if joystick.get_button(BUTTON_R1):
                active_shape['angle'] = (active_shape['angle'] - ROTATION_SPEED * dt) % 360

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.JOYBUTTONDOWN:
                b = event.button
                # Spawns
                if building_mode:
                    if lock == 0 and b in (BUTTON_L3, BUTTON_R3) and joystick.get_button(BUTTON_R3) and joystick.get_button(BUTTON_L3):
                        if active_cluster is not None:
                                # Cluster-Commit
                            if new_cluster:
                                clusters.insert(0, {
                                    'placed_shapes': [],
                                    'placed_regions': [],
                                    'placed_icons': [],
                                    'visible': False
                                })
                            if len(placed_icons) > 0 and len(placed_shapes) > 0 and len(placed_regions) > 0:
                                clusters.append({
                                    'placed_shapes': placed_shapes,
                                    'placed_regions': placed_regions,
                                    'placed_icons': placed_icons,
                                    'visible': False
                                    })
                                for k,icon in enumerate(clusters[len(clusters)-1]['placed_icons']):
                                    # Get shape data to recreate with new color
                                    shape_data = clusters[len(clusters)-1]['placed_shapes'][k]
                                    if shape_data['type'] == 'square':
                                        new_surface = create_outline('square', shape_data['width'], shape_data['height'], ICON_GRAY_COLOR)
                                    else:
                                        new_surface = create_outline(shape_data['type'], shape_data['scale'], None, ICON_GRAY_COLOR)
                                    # Apply rotation
                                    new_surface = pygame.transform.rotate(new_surface, shape_data['angle'])
                                    # Replace the surface
                                    icon['surface'] = new_surface
                                for r in clusters[len(clusters)-1]['placed_regions']:
                                    r['surface'].set_alpha(0)
                            placed_shapes = []
                            placed_regions = []
                            placed_icons = []
                            cluster_cursor = 0
                            active_cluster = None
                            building_mode = False
                            lock == 5
                    if b == BUTTON_SQUARE and not active_shape:
                        active_shape = spawn_shape('square')
                        
                    elif b == BUTTON_CIRCLE and not active_shape:
                        active_shape = spawn_shape('circle')
                    elif b == BUTTON_TRIANGLE and not active_shape:
                        active_shape = spawn_shape('triangle')
                    elif b == BUTTON_CROSS and not active_shape:
                        active_shape = spawn_shape('plus')
                    # Commit
                    elif b == BUTTON_L3 and active_shape:
                        commit_shape(active_shape)
                        active_shape = None
                        invert = False
                        # falls wir gerade eine alte Form editiert haben, Backup auflösen
                        if editing_backup is not None:
                            editing_backup = None
                            editing_index  = None
                    # Node-Iteration
                    elif b == BUTTON_DPAD_RIGHT and active_shape and active_shape['type'] in ('square', 'circle', 'plus'):
                        active_shape['selected_node'] = (active_shape['selected_node'] + 1) % 4
                    elif b == BUTTON_DPAD_LEFT and active_shape and active_shape['type'] in ('square', 'circle', 'plus'):
                        active_shape['selected_node'] = (active_shape['selected_node'] - 1) % 4
                    elif b == BUTTON_DPAD_RIGHT and active_shape and active_shape['type'] == 'triangle':
                        active_shape['selected_node'] = (active_shape['selected_node'] + 1) % 3
                    elif b == BUTTON_DPAD_LEFT and active_shape and active_shape['type'] == 'triangle':
                        active_shape['selected_node'] = (active_shape['selected_node'] - 1) % 3
                    elif b == BUTTON_R3 and active_shape:
                        invert = not invert
                    elif b == BUTTON_DPAD_UP:
                        if active_shape and editing_backup is not None:
                            # aktuelle Edit-Session abbrechen
                            placed_regions.insert(editing_index, editing_backup['region'])
                            placed_icons.insert(editing_index,   editing_backup['icon'])
                            placed_shapes.insert(editing_index,  editing_backup['shape_data'])
                            editing_backup = None
                            # neuen Index berechnen
                            new_idx = (editing_index + 1) % len(placed_shapes)
                            select_shape(new_idx)
                        # 2) normale Selektion (wenn keine Form aktiv)
                        elif active_shape is None and placed_shapes:
                            # beim ersten Mal alte Form (Idx 0), sonst inkremetieren
                            idx0 = 0 if editing_index is None else (editing_index + 1) % len(placed_shapes)
                            select_shape(idx0)
                    elif b == BUTTON_DPAD_DOWN:
                        if active_shape and editing_backup is not None:
                            placed_regions.insert(editing_index, editing_backup['region'])
                            placed_icons.insert(editing_index,   editing_backup['icon'])
                            placed_shapes.insert(editing_index,  editing_backup['shape_data'])
                            editing_backup = None
                            new_idx = (editing_index - 1) % len(placed_shapes)
                            select_shape(new_idx)
                        elif active_shape is None and placed_shapes:
                            idx0 = len(placed_shapes)-1 if editing_index is None else (editing_index - 1) % len(placed_shapes)
                            select_shape(idx0)
                    elif b == BUTTON_OPTIONS and active_shape:
                        # 1) Wenn es eine Edit-Session war, dann alles verwerfen
                        if editing_backup is not None:
                            # Backup nicht zurück einfügen → Hintergrund bleibt weg
                            editing_backup = None
                            editing_index  = None
                            active_shape   = None
                        # 2) Wenn es eine neu gespawnte Form war, einfach abbrechen
                        else:
                            active_shape = None
                            invert = False
                else:
                    if b == BUTTON_DPAD_UP:
                        # Cluster-Iteration
                        for k,icon in enumerate(clusters[cluster_cursor]['placed_icons']):
                            # Get shape data to recreate with new color
                            shape_data = clusters[cluster_cursor]['placed_shapes'][k]
                            if shape_data['type'] == 'square':
                                new_surface = create_outline('square', shape_data['width'], shape_data['height'], ICON_LIGHTBLUE_COLOR if clusters[cluster_cursor]['visible'] else ICON_GRAY_COLOR)
                            else:
                                new_surface = create_outline(shape_data['type'], shape_data['scale'], None, ICON_LIGHTBLUE_COLOR if clusters[cluster_cursor]['visible'] else ICON_GRAY_COLOR)
                            # Apply rotation
                            new_surface = pygame.transform.rotate(new_surface, shape_data['angle'])
                            # Replace the surface
                            icon['surface'] = new_surface

                        cluster_cursor = (cluster_cursor + 1) % len(clusters) 

                        for k,icon in enumerate(clusters[cluster_cursor]['placed_icons']):
                            # Get shape data to recreate with new color
                            shape_data = clusters[cluster_cursor]['placed_shapes'][k]
                            if shape_data['type'] == 'square':
                                new_surface = create_outline('square', shape_data['width'], shape_data['height'], ICON_RED_COLOR)
                            else:
                                new_surface = create_outline(shape_data['type'], shape_data['scale'], None, ICON_RED_COLOR)
                            # Apply rotation
                            new_surface = pygame.transform.rotate(new_surface, shape_data['angle'])
                            # Replace the surface
                            icon['surface'] = new_surface
                        
                        
                    elif b == BUTTON_DPAD_DOWN:
                        # Cluster-Iteration
                        for k,icon in enumerate(clusters[cluster_cursor]['placed_icons']):
                            # Get shape data to recreate with new color
                            shape_data = clusters[cluster_cursor]['placed_shapes'][k]
                            if shape_data['type'] == 'square':
                                new_surface = create_outline('square', shape_data['width'], shape_data['height'], ICON_LIGHTBLUE_COLOR if clusters[cluster_cursor]['visible'] else ICON_GRAY_COLOR)
                            else:
                                new_surface = create_outline(shape_data['type'], shape_data['scale'], None, ICON_LIGHTBLUE_COLOR if clusters[cluster_cursor]['visible'] else ICON_GRAY_COLOR)
                            # Apply rotation
                            new_surface = pygame.transform.rotate(new_surface, shape_data['angle'])
                            # Replace the surface
                            icon['surface'] = new_surface

                        cluster_cursor = (cluster_cursor - 1) % len(clusters)

                        for k,icon in enumerate(clusters[cluster_cursor]['placed_icons']):
                            # Get shape data to recreate with new color
                            shape_data = clusters[cluster_cursor]['placed_shapes'][k]
                            if shape_data['type'] == 'square':
                                new_surface = create_outline('square', shape_data['width'], shape_data['height'], ICON_RED_COLOR)
                            else:
                                new_surface = create_outline(shape_data['type'], shape_data['scale'], None, ICON_RED_COLOR)
                            # Apply rotation
                            new_surface = pygame.transform.rotate(new_surface, shape_data['angle'])
                            # Replace the surface
                            icon['surface'] = new_surface

                    elif b == BUTTON_CROSS:
                        
                        for r in clusters[cluster_cursor]['placed_regions']:
                            r['surface'].set_alpha(0 if clusters[cluster_cursor]['visible'] else 255)
                        clusters[cluster_cursor]['visible'] = not clusters[cluster_cursor]['visible']

                    elif lock == 0 and b in (BUTTON_L3, BUTTON_R3) and joystick.get_button(BUTTON_R3) and joystick.get_button(BUTTON_L3):
                        select_cluster(cluster_cursor)
                        building_mode = True
                        lock = 5
                    elif b == BUTTON_OPTIONS:
                        if cluster_cursor != 0:
                            del clusters[cluster_cursor] 
                            cluster_cursor = 0


        # Bewegung mit LS
        if active_shape:
            ax = joystick.get_axis(AXIS_LS_X)
            ay = joystick.get_axis(AXIS_LS_Y)
            if abs(ax) > DEADZONE:
                active_shape['rect'].x += ax * BASE_MOVE_SPEED * dt
            if abs(ay) > DEADZONE:
                active_shape['rect'].y += ay * BASE_MOVE_SPEED * dt
            # Node-Manipulation oder globale Skalierung
            if active_shape['type'] == 'square':
                rsx = joystick.get_axis(AXIS_RS_X)
                rsy = joystick.get_axis(AXIS_RS_Y)
                if abs(rsx) > DEADZONE or abs(rsy) > DEADZONE:
                    idx = active_shape['selected_node']
                    dx = rsx * NODE_MOVE_SPEED * dt
                    dy = rsy * NODE_MOVE_SPEED * dt
                    cx, cy = active_shape['rect'].center
                    # Höhe anpassen (top/bottom)
                    if idx in (0, 2) and abs(rsy) > DEADZONE:
                        delta_h = -dy if idx == 0 else dy
                        new_h = active_shape['height'] + delta_h
                        if new_h >= MIN_SHAPE_SIZE:
                            active_shape['height'] = new_h
                            # Center Y verschieben
                            shift = dy/2
                            active_shape['rect'].center = (cx, cy + shift)
                    # Breite anpassen (right/left)
                    elif idx in (1, 3) and abs(rsx) > DEADZONE:
                        delta_w = (dx if idx == 1 else -dx)
                        new_w = active_shape['width'] + delta_w
                        if new_w >= MIN_SHAPE_SIZE:
                            active_shape['width'] = new_w
                            shift = dx/2
                            active_shape['rect'].center = (cx + shift, cy)
                else:
                    # Globale einheitliche Skalierung
                    l2 = joystick.get_axis(AXIS_L2)
                    r2 = joystick.get_axis(AXIS_R2)
                    if l2 > DEADZONE:
                        change = -l2 * BASE_SCALE_SPEED * dt
                        nw = active_shape['width'] + change
                        nh = active_shape['height'] + change
                        if nw >= MIN_SHAPE_SIZE and nh >= MIN_SHAPE_SIZE:
                            active_shape['width'], active_shape['height'] = nw, nh
                    if r2 > DEADZONE:
                        change = r2 * BASE_SCALE_SPEED * dt
                        active_shape['width'] += change
                        active_shape['height'] += change
            else:
                # Globale Skalierung für andere Formen
                l2 = joystick.get_axis(AXIS_L2)
                r2 = joystick.get_axis(AXIS_R2)
                if l2 > DEADZONE:
                    active_shape['scale'] = max(MIN_SHAPE_SIZE, active_shape['scale'] - l2 * BASE_SCALE_SPEED * dt)
                if r2 > DEADZONE:
                    active_shape['scale'] += r2 * BASE_SCALE_SPEED * dt
            # Preview-Update
            center = active_shape['rect'].center
            if active_shape['type'] == 'square':
                w, h = int(active_shape['width']), int(active_shape['height'])
                pad = NODE_RADIUS
                outline = create_outline('square', w, h, (255,0,0))
                surf = pygame.Surface((w+pad*2, h+pad*2), pygame.SRCALPHA)
                surf.blit(outline, (pad, pad))
                coords = [(w/2, 0), (w, h/2), (w/2, h), (0, h/2)]
                sel = active_shape['selected_node']
                for i, (nx, ny) in enumerate(coords):
                    col = (255,0,0) if i==sel else ICON_LIGHTBLUE_COLOR
                    pygame.draw.circle(surf, col, (int(nx+pad), int(ny+pad)), NODE_RADIUS)
                surf = pygame.transform.rotate(surf, active_shape['angle'])
            elif active_shape['type'] == 'circle':
                size = int(active_shape['scale'])
                pad = NODE_RADIUS
                outline = create_outline('circle', size, None, (255,0,0))
                surf = pygame.transform.rotate(outline, active_shape['angle'])
                surf = pygame.Surface((size+pad*2, size+pad*2), pygame.SRCALPHA)
                surf.blit(outline, (pad, pad))
                coords = [(pad+size//2, pad), (pad+size, pad+size//2), (pad+size//2, pad+size), (pad, pad+size//2)]
                sel = active_shape['selected_node']
                for i, (nx, ny) in enumerate(coords):
                    col = (255,0,0) if i==sel else ICON_LIGHTBLUE_COLOR
                    pygame.draw.circle(surf, col, (int(nx), int(ny)), NODE_RADIUS) 
                surf = pygame.transform.rotate(surf, active_shape['angle'])
            elif active_shape['type'] == 'plus':
                size = int(active_shape['scale'])
                pad = NODE_RADIUS
                outline = create_outline('plus', size, None, (255,0,0))
                surf = pygame.Surface((size+pad*2, size+pad*2), pygame.SRCALPHA)
                surf.blit(outline, (pad, pad))
                coords = [(pad+size//2, pad), (pad+size, pad+size//2), (pad+size//2, pad+size), (pad, pad+size//2)]
                sel = active_shape['selected_node']
                for i, (nx, ny) in enumerate(coords):
                    col = (255,0,0) if i==sel else ICON_LIGHTBLUE_COLOR
                    pygame.draw.circle(surf, col, (int(nx), int(ny)), NODE_RADIUS)
                surf = pygame.transform.rotate(surf, active_shape['angle'])
            elif active_shape['type'] == 'triangle':
                size = int(active_shape['scale'])
                pad = NODE_RADIUS
                outline = create_outline('triangle', size, None, (255,0,0))
                surf = pygame.Surface((size+pad*2+6, size+pad*2), pygame.SRCALPHA)
                surf.blit(outline, (pad+3, pad))
                coords = [(pad+size//2+3, pad+65/1000*size), ((pad+size+3), pad+ 935/1000 *size), (pad+3, pad+  935/1000 *size)]
                sel = active_shape['selected_node']
                for i, (nx, ny) in enumerate(coords):
                    col = (255,0,0) if i==sel else ICON_LIGHTBLUE_COLOR
                    pygame.draw.circle(surf, col, (int(nx), int(ny)), NODE_RADIUS)
                surf = pygame.transform.rotate(surf, active_shape['angle'])
            active_shape['surface'] = surf
            active_shape['rect'] = surf.get_rect(center=center)

        # Zeichnen

        if building_mode:
            screen.blit(bg_gray, (0,0))
            for r in placed_regions:
                screen.blit(r['surface'], r['rect'])
            for ic in placed_icons:
                screen.blit(ic['surface'], ic['rect'])
            if active_shape:
                screen.blit(active_shape['surface'], active_shape['rect'])
            for cluster in clusters:
                for r in cluster['placed_regions']:
                    screen.blit(r['surface'], r['rect'])
                for ic in cluster['placed_icons']:
                    screen.blit(ic['surface'], ic['rect'])
        else:
            screen.blit(bg_gray, (0,0))
            for cluster in clusters:
                for r in cluster['placed_regions']:
                    screen.blit(r['surface'], r['rect'])
                for ic in cluster['placed_icons']:
                    screen.blit(ic['surface'], ic['rect'])
            
        pygame.display.flip()
        lock = lock-1 if lock > 0 else 0

    # At the end:
    if allow_return_to_static:
        return "switch_to_static"
    return "quit"



def main():
    mode = "static"  # ⬅️ should default to static viewer

    while True:
        if mode == "static":
            result = run_static_viewer()
            if result == "quit":
                break
            elif result == "switch_to_dynamic":
                mode = "dynamic"

        elif mode == "dynamic":
            result = run_dynamic_environment()
            if result == "switch_to_static":
                mode = "static"
            elif result == "quit":
                break


if __name__ == "__main__":
    main()

