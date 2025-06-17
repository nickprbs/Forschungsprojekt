import pygame
import sys
from time import sleep

pygame.init()
pygame.joystick.init()

button_names = {
    0: "A",
    1: "B",
    2: "X",
    3: "Y",
    4: "BACK",
    5: "GUIDE",
    6: "START",
    7: "L STICK",
    8: "R Stick",
    9: "LB",
    10: "RB",
    11: "DPAD-UP",
    12: "DPAD-DOWN",
    13: "DPAD-LEFT",
    14: "DPAD-RIGHT"
}



if pygame.joystick.get_count() == 0:
    print("Couldn't find Controller. Please connect and try again.")
    sys.exit()

ps_controller = pygame.joystick.Joystick(0)
ps_controller.init()

width, height = 1200, 800
background_image =  pygame.image.load("Prototyp/img/start.jpg")
background_image = pygame.transform.scale(background_image, (width, height))

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Protoype / Mockup")
font = pygame.font.Font(None, 36)


running = True
state = 0
last_button_pressed = "No button pressed yet"
selection = 0
selected = False
while running:
    buttons = [ps_controller.get_button(i) for i in range(ps_controller.get_numbuttons())]
    axes = [ps_controller.get_axis(i) for i in range(ps_controller.get_numaxes())]

    for event in pygame.event.get():
        buttons = [ps_controller.get_button(i) for i in range(ps_controller.get_numbuttons())]
        axes = [ps_controller.get_axis(i) for i in range(ps_controller.get_numaxes())]
        if event.type == pygame.JOYBUTTONDOWN:
            print(pygame.CONTROLLER_BUTTON_DPAD_DOWN)
            if state == 0:
                if buttons[14] == 1:
                    state = 1
                    background_image = pygame.image.load("Prototyp/img/S1.jpg")
                    selection = 0
                elif buttons[12] == 1:
                    state = 2
                    background_image = pygame.image.load("Prototyp/img/S2.jpg")
                    selection = 0
            elif state == 1:
                if buttons[13] == 1:
                    state = 0
                    background_image = pygame.image.load("Prototyp/img/start.jpg")
                    selection = 0
                elif buttons[12] == 1:
                    state = 3
                    background_image = pygame.image.load("Prototyp/img/S3.jpg")
                    selection = 0
            elif state == 2:
                if buttons[14] == 1:
                    state = 3
                    background_image = pygame.image.load("Prototyp/img/S3.jpg")
                    selection = 0
                elif buttons[11] == 1:
                    state = 0 
                    background_image = pygame.image.load("Prototyp/img/start.jpg")
                    selection = 0
            elif state == 3:
                if buttons[13] == 1:
                    state = 2
                    background_image = pygame.image.load("Prototyp/img/S2.jpg")
                    selection = 0
                elif buttons[11] == 1:
                    state = 1
                    background_image = pygame.image.load("Prototyp/img/S1.jpg")
                    selection = 0
            selected = False

        #print(event)
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.JOYBUTTONDOWN:
            button_index = event.button
            last_button_pressed = f'Button {button_names.get(button_index, "Unknown Button")} has been pressed.'


    left_stick_x, left_stick_y = axes[0], axes[1]
    right_stick_x, right_stick_y = axes[2], axes[3]
    x_button = buttons[0]
    circle_button = buttons[1]
    square_button = buttons[2]
    right_bumper = buttons[10]
    left_bumper = buttons[9]
    
    if state == 0:
        if left_stick_x < -0.4 and left_stick_y < -0.4:
            background_image = pygame.image.load("prototyp/img/S0_LU.jpg")
        elif left_stick_x > 0.4 and left_stick_y < -0.4:
            background_image = pygame.image.load("Prototyp/img/S0_RU.jpg")
        elif left_stick_x < -0.4 and left_stick_y > 0.4:
            background_image = pygame.image.load("Prototyp/img/S0_LD.jpg")
        elif left_stick_x > 0.4 and left_stick_y > 0.4:
            background_image = pygame.image.load("Prototyp/img/S0_RD.jpg") 
        elif left_stick_x < -0.5:
            background_image = pygame.image.load("Prototyp/img/S0_L.jpg")
        elif left_stick_x > 0.5:
            background_image = pygame.image.load("Prototyp/img/S0_R.jpg")
        elif left_stick_y < -0.5:
            background_image = pygame.image.load("Prototyp/img/S0_U.jpg")
        elif left_stick_y > 0.5:
            background_image = pygame.image.load("Prototyp/img/S0_D.jpg")
        elif abs(left_stick_x) < 0.5 and abs(left_stick_y) < 0.5:
            background_image = pygame.image.load("Prototyp/img/start.jpg")
    elif state == 2:
        if selection == 0 and x_button:
            selection = 1
            background_image = pygame.image.load("Prototyp/img/S2_selection1.jpg")
        elif not selection == 0:
            if circle_button:
                selection = 0
                background_image = pygame.image.load("Prototyp/img/S2.jpg")
            elif right_bumper:
                if selection == 1:
                    selection = 2
                    background_image = pygame.image.load("Prototyp/img/S2_selection2.jpg")
                elif selection == 2:
                    selection = 3
                    background_image = pygame.image.load("Prototyp/img/S2_selection3.jpg")
            elif left_bumper:
                if selection == 2:
                    selection = 1
                    background_image = pygame.image.load("Prototyp/img/S2_selection1.jpg")
                elif selection == 3:
                    selection = 2
                    background_image = pygame.image.load("Prototyp/img/S2_selection2.jpg")
            elif selection == 3 and square_button:
                if not selected:
                    selected = True
                    background_image = pygame.image.load("Prototyp/img/S2_selected.jpg")
                else: 
                    selected = False
                    background_image = pygame.image.load("Prototyp/img/S2_selection3.jpg")
            sleep(0.06)

    elif state == 3:
        if selection == 0 and x_button:
            selection = 1
            background_image = pygame.image.load("Prototyp/img/S3_selection1.jpg")
        elif not selection == 0:
            if circle_button:
                selection = 0
                background_image = pygame.image.load("Prototyp/img/S3.jpg")
            elif right_bumper:
                if selection == 1:
                    selection = 2
                    background_image = pygame.image.load("Prototyp/img/S3_selection2.jpg")
                elif selection == 2:
                    selection = 3
                    background_image = pygame.image.load("Prototyp/img/S3_selection3.jpg")
                elif selection == 3:
                    selection = 4
                    background_image = pygame.image.load("Prototyp/img/S3_selection4.jpg")
                elif selection == 4:
                    selection = 1
                    background_image = pygame.image.load("Prototyp/img/S3_selection1.jpg")
            elif left_bumper:
                if selection == 2:
                    selection = 1
                    background_image = pygame.image.load("Prototyp/img/S3_selection1.jpg")
                elif selection == 3:
                    selection = 2
                    background_image = pygame.image.load("Prototyp/img/S3_selection2.jpg")
                elif selection == 4:
                    selection = 3
                    background_image = pygame.image.load("Prototyp/img/S3_selection3.jpg")
                elif selection == 1:
                    selection = 4
                    background_image = pygame.image.load("Prototyp/img/S3_selection4.jpg")
            elif selection == 1 and square_button:
                if not selected:
                    selected = True
                    background_image = pygame.image.load("Prototyp/img/S3_selected.jpg")
                else: 
                    selected = False
                    background_image = pygame.image.load("Prototyp/img/S3_selection1.jpg")
            sleep(0.06)

    background_image = pygame.transform.scale(background_image, (width, height))
    screen.blit(background_image, (0, 0))

    pygame.display.flip()

pygame.quit()
