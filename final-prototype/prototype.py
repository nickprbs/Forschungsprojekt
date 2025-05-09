import os
import pygame
from enum import Enum, auto

# --- 1) State-Definition (bleibt gleich) ---
class State(Enum):
    SCATTER       = auto()
    BUILD1        = auto()
    BUILD2        = auto()
    NULL_OBJECT   = auto()
    INTERVAL_AXIS = auto()
    BAR_SELECTED  = auto()
    # … alle weiteren States

# --- 2) ScreenManager für PNGs ---
class ScreenManager:
    def __init__(self, folder_path: str, mapping: dict[State, str]):
        """
        folder_path: Pfad zu Deinem Verzeichnis mit den PNGs
        mapping: Dict, das jedem State den entsprechenden Dateinamen zuordnet
        """
        self.folder = folder_path
        self.mapping = mapping
        self.cache: dict[State, pygame.Surface] = {}

    def get_screen(self, state: State) -> pygame.Surface:
        if state in self.cache:
            return self.cache[state]
        filename = self.mapping[state]
        fullpath = os.path.join(self.folder, filename)
        surf = pygame.image.load(fullpath).convert()
        # Optional: surf = pygame.transform.scale(surf, (1280,720))
        self.cache[state] = surf
        return surf

# --- InteractionManager und Input bleiben wie gehabt (siehe vorheriges Beispiel) ---
# --- 3) InteractionManager (State Machine) ---
class InteractionManager:
    def __init__(self, screen_manager: ScreenManager):
        self.sm = screen_manager
        self.state = State.SCATTER
        # Übergangsgraph: (aktueller State, Aktion) → neuer State
        self.transitions = {
            (State.SCATTER,       "NEXT"): State.BUILD1,
            (State.BUILD1,        "SPAWN_TRIANGLE"): State.BUILD2,
            (State.BUILD2,        "NO_SELECTION"): State.NULL_OBJECT,
            (State.NULL_OBJECT,   "ENTER_INTERVAL"): State.INTERVAL_AXIS,
            (State.INTERVAL_AXIS, "SELECT_BAR"): State.BAR_SELECTED,
            # … ergänze alle Übergänge Deines Flowcharts
        }

    def handle(self, action: str):
        key = (self.state, action)
        if key in self.transitions:
            self.state = self.transitions[key]
            # beim State-Wechsel ggf. Screen updaten:
            return True   # Signal: State hat sich geändert
        return False      # keine Transition gefunden

# --- 4) Input-Mapping auf Actions ---
def map_input_to_action(event) -> str | None:
    # Beispiel: D-Pad rechts → "NEXT", Button X → "SPAWN_TRIANGLE" …
    if event.type == pygame.JOYHATMOTION:
        x, y = event.value
        if x == 1: return "NEXT"
        if x == -1: return "PREV"
    if event.type == pygame.JOYBUTTONDOWN:
        if event.button == 0: return "SPAWN_TRIANGLE"  # X-Button
        if event.button == 1: return "ENTER_INTERVAL"  # Kreis
    # …
    return None

# --- 5) Haupt-Loop mit PNG-Screens ---
def run_app(png_folder: str):
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    
    # Mapping-Beispiel: State → Dateiname
    png_map = {
        State.SCATTER:       "GlobeStart.png",
        State.BUILD1:        "GlobeSelected.png",
        State.BUILD2:        "02_build2.png",
        State.NULL_OBJECT:   "03_null_object.png",
        State.INTERVAL_AXIS: "04_interval_axis.png",
        State.BAR_SELECTED:  "05_bar_selected.png",
        # … weitere States
    }
    
    sm = ScreenManager(png_folder, png_map)
    im = InteractionManager(sm)  # wie vorher definiert
    clock = pygame.time.Clock()

    running = True
    while running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            action = map_input_to_action(ev)
            if action and im.handle(action):
                # State-Wechsel: hier könntest Du Sound/Animation triggern
                pass

        # immer aktuellen PNG-Screen rendern
        surf = sm.get_screen(im.state)
        screen.blit(surf, (0, 0))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    run_app("final-prototype/screens")  # z.B. Dein Ordner mit den PNGs
