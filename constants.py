"""
PacMan Game Constants
All game constants, colors, and configuration values
"""

# === Display Settings ===
BLOCK_SIZE = 24
FPS = 60  # Increased from 10 for smoother gameplay
FONT_SIZE = 48

# === Game Settings ===
POWERUP_DURATION = 5000  # 5 seconds in milliseconds
START_LIVES = 3
GHOST_MOVE_DELAY = 3  # Frames between ghost movements (reduced for 60 FPS)
PACMAN_MOUTH_DURATION = 100  # Milliseconds for mouth animation (reduced for smoother animation)
GHOST_RESPAWN_INVISIBILITY_DURATION = 2000  # 2 seconds invisibility after respawn

# === Scoring ===
POINTS_PER_DOT = 10
POINTS_PER_GHOST = 50
POINTS_PER_POWER_PELLET = 20

# === Level Layout ===
LEVEL_LAYOUT = [
    "############################",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#.####.#####.##.#####.####.#",
    "#.......P..................#",
    "#.####.##.########.##.####.#",
    "#.####.##.########.##.####.#",
    "#......##....##....##......#",
    "######.##### ## #####.######",
    "######.##### ## #####.######",
    "#............##............#",
    "############################",
]

# === Dynamically calculated dimensions ===
GRID_HEIGHT = len(LEVEL_LAYOUT)
GRID_WIDTH = len(LEVEL_LAYOUT[0])
WINDOW_WIDTH = BLOCK_SIZE * GRID_WIDTH
WINDOW_HEIGHT = BLOCK_SIZE * GRID_HEIGHT
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)

# === Colors (RGB) ===
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
PINK = (255, 192, 203)
GRAY = (128, 128, 128)

# === Game States ===
STATE_START = "start"
STATE_PLAYING = "playing"
STATE_PAUSED = "paused"
STATE_GAMEOVER = "gameover"
STATE_WIN = "win"
STATE_HELP = "help"

# === Key Bindings ===
KEY_UP = ['w', 'up']
KEY_DOWN = ['s', 'down']  
KEY_LEFT = ['a', 'left']
KEY_RIGHT = ['d', 'right']
KEY_PAUSE = 'p'
KEY_HELP = 'h'
KEY_ENTER = 'return'

# === Ghost Colors ===
GHOST_COLORS = [RED, GREEN, PURPLE, ORANGE]

# === Pacman Starting Position ===
PACMAN_START_X = 1
PACMAN_START_Y = 1

# === Ghost Starting Positions ===
GHOST_START_POSITIONS = [
    (13, 11),
    (15, 11), 
    (13, 13),
    (14, 11)
]

# === File Paths ===
HIGHSCORE_FILE = "highscore.txt"

# === UI Settings ===
TITLE_OFFSET_Y = -50
SUBTITLE_OFFSET_Y = 0
HELP_TEXT_SPACING = 30
SCORE_DISPLAY_X = 10
SCORE_DISPLAY_Y = 10
LIVES_DISPLAY_Y = 50
TIMER_DISPLAY_X = 250