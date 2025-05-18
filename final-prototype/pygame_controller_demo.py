import pygame
import sys

# Konfiguration
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
BG_GRAY_PATH = 'bg_gray.png'
BG_COLOR_PATH = 'bg_color.png'
SHAPE_INITIAL_SIZE = 100
MIN_SHAPE_SIZE = 10
DEADZONE = 0.1
BASE_MOVE_SPEED = 300    # Maximale Pixel pro Sekunde bei vollem Ausschlag
BASE_SCALE_SPEED = 100   # Maximale Größenänderung pro Sekunde bei vollem Auslösen
OUTLINE_WIDTH = 4        # Stärke der Outline
ICON_LIGHT_COLOR = (50, 50, 255)  # leicht aufgehelltes Blau für Icons

# PS4 Controller-Mappings (kann je nach Plattform variieren)
BUTTON_SQUARE = 2        # □
BUTTON_CIRCLE = 1        # ○
BUTTON_L3 = 7            # Linker Stick (L3) - jetzt korrekt auf Index 7 gesetzt
# Achsen: 0: LS X, 1: LS Y, 2: RS X, 3: RS Y, 4: L2, 5: R2
AXIS_LS_X = 0
AXIS_LS_Y = 1
AXIS_L2 = 4
AXIS_R2 = 5

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

# Hintergründe laden und skalieren
bg_gray = pygame.image.load(BG_GRAY_PATH).convert()
bg_gray = pygame.transform.scale(bg_gray, (WINDOW_WIDTH, WINDOW_HEIGHT))
bg_color = pygame.image.load(BG_COLOR_PATH).convert()
bg_color = pygame.transform.scale(bg_color, (WINDOW_WIDTH, WINDOW_HEIGHT))

# Joystick initialisieren
pygame.joystick.init()
if pygame.joystick.get_count() == 0:
    print("Kein Controller gefunden!")
    sys.exit()
joystick = pygame.joystick.Joystick(0)
joystick.init()

active_shape = None
placed_regions = []  # Farbige Ausschnitte aus bg_color mit Outline
placed_icons = []    # Blaue Outline-Icons


def create_shape_outline_surface(shape_type, size, color, outline_width=OUTLINE_WIDTH):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    rect = surf.get_rect()
    if shape_type == 'square':
        pygame.draw.rect(surf, color, rect, width=outline_width)
    else:
        pygame.draw.circle(surf, color, rect.center, size // 2, width=outline_width)
    return surf


def spawn_shape(shape_type):
    shape = {
        'type': shape_type,
        'scale': float(SHAPE_INITIAL_SIZE),
        'rect': pygame.Rect(0, 0, SHAPE_INITIAL_SIZE, SHAPE_INITIAL_SIZE)
    }
    shape['rect'].center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
    return shape


def commit_shape(shape):
    size = int(shape['scale'])
    rect = shape['rect']
    # Farbigen Ausschnitt aus bg_color kopieren und maskieren
    orig = bg_color.subsurface(rect).copy()
    mask_surf = pygame.Surface((size, size), pygame.SRCALPHA)
    if shape['type'] == 'square':
        mask_surf.fill((255, 255, 255, 255))
    else:
        pygame.draw.circle(mask_surf, (255, 255, 255, 255), (size // 2, size // 2), size // 2)
    region = pygame.Surface((size, size), pygame.SRCALPHA)
    region.blit(orig, (0, 0))
    region.blit(mask_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    # Nur Outline in Blau über die regionale Surface zeichnen
    if shape['type'] == 'square':
        pygame.draw.rect(region, (0, 0, 255), region.get_rect(), width=OUTLINE_WIDTH)
    else:
        pygame.draw.circle(region, (0, 0, 255), (size // 2, size // 2), size // 2, width=OUTLINE_WIDTH)
    placed_regions.append({'surface': region, 'rect': rect.copy()})
    # Miniatur-Icon: Nur Outline in leicht aufgehelltem Blau, Originalgröße
    icon = create_shape_outline_surface(shape['type'], size, ICON_LIGHT_COLOR)
    icon_rect = icon.get_rect(center=rect.center)
    placed_icons.append({'surface': icon, 'rect': icon_rect})

running = True
while running:
    dt = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.JOYBUTTONDOWN:
            if event.button == BUTTON_SQUARE and not active_shape:
                active_shape = spawn_shape('square')
            elif event.button == BUTTON_CIRCLE and not active_shape:
                active_shape = spawn_shape('circle')
            elif event.button == BUTTON_L3 and active_shape:
                commit_shape(active_shape)
                active_shape = None

    # Manipulation der aktiven Form basierend auf analogem Input
    if active_shape:
        axis_x = joystick.get_axis(AXIS_LS_X)
        axis_y = joystick.get_axis(AXIS_LS_Y)
        if abs(axis_x) > DEADZONE:
            active_shape['rect'].x += axis_x * BASE_MOVE_SPEED * dt
        if abs(axis_y) > DEADZONE:
            active_shape['rect'].y += axis_y * BASE_MOVE_SPEED * dt
        l2 = joystick.get_axis(AXIS_L2)
        r2 = joystick.get_axis(AXIS_R2)
        if l2 > DEADZONE:
            active_shape['scale'] = max(MIN_SHAPE_SIZE,
                                       active_shape['scale'] - l2 * BASE_SCALE_SPEED * dt)
        if r2 > DEADZONE:
            active_shape['scale'] += r2 * BASE_SCALE_SPEED * dt
        size = int(active_shape['scale'])
        center = active_shape['rect'].center
        active_shape['surface'] = create_shape_outline_surface(active_shape['type'], size, (255, 0, 0))
        active_shape['rect'] = active_shape['surface'].get_rect(center=center)

    # Zeichnen aller Elemente
    screen.blit(bg_gray, (0, 0))
    for region in placed_regions:
        screen.blit(region['surface'], region['rect'])
    for icon in placed_icons:
        screen.blit(icon['surface'], icon['rect'])
    if active_shape:
        screen.blit(active_shape['surface'], active_shape['rect'])
    pygame.display.flip()

pygame.quit()
