import pygame
import sys
import os

# ----- Configuration -----
WINDOW_WIDTH = 948
WINDOW_HEIGHT = 900
FPS = 60

# PS4 Controller mapping (adjust if needed)
BUTTON_X = 0
BUTTON_L1 = 9
BUTTON_R1 = 10
BUTTON_L3 = 7
BUTTON_R3 = 8
BUTTON_OPTIONS = 6

# Axes indexes
LS_AXIS = 0   # Left stick horizontal
L2_AXIS = 4   # L2 trigger
R2_AXIS = 5   # R2 trigger

# Bar chart settings (anpassen: Position & Größe des ganzen Diagramms)
CHART_X = 43       # linke obere Ecke X
CHART_Y = 50       # linke obere Ecke Y
CHART_WIDTH = 902  # Breite des Diagramms
CHART_HEIGHT = 600 # Höhe des Diagramms
BAR_COUNT = 17     # Anzahl der Balken

# Axis threshold for trigger activation
AXIS_THRESHOLD = 0.5
# Delay in milliseconds for continuous movements
CURSOR_MOVE_DELAY = 200
BOUND_MOVE_DELAY = 200
# Directory for images
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "template")


# ----- Hilfsfunktionen -----
def draw_dashed_rect(surface, color, rect, dash_length=5):
    x1, y1 = rect.topleft
    x2, y2 = rect.bottomright
    dx = dash_length * 2
    # obere & untere Kante
    for x in range(x1, x2, dx):
        pygame.draw.line(surface, color, (x, y1), (min(x + dash_length, x2), y1))
        pygame.draw.line(surface, color, (x, y2), (min(x + dash_length, x2), y2))
    # linke & rechte Kante
    for y in range(y1, y2, dx):
        pygame.draw.line(surface, color, (x1, y), (x1, min(y + dash_length, y2)))
        pygame.draw.line(surface, color, (x2, y), (x2, min(y + dash_length, y2)))


def main():
    selected_count = 0
    pygame.init()
    pygame.joystick.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Bar Chart Selector')
    clock = pygame.time.Clock()

    if pygame.joystick.get_count() < 1:
        print("Kein Joystick gefunden. Bitte Controller anschließen.")
        pygame.quit()
        sys.exit()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    # Hintergrund-Bilder laden
    color_bg = pygame.image.load(os.path.join(IMAGE_DIR, "bar_color.png")).convert()
    gray_bg = pygame.image.load(os.path.join(IMAGE_DIR, "bar_gray.png")).convert()
    tooltipp_selected = pygame.image.load(os.path.join(IMAGE_DIR, "bar_tooltipp_selected.png")).convert_alpha()
    tooltipp_interval = pygame.image.load(os.path.join(IMAGE_DIR, "bar_tooltipp_interval.png")).convert_alpha()

    # Balken-Rechtecke berechnen
    bar_width = CHART_WIDTH // BAR_COUNT
    bar_rects = [pygame.Rect(CHART_X + i * bar_width, CHART_Y, bar_width, CHART_HEIGHT)
                 for i in range(BAR_COUNT)]

    # Subsurfaces für Balken vorberechnen
    bar_color_surfs = [color_bg.subsurface(r).copy() for r in bar_rects]
    bar_gray_surfs = [gray_bg.subsurface(r).copy() for r in bar_rects]

    # Status-Variablen
    cursor_idx = BAR_COUNT // 2
    selected = set()
    interval_mode = False
    interval_start = interval_end = None
    last_interval_start = None
    last_interval_end = None
    invert_interval = False
    pressed_buttons = set()

    last_cursor_move = pygame.time.get_ticks()
    last_bound_move = pygame.time.get_ticks()

    running = True
    while running:
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.JOYBUTTONDOWN:
                pressed_buttons.add(event.button)

                # Einzelauswahl mit X (nur Normalmodus)
                if event.button == BUTTON_X and not interval_mode:
                    if cursor_idx in selected:
                        selected.remove(cursor_idx)
                        selected_count -= 1
                        
                    else:
                        selected_count += 1
                        selected.add(cursor_idx)

                # Inrtervall-Modus toggeln (L3 + R3)
                if event.button in (BUTTON_R3, BUTTON_L3) and (joystick.get_button(BUTTON_L3) and joystick.get_button(BUTTON_R3)):
                    if not interval_mode:
                        # Öffnen: Verwende vorheriges Intervall falls vorhanden

                        interval_mode = True
                        if last_interval_start is not None and last_interval_end is not None:
                            interval_start = last_interval_start
                            interval_end = last_interval_end
                            last_interval_start = None
                            last_interval_end = None
                            if invert_interval:
                                # Invertiere Selektion
                                if interval_end >= interval_start:
                                    selected -= set(range(0, interval_start)) | set(range(interval_end, BAR_COUNT))
                                else:
                                    selected -= set(range(interval_end +1 , interval_start))
                            else:
                                if interval_end >= interval_start:
                                    selected -= set(range(interval_start, interval_end + 1))
                                else:
                                    selected -= set(range(interval_start, BAR_COUNT)) | set(range(0, interval_end + 1))
                        else:
                            mid = BAR_COUNT // 2
                            interval_start = interval_end = mid
                        
                    else:
                        # Schließen: speichere aktuelles Intervall
                        last_interval_start = interval_start
                        last_interval_end = interval_end
                        # Überführen in Selektion
                        if interval_end >= interval_start:
                            rng = set(range(interval_start, interval_end + 1))
                        else: 
                            rng = set(range(interval_start, BAR_COUNT)) | set(range(0, interval_end + 1))
                        if not invert_interval:
                            selected |= rng
                        else:
                            selected |= (set(range(BAR_COUNT)) - rng)
                        interval_mode = False
                        interval_start = interval_end = None

                # Intervall invertieren (R3 einzeln)
                if interval_mode and event.button == BUTTON_R3 and not joystick.get_button(BUTTON_L3):
                    invert_interval = not invert_interval

                # Intervall löschen (Options)
                if interval_mode and event.button == BUTTON_OPTIONS:
                    mid = BAR_COUNT // 2
                    interval_start = interval_end = mid
                    invert_interval = False

            elif event.type == pygame.JOYBUTTONUP:
                if event.button in pressed_buttons:
                    pressed_buttons.remove(event.button)

        # ----- Achsen-Verarbeitung -----
        ls_val = joystick.get_axis(LS_AXIS)
        if not interval_mode:
            # LS: Cursor-Bewegung mit Verzögerung
            if current_time - last_cursor_move >= CURSOR_MOVE_DELAY:
                if ls_val > AXIS_THRESHOLD:
                    cursor_idx = (cursor_idx + 1) % BAR_COUNT
                    last_cursor_move = current_time
                elif ls_val < -AXIS_THRESHOLD:
                    cursor_idx = (cursor_idx - 1) % BAR_COUNT
                    last_cursor_move = current_time
                # Zur nächsten Auswahl springen
                if joystick.get_button(BUTTON_R1):
                    if selected:
                        new_cursor = (cursor_idx + 1) % BAR_COUNT
                        while new_cursor not in selected:
                            new_cursor = (new_cursor + 1) % BAR_COUNT
                        cursor_idx = new_cursor
                        last_cursor_move = current_time
                if joystick.get_button(BUTTON_L1):
                    if selected:
                        new_cursor = (cursor_idx - 1) % BAR_COUNT
                        while new_cursor not in selected:
                            new_cursor = (new_cursor - 1) % BAR_COUNT
                        cursor_idx = new_cursor
                    last_cursor_move = current_time
        else:
            # LS: Intervall-Verschiebung mit Verzögerung über Chart-Grenzen hinweg
            if current_time - last_bound_move >= BOUND_MOVE_DELAY:
                if ls_val > AXIS_THRESHOLD:
                    interval_start = (interval_start + 1) % BAR_COUNT
                    interval_end = (interval_end + 1) % BAR_COUNT
                    last_bound_move = current_time
                elif ls_val < -AXIS_THRESHOLD:
                    interval_start = (interval_start - 1) % BAR_COUNT
                    interval_end = (interval_end - 1) % BAR_COUNT
                    last_bound_move = current_time

            # Kontinuierliches Verschieben der Intervalsgrenzen mit Buttons
            if current_time - last_bound_move >= BOUND_MOVE_DELAY:
                if joystick.get_button(BUTTON_L1):
                    interval_start = (interval_start + 1) % BAR_COUNT
                    last_bound_move = current_time
                if joystick.get_button(BUTTON_R1):
                    interval_end = (interval_end + 1) % BAR_COUNT
                    last_bound_move = current_time

            # Kontinuierliches Anpassen der Intervalsgrenzen mit Triggern
            l2_val = joystick.get_axis(L2_AXIS)
            if current_time - last_bound_move >= BOUND_MOVE_DELAY and l2_val > AXIS_THRESHOLD and True:
                interval_start = (interval_start - 1) % BAR_COUNT 
                last_bound_move = current_time
            r2_val = joystick.get_axis(R2_AXIS)
            if current_time - last_bound_move >= BOUND_MOVE_DELAY and r2_val > AXIS_THRESHOLD:
                interval_end = (interval_end - 1) % BAR_COUNT
                last_bound_move = current_time

        # ----- Zeichnen -----
        if not interval_mode:

            screen.blit(tooltipp_selected, (0, 660))
            if not selected:
                screen.blit(color_bg, (0, 0))
            else:
                screen.blit(gray_bg, (0, 0))
                for idx in selected:
                    screen.blit(bar_color_surfs[idx], bar_rects[idx].topleft)
            
            pygame.draw.rect(screen, (140, 80, 255), pygame.Rect(0, 0, 948, 660), 4)
        else:
            screen.blit(tooltipp_interval, (0, 660))
            if not invert_interval:
                screen.blit(gray_bg, (0, 0))
                # Intervall farbig
                if interval_start <= interval_end:
                    for idx in range(interval_start, interval_end + 1):
                        screen.blit(bar_color_surfs[idx], bar_rects[idx].topleft)
                else: 
                    for idx in range(interval_start, BAR_COUNT):
                        screen.blit(bar_color_surfs[idx], bar_rects[idx].topleft)
                    for idx in range(0, interval_end + 1):
                        screen.blit(bar_color_surfs[idx], bar_rects[idx].topleft)
                # normale Auswahl farbig
                for idx in selected:
                    screen.blit(bar_color_surfs[idx], bar_rects[idx].topleft)
            else:
                screen.blit(color_bg, (0, 0))
                # Intervall grau
                if interval_start <= interval_end:
                    for idx in range(interval_start, interval_end + 1):
                        screen.blit(bar_gray_surfs[idx], bar_rects[idx].topleft)
                else: 
                    for idx in range(interval_start, BAR_COUNT):
                        screen.blit(bar_gray_surfs[idx], bar_rects[idx].topleft)
                    for idx in range(0, interval_end + 1):
                        screen.blit(bar_gray_surfs[idx], bar_rects[idx].topleft)
                # normale Auswahl farbig
                for idx in selected:
                    screen.blit(bar_color_surfs[idx], bar_rects[idx].topleft)
            
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(0, 0, 948, 660), 4)


        if not interval_mode:
            # Cursor zeichnen   
            cursor_rect = bar_rects[cursor_idx]
            draw_dashed_rect(screen, (255, 0, 0), cursor_rect)
        else: 
            # Intervall-Rechteck zeichnen
            if interval_start <= interval_end:
                interval_rect = pygame.Rect(bar_rects[interval_start].left, bar_rects[interval_start].top,
                                             bar_rects[interval_end].right - bar_rects[interval_start].left,
                                             bar_rects[interval_end].bottom - bar_rects[interval_start].top)
                draw_dashed_rect(screen, (255, 0, 0), interval_rect)
            else:
                interval_rect_left = pygame.Rect(bar_rects[0].left, bar_rects[0].top,
                                             bar_rects[interval_end].right - bar_rects[0].left,
                                             bar_rects[interval_end].bottom - bar_rects[0].top)
                
                interval_rect_right = pygame.Rect(bar_rects[interval_start].left, bar_rects[interval_start].top,
                                             bar_rects[16].right - bar_rects[interval_start].left,
                                             bar_rects[16].bottom - bar_rects[interval_start].top)
                draw_dashed_rect(screen, (255, 0, 0), interval_rect_left)
                draw_dashed_rect(screen, (255, 0, 0), interval_rect_right)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
