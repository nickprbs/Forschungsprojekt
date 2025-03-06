import pygame

pygame.init()
ps_controller = pygame.joystick.Joystick(0)
ps_controller.init()
running = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.JOYAXISMOTION:
            for i in range(ps_controller.get_numaxes()):
                if ps_controller.get_axis(i) > 0.1:
                    print(f"Axis {i}: {ps_controller.get_axis(i)}")  
        else:  
            print(event)


print("buttons pressed: ", ps_controller.get_numbuttons())
print("axes: ", ps_controller.get_numaxes())
print("hats: ", ps_controller.get_numhats())
print("balls: ", ps_controller.get_numballs())
