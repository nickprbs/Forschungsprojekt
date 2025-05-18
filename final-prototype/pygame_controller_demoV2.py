import pygame
import sys
import math

# Konfiguration
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
BG_GRAY_PATH = 'bg_gray.png'
BG_COLOR_PATH = 'bg_color.png'
SHAPE_INITIAL_SIZE = 100
MIN_SHAPE_SIZE = 10
DEADZONE = 0.1
BASE_MOVE_SPEED = 300      # Pixel/s bei vollem Stick
BASE_SCALE_SPEED = 100     # Größenänderung/s bei vollem Trigger
ROTATION_SPEED = 90        # Grad/s bei gehaltenem L1/R1
OUTLINE_WIDTH = 4          # Stärke der Outline
ICON_LIGHT_COLOR = (50, 50, 255)  # leicht aufgehelltes Blau für Icons

# PS4 Controller-Mappings
BUTTON_CROSS = 0      # X (Plus-Form)
BUTTON_CIRCLE = 1     # ○
BUTTON_SQUARE = 2     # □
BUTTON_TRIANGLE = 3   # Δ
BUTTON_L3 = 7         # Commit mit Linksklick-Stick
BUTTON_L1 = 9         # Rotation links
BUTTON_R1 = 10        # Rotation rechts
# Achsen: 0: LS X, 1: LS Y, 4: L2, 5: R2
AXIS_LS_X = 0
AXIS_LS_Y = 1
AXIS_L2 = 4
AXIS_R2 = 5

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

# Bilder laden & skalieren
bg_gray = pygame.image.load(BG_GRAY_PATH).convert()
bg_gray = pygame.transform.scale(bg_gray, (WINDOW_WIDTH, WINDOW_HEIGHT))
bg_color = pygame.image.load(BG_COLOR_PATH).convert()
bg_color = pygame.transform.scale(bg_color, (WINDOW_WIDTH, WINDOW_HEIGHT))

# Joystick init
pygame.joystick.init()
if pygame.joystick.get_count() == 0:
    print("Kein Controller gefunden!")
    sys.exit()
joystick = pygame.joystick.Joystick(0)
joystick.init()

active_shape = None
placed_regions = []  # Ausschnitte mit Maske & Outline
placed_icons = []    # Icons mit Outline

# Maske erzeugen (für alle Formen)
def create_mask(shape_type, size):
    mask = pygame.Surface((size, size), pygame.SRCALPHA)
    if shape_type == 'square':
        mask.fill((255, 255, 255, 255))
    elif shape_type == 'circle':
        pygame.draw.circle(mask, (255, 255, 255, 255), (size//2, size//2), size//2)
    elif shape_type == 'triangle':
        h = size * math.sqrt(3) / 2
        y_off = (size - h) / 2
        p1 = (size//2, int(y_off))
        p2 = (0, int(y_off + h))
        p3 = (size, int(y_off + h))
        pygame.draw.polygon(mask, (255, 255, 255, 255), [p1, p2, p3])
    elif shape_type == 'plus':
        bar = size // 4
        c = size // 2
        pygame.draw.rect(mask, (255,255,255,255), (c - bar//2, 0, bar, size))
        pygame.draw.rect(mask, (255,255,255,255), (0, c - bar//2, size, bar))
    return mask

# Outline erzeugen (für alle Formen)
def create_outline(shape_type, size, color):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    if shape_type == 'square':
        pygame.draw.rect(surf, color, surf.get_rect(), width=OUTLINE_WIDTH)
    elif shape_type == 'circle':
        pygame.draw.circle(surf, color, surf.get_rect().center, size//2, width=OUTLINE_WIDTH)
    elif shape_type == 'triangle':
        h = size * math.sqrt(3) / 2
        y_off = (size - h) / 2
        p1 = (size//2, int(y_off))
        p2 = (0, int(y_off + h))
        p3 = (size, int(y_off + h))
        pygame.draw.polygon(surf, color, [p1, p2, p3], width=OUTLINE_WIDTH)
    elif shape_type == 'plus':
        # Verwende Masken-Kontur für gleichmäßige Dicke
        mask_surf = create_mask('plus', size)
        mask_obj = pygame.mask.from_surface(mask_surf)
        outline_pts = mask_obj.outline()
        if outline_pts:
            pygame.draw.lines(surf, color, True, outline_pts, width=OUTLINE_WIDTH)
    return surf

# Neue Form spawnen
def spawn_shape(shape_type):
    shape = {'type': shape_type,
             'scale': float(SHAPE_INITIAL_SIZE),
             'angle': 0,
             'rect': pygame.Rect(0, 0, SHAPE_INITIAL_SIZE, SHAPE_INITIAL_SIZE)}
    shape['rect'].center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
    return shape

# Form final platzieren (Commit)
def commit_shape(shape):
    size = int(shape['scale'])
    center = shape['rect'].center

    mask = create_mask(shape['type'], size)
    outline = create_outline(shape['type'], size, (0, 0, 255))
    mask_rot = pygame.transform.rotate(mask, shape['angle'])
    outline_rot = pygame.transform.rotate(outline, shape['angle'])

    region = pygame.Surface(mask_rot.get_size(), pygame.SRCALPHA)
    rect_rot = region.get_rect(center=center)
    tmp = pygame.Surface(mask_rot.get_size(), pygame.SRCALPHA)
    tmp.blit(bg_color, (0, 0), area=rect_rot)
    region.blit(tmp, (0, 0))
    region.blit(mask_rot, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    region.blit(outline_rot, (0, 0))
    placed_regions.append({'surface': region, 'rect': rect_rot})

    icon_base = create_outline(shape['type'], size, ICON_LIGHT_COLOR)
    icon_rot = pygame.transform.rotate(icon_base, shape['angle'])
    icon_rect = icon_rot.get_rect(center=center)
    placed_icons.append({'surface': icon_rot, 'rect': icon_rect})

running = True
while running:
    dt = clock.tick(60) / 1000.0

    # Kontinuierliche Rotation
    if active_shape:
        if joystick.get_button(BUTTON_L1):
            active_shape['angle'] = (active_shape['angle'] + ROTATION_SPEED * dt) % 360
        if joystick.get_button(BUTTON_R1):
            active_shape['angle'] = (active_shape['angle'] - ROTATION_SPEED * dt) % 360

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.JOYBUTTONDOWN:
            if event.button == BUTTON_SQUARE and not active_shape:
                active_shape = spawn_shape('square')
            elif event.button == BUTTON_CIRCLE and not active_shape:
                active_shape = spawn_shape('circle')
            elif event.button == BUTTON_TRIANGLE and not active_shape:
                active_shape = spawn_shape('triangle')
            elif event.button == BUTTON_CROSS and not active_shape:
                active_shape = spawn_shape('plus')
            elif event.button == BUTTON_L3 and active_shape:
                commit_shape(active_shape)
                active_shape = None

    # Bewegung & Skalierung analog
    if active_shape:
        ax = joystick.get_axis(AXIS_LS_X)
        ay = joystick.get_axis(AXIS_LS_Y)
        if abs(ax) > DEADZONE:
            active_shape['rect'].x += ax * BASE_MOVE_SPEED * dt
        if abs(ay) > DEADZONE:
            active_shape['rect'].y += ay * BASE_MOVE_SPEED * dt
        l2 = joystick.get_axis(AXIS_L2)
        r2 = joystick.get_axis(AXIS_R2)
        if l2 > DEADZONE:
            active_shape['scale'] = max(MIN_SHAPE_SIZE,
                                       active_shape['scale'] - l2 * BASE_SCALE_SPEED * dt)
        if r2 > DEADZONE:
            active_shape['scale'] += r2 * BASE_SCALE_SPEED * dt

        # Preview aktualisieren
        size = int(active_shape['scale'])
        center = active_shape['rect'].center
        surf = create_outline(active_shape['type'], size, (255, 0, 0))
        surf = pygame.transform.rotate(surf, active_shape['angle'])
        rect = surf.get_rect(center=center)
        active_shape['surface'] = surf
        active_shape['rect'] = rect

    # Zeichnen
    screen.blit(bg_gray, (0, 0))
    for r in placed_regions:
        screen.blit(r['surface'], r['rect'])
    for icon in placed_icons:
        screen.blit(icon['surface'], icon['rect'])
    if active_shape:
        screen.blit(active_shape['surface'], active_shape['rect'])
    pygame.display.flip()

pygame.quit()
