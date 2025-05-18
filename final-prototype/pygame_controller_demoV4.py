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
invert = False 

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
BUTTON_R3 = 8
BUTTON_DPAD_DOWN = 12
BUTTON_DPAD_UP = 11
BUTTON_OPTIONS = 6

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
placed_shapes = []
placed_regions = []
placed_icons = []
editing_index = None     # aktueller Index in placed_shapes
editing_backup = None    # Backup von region, icon, shape_data


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
    icon = create_outline(shape['type'], w, h, ICON_LIGHT_COLOR) if shape['type']=='square' else create_outline(shape['type'], size, None, ICON_LIGHT_COLOR)
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
                col = (255,0,0) if i==sel else ICON_LIGHT_COLOR
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
                col = (255,0,0) if i==sel else ICON_LIGHT_COLOR
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
                col = (255,0,0) if i==sel else ICON_LIGHT_COLOR
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
                col = (255,0,0) if i==sel else ICON_LIGHT_COLOR
                pygame.draw.circle(surf, col, (int(nx), int(ny)), NODE_RADIUS)
            surf = pygame.transform.rotate(surf, active_shape['angle'])
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