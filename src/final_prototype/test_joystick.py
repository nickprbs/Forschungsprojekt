import pygame

pygame.init()
pygame.joystick.init()

count = pygame.joystick.get_count()
print(f"🎮 Detected {count} gamepad(s).")

for i in range(count):
    joystick = pygame.joystick.Joystick(i)
    joystick.init()
    print(f" - Gamepad {i}: {joystick.get_name()}")

