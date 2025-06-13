import pygame
import sys
import random
import time

# === Globale Konstanten und Farben ===
BLOCK_SIZE = 24
FPS = 10  # Basis-Framerate (kann für flüssigere Animationen angepasst werden)

# Level-Layout (als Beispiel)
level_layout = [
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

# Dynamisch berechne Breite und Höhe basierend auf dem Layout
GRID_HEIGHT = len(level_layout)
GRID_WIDTH = len(level_layout[0])
WINDOW_WIDTH = BLOCK_SIZE * GRID_WIDTH
WINDOW_HEIGHT = BLOCK_SIZE * GRID_HEIGHT
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)

# Farben (RGB)
BLACK   = (0, 0, 0)
BLUE    = (0, 0, 255)
WHITE   = (255, 255, 255)
YELLOW  = (255, 255, 0)
RED     = (255, 0, 0)
GREEN   = (0, 255, 0)
PURPLE  = (255, 0, 255)
CYAN    = (0, 255, 255)

# Power-Up Dauer (in Millisekunden) und Startleben
POWERUP_DURATION = 5000  # 5 Sekunden
START_LIVES = 3

# === Pygame-Initialisierung ===
pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Pac-Man")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)

# === Level-Klasse ===
class Level:
    def __init__(self, layout):
        # Erstelle eine Kopie des Layouts
        self.layout = layout.copy()
        self.width = len(self.layout[0])
        self.height = len(self.layout)

    def draw(self, surface):
        for y, row in enumerate(self.layout):
            for x, ch in enumerate(row):
                rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                if ch == "#":
                    pygame.draw.rect(surface, BLUE, rect)
                elif ch == ".":
                    pygame.draw.circle(surface, WHITE, rect.center, 4)
                elif ch == "P":
                    pygame.draw.circle(surface, PURPLE, rect.center, BLOCK_SIZE // 2 - 2)

    def is_wall(self, x, y):
        # Außerhalb des Levels immer als Wand
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return True
        return self.layout[y][x] == "#"

    def collect_item(self, x, y):
        """Überprüft, ob an Position (x, y) ein Punkt (.) oder Power-Pill (P) liegt.
           Entfernt diesen und gibt 'point' oder 'power' zurück, ansonsten None."""
        row = self.layout[y]
        if row[x] == ".":
            self.layout[y] = row[:x] + " " + row[x+1:]
            return "point"
        elif row[x] == "P":
            self.layout[y] = row[:x] + " " + row[x+1:]
            return "power"
        return None

    def is_complete(self):
        # Das Level ist abgeschlossen, wenn kein Punkt und kein Power-Up mehr vorhanden sind
        for row in self.layout:
            if "." in row or "P" in row:
                return False
        return True

# === Basis-Klasse für bewegliche Objekte ===
class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.grid_x = x
        self.grid_y = y
        self.image = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.update_position()

    def update_position(self):
        self.rect.topleft = (self.grid_x * BLOCK_SIZE, self.grid_y * BLOCK_SIZE)

# === Pacman-Klasse ===
class Pacman(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.mouth_open = True
        self.mouth_timer = pygame.time.get_ticks()
        self.mouth_duration = 200  # Millisekunden
        self.powered_up = False
        self.powerup_end_time = 0

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.mouth_timer > self.mouth_duration:
            self.mouth_open = not self.mouth_open
            self.mouth_timer = current_time
        self.draw()

        if self.powered_up and current_time > self.powerup_end_time:
            self.powered_up = False

    def draw(self):
        self.image.fill((0, 0, 0, 0))
        center = (BLOCK_SIZE // 2, BLOCK_SIZE // 2)
        pygame.draw.circle(self.image, YELLOW, center, BLOCK_SIZE // 2)
        if self.mouth_open:
            mouth = [center, (BLOCK_SIZE, 0), (BLOCK_SIZE, BLOCK_SIZE)]
            pygame.draw.polygon(self.image, BLACK, mouth)

    def move(self, dx, dy, level):
        new_x = self.grid_x + dx
        new_y = self.grid_y + dy
        if not level.is_wall(new_x, new_y):
            self.grid_x = new_x
            self.grid_y = new_y
            self.update_position()

# === Ghost-Klasse ===
class Ghost(GameObject):
    def __init__(self, x, y, color, start_pos):
        super().__init__(x, y)
        self.color = color
        self.direction = random.choice(['up', 'down', 'left', 'right'])
        self.move_delay = 5  # Frames zwischen Bewegungen
        self.move_counter = 0
        self.frightened = False  # Bei Pacman-Powerup
        self.start_pos = start_pos  # Startposition für den Respawn

    def update(self, level, pacman):
        self.move_counter += 1
        if self.move_counter < self.move_delay:
            return
        self.move_counter = 0

        possible_dirs = []
        for d in ['up', 'down', 'left', 'right']:
            nx, ny = self.get_new_position(d)
            if not level.is_wall(nx, ny):
                possible_dirs.append(d)
        if possible_dirs:
            if self.frightened:
                best_dir = max(possible_dirs, key=lambda d: self.manhattan_distance(self.get_new_position(d), (pacman.grid_x, pacman.grid_y)))
            else:
                best_dir = min(possible_dirs, key=lambda d: self.manhattan_distance(self.get_new_position(d), (pacman.grid_x, pacman.grid_y)))
            if random.random() < 0.1:
                best_dir = random.choice(possible_dirs)
            self.direction = best_dir
            nx, ny = self.get_new_position(self.direction)
            if not level.is_wall(nx, ny):
                self.grid_x = nx
                self.grid_y = ny
                self.update_position()
        self.draw()

    def get_new_position(self, direction):
        if direction == 'up':
            return self.grid_x, self.grid_y - 1
        elif direction == 'down':
            return self.grid_x, self.grid_y + 1
        elif direction == 'left':
            return self.grid_x - 1, self.grid_y
        elif direction == 'right':
            return self.grid_x + 1, self.grid_y
        return self.grid_x, self.grid_y

    def manhattan_distance(self, pos, target):
        return abs(pos[0] - target[0]) + abs(pos[1] - target[1])

    def draw(self):
        self.image.fill((0, 0, 0, 0))
        center = (BLOCK_SIZE // 2, BLOCK_SIZE // 2)
        draw_color = CYAN if self.frightened else self.color
        pygame.draw.circle(self.image, draw_color, center, BLOCK_SIZE // 2)
        pygame.draw.rect(self.image, draw_color, pygame.Rect(BLOCK_SIZE // 4, BLOCK_SIZE // 2, BLOCK_SIZE // 2, BLOCK_SIZE // 2))

    def respawn(self):
        self.grid_x, self.grid_y = self.start_pos
        self.frightened = False
        self.direction = random.choice(['up', 'down', 'left', 'right'])
        self.update_position()

# === Game-Klasse ===
class Game:
    def __init__(self):
        self.level = Level(level_layout)
        self.pacman = Pacman(1, 1)
        self.ghosts = pygame.sprite.Group()
        self.ghosts.add(Ghost(13, 11, RED, (13, 11)))
        self.ghosts.add(Ghost(15, 11, GREEN, (15, 11)))
        self.ghosts.add(Ghost(13, 13, PURPLE, (13, 13)))
        self.all_sprites = pygame.sprite.Group(self.pacman, *self.ghosts)
        self.score = 0
        self.lives = START_LIVES
        self.state = "start"  # Zustände: start, playing, paused, gameover, win
        self.powerup_end_time = 0

    def reset(self):
        self.level = Level(level_layout)
        self.pacman.grid_x, self.pacman.grid_y = 1, 1
        self.pacman.update_position()
        self.pacman.powered_up = False
        for ghost in self.ghosts:
            ghost.respawn()
        self.score = 0
        self.lives = START_LIVES
        self.state = "playing"

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if self.state == "start":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.state = "playing"
            elif self.state == "playing":
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_w, pygame.K_UP):
                        self.pacman.move(0, -1, self.level)
                    elif event.key in (pygame.K_s, pygame.K_DOWN):
                        self.pacman.move(0, 1, self.level)
                    elif event.key in (pygame.K_a, pygame.K_LEFT):
                        self.pacman.move(-1, 0, self.level)
                    elif event.key in (pygame.K_d, pygame.K_RIGHT):
                        self.pacman.move(1, 0, self.level)
                    elif event.key == pygame.K_p:
                        self.state = "paused"
            elif self.state == "paused":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    self.state = "playing"
            elif self.state in ["gameover", "win"]:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.reset()

    def update(self):
        if self.state == "playing":
            self.pacman.update()
            result = self.level.collect_item(self.pacman.grid_x, self.pacman.grid_y)
            if result == "point":
                self.score += 10
            elif result == "power":
                self.activate_powerup()

            if self.level.is_complete():
                self.state = "win"

            for ghost in self.ghosts:
                if ghost.frightened and pygame.time.get_ticks() > self.powerup_end_time:
                    ghost.frightened = False
                ghost.update(self.level, self.pacman)

            if pygame.sprite.spritecollide(self.pacman, self.ghosts, False):
                if self.pacman.powered_up:
                    for ghost in pygame.sprite.spritecollide(self.pacman, self.ghosts, False):
                        self.score += 50
                        ghost.respawn()
                else:
                    self.lives -= 1
                    self.pacman.grid_x, self.pacman.grid_y = 1, 1
                    self.pacman.update_position()
                    if self.lives <= 0:
                        self.state = "gameover"

    def activate_powerup(self):
        self.pacman.powered_up = True
        self.powerup_end_time = pygame.time.get_ticks() + POWERUP_DURATION
        for ghost in self.ghosts:
            ghost.frightened = True

    def draw_text(self, text, color, x, y):
        rendered = font.render(text, True, color)
        rect = rendered.get_rect(center=(x, y))
        screen.blit(rendered, rect)

    def draw_start_screen(self):
        self.draw_text("Pac-Man", YELLOW, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50)
        self.draw_text("Press Enter to Start", WHITE, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

    def draw_score(self):
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        lives_text = font.render(f"Lives: {self.lives}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 50))

    def draw_powerup_timer(self):
        remaining = (self.powerup_end_time - pygame.time.get_ticks()) // 1000
        timer_text = font.render(f"Invincible: {remaining}", True, PURPLE)
        screen.blit(timer_text, (WINDOW_WIDTH - 250, 10))

    def draw(self):
        screen.fill(BLACK)
        if self.state == "start":
            self.draw_start_screen()
        elif self.state == "playing":
            self.level.draw(screen)
            self.all_sprites.draw(screen)
            self.draw_score()
            if self.pacman.powered_up:
                self.draw_powerup_timer()
        elif self.state == "paused":
            self.level.draw(screen)
            self.all_sprites.draw(screen)
            self.draw_score()
            self.draw_text("Paused", RED, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        elif self.state == "gameover":
            self.draw_text("Game Over", RED, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
            self.draw_text(f"Score: {self.score}", WHITE, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50)
            self.draw_text("Press Enter to Restart", WHITE, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100)
        elif self.state == "win":
            self.draw_text("You Win!", GREEN, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
            self.draw_text(f"Score: {self.score}", WHITE, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50)
            self.draw_text("Press Enter to Restart", WHITE, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100)
        pygame.display.flip()

    def run(self):
        while True:
            clock.tick(FPS)
            self.process_events()
            if self.state == "playing":
                self.update()
            self.draw()

# === Main-Funktion ===
def main():
    game = Game()
    # Startbildschirm anzeigen
    while game.state == "start":
        game.process_events()
        game.draw()
        clock.tick(FPS)
    game.run()

if __name__ == "__main__":
    main()
