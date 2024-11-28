import pygame
import sys

# Initialize Pygame
pygame.init()
pygame.joystick.init()
print("Anzahl der erkannten Controller:", pygame.joystick.get_count())

# Initialize Controller
if pygame.joystick.get_count() == 0:
    print("Couldn't find Controller. Please connect and try again.")
    sys.exit()

xbox_controller = pygame.joystick.Joystick(0)
xbox_controller.init()

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


# Define window dimensions and colors
width, height = 800, 600
background_color = (30, 30, 30)
text_color = (200, 200, 200)
left_zone_color = (50, 150, 50, 50)  
right_zone_color = (150, 50, 50, 50)  

# Create window
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Controller Input Tracker")
font = pygame.font.Font(None, 36)

# Main loop
running = True
last_button_pressed = "No button pressed yet"
while running:
    screen.fill(background_color)

    # Event processing
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.JOYBUTTONDOWN:
            # Detect which button has been pressed
            button_index = event.button
            last_button_pressed = f'Button {button_names.get(button_index, "Unknown Button")} has been pressed.'

    # Read Button and Axis Values
    buttons = [xbox_controller.get_button(i) for i in range(xbox_controller.get_numbuttons())]
    axes = [xbox_controller.get_axis(i) for i in range(xbox_controller.get_numaxes())]

    # Visualisation of buttons
    button_text = font.render("Buttons: " + str(buttons), True, text_color)
    screen.blit(button_text, (20,20))

    # Visualization of last pressed button
    current_button_text = font.render(last_button_pressed, True, text_color)
    screen.blit(current_button_text, (20, 60))

    # Visualisation of Axis
    axis_text = font.render("Axes: " + str([round(axis,2) for axis in axes]), True, text_color)
    screen.blit(axis_text, (20, 100))

    # Stick area
    pygame.draw.circle(screen, (50, 150, 50), (int(width/4), int(height/2)), 120, width=2) #Left
    pygame.draw.circle(screen, (150, 50, 50), (int(3 * width/4), int(height/2)), 120, width=2) # Right

    # Joystick positions
    left_stick_x, left_stick_y = axes[0], axes[1]
    L_stick_pos_x = int(width / 4 + left_stick_x * 100)
    L_stick_pos_y = int(height / 2 + left_stick_y * 100)
    pygame.draw.circle(screen, (100, 200, 100), (L_stick_pos_x, L_stick_pos_y), 10) 

    right_stick_x, right_stick_y = axes[2], axes[3]
    R_stick_pos_x = int(3 * width / 4 + right_stick_x * 100)
    R_stick_pos_y = int(height / 2 + right_stick_y * 100)
    pygame.draw.circle(screen, (200, 100, 100), (R_stick_pos_x, R_stick_pos_y), 10) 

    # Actualize screen
    pygame.display.flip()

# End Pygame
pygame.quit()