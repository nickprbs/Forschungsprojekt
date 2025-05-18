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
NODE_MOVE_SPEED = 200      # Pixel/s für Node-Manipulation
OUTLINE_WIDTH = 4          # Stärke der Outline
NODE_RADIUS = OUTLINE_WIDTH * 2
ICON_LIGHT_COLOR = (50, 50, 255)

# PS4 Controller-Mappings
BUTTON_CROSS = 0      # X (Plus-Form)
BUTTON_CIRCLE = 1     # ○
BUTTON_SQUARE = 2     # □
BUTTON_TRIANGLE = 3   # Δ
BUTTON_L3 = 7         # Commit mit Linksklick-Stick
BUTTON_L1 = 9         # Rotation links
BUTTON_R1 = 10        # Rotation rechts
BUTTON_DPAD_RIGHT = 14
BUTTON_DPAD_LEFT = 13

# Achsen: 0 LS X, 1 LS Y, 2 RS X, 3 RS Y, 4 L2, 5 R2
AXIS_LS_X, AXIS_LS_Y = 0, 1
AXIS_RS_X, AXIS_RS_Y = 2, 3
AXIS_L2, AXIS_R2 = 4, 5

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

# Hintergründe laden & skalieren
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
placed_regions = []
placed_icons = []

# Maske für Formen
def create_mask(shape_type, size):
    mask = pygame.Surface((size, size), pygame.SRCALPHA)
    if shape_type == 'square':
        mask.fill((255,255,255,255))
    elif shape_type == 'circle':
        pygame.draw.circle(mask, (255,255,255,255), (size//2,size//2), size//2)
    elif shape_type == 'triangle':
        h = size * math.sqrt(3) / 2
        y = (size - h) / 2
        pts = [(size//2,int(y)), (0,int(y+h)), (size,int(y+h))]
        pygame.draw.polygon(mask, (255,255,255,255), pts)
    elif shape_type == 'plus':
        bar = size//4; c = size//2
        pygame.draw.rect(mask, (255,255,255,255), (c-bar//2,0,bar,size))
        pygame.draw.rect(mask, (255,255,255,255), (0,c-bar//2,size,bar))
    return mask

# Outline für Formen
def create_outline(shape_type, size, color):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    if shape_type == 'square':
        pygame.draw.rect(surf, color, surf.get_rect(), width=OUTLINE_WIDTH)
    elif shape_type == 'circle':
        pygame.draw.circle(surf, color, surf.get_rect().center, size//2, width=OUTLINE_WIDTH)
    elif shape_type == 'triangle':
        h = size * math.sqrt(3) / 2
        y = (size - h) / 2
        pts = [(size//2,int(y)), (0,int(y+h)), (size,int(y+h))]
        pygame.draw.polygon(surf, color, pts, width=OUTLINE_WIDTH)
    elif shape_type == 'plus':
        mask = create_mask('plus', size)
        mask_obj = pygame.mask.from_surface(mask)
        outline_pts = mask_obj.outline()
        if outline_pts:
            pygame.draw.lines(surf, color, True, outline_pts, width=OUTLINE_WIDTH)
    return surf

# Neues Shape instanziieren
def spawn_shape(shape_type):
    shape = {
        'type': shape_type,
        'scale': float(SHAPE_INITIAL_SIZE),
        'angle': 0,
        'rect': pygame.Rect(0, 0, SHAPE_INITIAL_SIZE, SHAPE_INITIAL_SIZE)
    }
    shape['rect'].center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
    if shape_type == 'square':
        shape['selected_node'] = 0  # 0=top,1=right,2=bottom,3=left
    return shape

# Form festsetzen
def commit_shape(shape):
    size = int(shape['scale'])
    center = shape['rect'].center
    mask = create_mask(shape['type'], size)
    outline = create_outline(shape['type'], size, (0,0,255))
    mask_r = pygame.transform.rotate(mask, shape['angle'])
    out_r = pygame.transform.rotate(outline, shape['angle'])
    region = pygame.Surface(mask_r.get_size(), pygame.SRCALPHA)
    rect_r = region.get_rect(center=center)
    tmp = pygame.Surface(mask_r.get_size(), pygame.SRCALPHA)
    tmp.blit(bg_color, (0,0), area=rect_r)
    region.blit(tmp, (0,0))
    region.blit(mask_r, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
    region.blit(out_r, (0,0))
    placed_regions.append({'surface':region,'rect':rect_r})
    # Icon
    icon = create_outline(shape['type'], size, ICON_LIGHT_COLOR)
    icon_r = pygame.transform.rotate(icon, shape['angle'])
    icon_rect = icon_r.get_rect(center=center)
    placed_icons.append({'surface':icon_r,'rect':icon_rect})

running = True
while running:
    dt = clock.tick(60) / 1000.0
    # Rotation kontinuierlich
    if active_shape:
        if joystick.get_button(BUTTON_L1):
            active_shape['angle'] = (active_shape['angle'] + ROTATION_SPEED*dt) % 360
        if joystick.get_button(BUTTON_R1):
            active_shape['angle'] = (active_shape['angle'] - ROTATION_SPEED*dt) % 360

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.JOYBUTTONDOWN:
            b = event.button
            # Spawns
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
            # Node-Iteration
            elif b == BUTTON_DPAD_RIGHT and active_shape and active_shape['type']=='square':
                active_shape['selected_node'] = (active_shape['selected_node'] + 1) % 4
            elif b == BUTTON_DPAD_LEFT and active_shape and active_shape['type']=='square':
                active_shape['selected_node'] = (active_shape['selected_node'] - 1) % 4

    if active_shape:
        # Bewegung (L-Stick)
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
                rect = active_shape['rect']
                idx = active_shape['selected_node']
                # Edge adjustment
                if idx == 0 and abs(rsy) > DEADZONE:  # top
                    new_top = rect.top + rsy * NODE_MOVE_SPEED * dt
                    new_h = rect.bottom - new_top
                    if new_h >= MIN_SHAPE_SIZE:
                        rect.height, rect.top = new_h, new_top
                elif idx == 1 and abs(rsx) > DEADZONE:  # right
                    new_right = rect.right + rsx * NODE_MOVE_SPEED * dt
                    new_w = new_right - rect.left
                    if new_w >= MIN_SHAPE_SIZE:
                        rect.width = new_w
                elif idx == 2 and abs(rsy) > DEADZONE:  # bottom
                    new_bottom = rect.bottom + rsy * NODE_MOVE_SPEED * dt
                    new_h = new_bottom - rect.top
                    if new_h >= MIN_SHAPE_SIZE:
                        rect.height = new_h
                elif idx == 3 and abs(rsx) > DEADZONE:  # left
                    new_left = rect.left + rsx * NODE_MOVE_SPEED * dt
                    new_w = rect.right - new_left
                    if new_w >= MIN_SHAPE_SIZE:
                        rect.left, rect.width = new_left, new_w
                active_shape['rect'] = rect
            else:
                # globale Skalierung (Trigger)
                l2 = joystick.get_axis(AXIS_L2)
                r2 = joystick.get_axis(AXIS_R2)
                if l2 > DEADZONE:
                    active_shape['scale'] = max(MIN_SHAPE_SIZE, active_shape['scale'] - l2 * BASE_SCALE_SPEED * dt)
                if r2 > DEADZONE:
                    active_shape['scale'] += r2 * BASE_SCALE_SPEED * dt
        else:
            # globale Skalierung für andere Formen
            l2 = joystick.get_axis(AXIS_L2)
            r2 = joystick.get_axis(AXIS_R2)
            if l2 > DEADZONE:
                active_shape['scale'] = max(MIN_SHAPE_SIZE, active_shape['scale'] - l2 * BASE_SCALE_SPEED * dt)
            if r2 > DEADZONE:
                active_shape['scale'] += r2 * BASE_SCALE_SPEED * dt
        # Preview-Update
        size = int(active_shape['scale'])
        center = active_shape['rect'].center
        outline = create_outline(active_shape['type'], size, (255,0,0))
        if active_shape['type']=='square':
            # Nodes hinzufügen
            pad = NODE_RADIUS
            w, h = size, size
            surf = pygame.Surface((w+pad*2, h+pad*2), pygame.SRCALPHA)
            surf.blit(outline, (pad,pad))
            coords = [(w/2,0),(w,h/2),(w/2,h),(0,h/2)]
            sel = active_shape['selected_node']
            for i,(nx,ny) in enumerate(coords):
                col = (255,0,0) if i==sel else ICON_LIGHT_COLOR
                pygame.draw.circle(surf, col, (int(nx+pad),int(ny+pad)), NODE_RADIUS)
            surf = pygame.transform.rotate(surf, active_shape['angle'])
        else:
            surf = pygame.transform.rotate(outline, active_shape['angle'])
        active_shape['surface'] = surf
        active_shape['rect'] = surf.get_rect(center=center)

    # Zeichnen
    screen.blit(bg_gray, (0,0))
    for r in placed_regions:
        screen.blit(r['surface'], r['rect'])
    for ic in placed_icons:
        screen.blit(ic['surface'], ic['rect'])
    if active_shape:
        screen.blit(active_shape['surface'], active_shape['rect'])
    pygame.display.flip()

pygame.quit()
