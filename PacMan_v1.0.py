"""
PacMan v1.0
Designed by:
  ██████  ██       ██  ██    ██ ███████ ██████  
 ██    ██ ██       ██  ██    ██ ██      ██   ██ 
 ██    ██ ██       ██  ██    ██ █████   ██████  
 ██    ██ ██       ██   ██  ██  ██      ██   ██ 
  ██████  ███████  ██    ████   ███████ ██   ██ 
(c) 2025 by oliver@devtron.pro

Refactored modular version with enhanced features:
- Sound effects
- Smooth animations
- Help screen
- Highscore system
- Improved user experience
"""

import pygame
import sys
import random
import time

# Import our modules
from constants import *
from sound import get_sound_manager
from ui import UIRenderer

# === Pygame Initialization ===
pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Pac-Man")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, FONT_SIZE)

# Initialize managers
sound_manager = get_sound_manager()
ui_renderer = UIRenderer(screen, font)

# === Level Class ===
class Level:
    """Represents the game level with walls, dots, and power pellets"""
    
    def __init__(self, layout):
        """Initialize level with layout"""
        # Create a copy of the layout
        self.layout = layout.copy()
        self.width = len(self.layout[0])
        self.height = len(self.layout)

    def draw(self, surface):
        """Draw the level on the given surface"""
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
        """Check if position (x, y) is a wall"""
        # Outside the level is always a wall
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return True
        return self.layout[y][x] == "#"

    def collect_item(self, x, y):
        """Check if there's a dot (.) or power pellet (P) at position (x, y).
           Removes it and returns 'point' or 'power', otherwise None."""
        row = self.layout[y]
        if row[x] == ".":
            self.layout[y] = row[:x] + " " + row[x+1:]
            return "point"
        elif row[x] == "P":
            self.layout[y] = row[:x] + " " + row[x+1:]
            return "power"
        return None

    def is_complete(self):
        """Check if level is complete (no dots or power pellets remaining)"""
        for row in self.layout:
            if "." in row or "P" in row:
                return False
        return True

# === Base Class for Moveable Objects ===
class GameObject(pygame.sprite.Sprite):
    """Base class for game objects like Pacman and ghosts"""
    
    def __init__(self, x, y):
        """Initialize game object at grid position (x, y)"""
        super().__init__()
        self.grid_x = x
        self.grid_y = y
        self.image = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.update_position()

    def update_position(self):
        """Update sprite position based on grid coordinates"""
        self.rect.topleft = (self.grid_x * BLOCK_SIZE, self.grid_y * BLOCK_SIZE)

# === Pacman Class ===
class Pacman(GameObject):
    """The player character - Pacman"""
    
    def __init__(self, x, y):
        """Initialize Pacman at given position"""
        super().__init__(x, y)
        self.mouth_open = True
        self.mouth_timer = pygame.time.get_ticks()
        self.direction = 'right'  # Track current direction for mouth orientation

    def update(self):
        """Update Pacman animation and state"""
        current_time = pygame.time.get_ticks()
        if current_time - self.mouth_timer > PACMAN_MOUTH_DURATION:
            self.mouth_open = not self.mouth_open
            self.mouth_timer = current_time
        self.draw()

    def draw(self):
        """Draw Pacman with animated mouth"""
        self.image.fill((0, 0, 0, 0))
        center = (BLOCK_SIZE // 2, BLOCK_SIZE // 2)
        pygame.draw.circle(self.image, YELLOW, center, BLOCK_SIZE // 2)
        
        if self.mouth_open:
            # Draw mouth based on direction
            mouth_points = self._get_mouth_points(center)
            if mouth_points:
                pygame.draw.polygon(self.image, BLACK, mouth_points)

    def _get_mouth_points(self, center):
        """Get mouth triangle points based on direction"""
        if self.direction == 'right':
            return [center, (BLOCK_SIZE, 0), (BLOCK_SIZE, BLOCK_SIZE)]
        elif self.direction == 'left':
            return [center, (0, 0), (0, BLOCK_SIZE)]
        elif self.direction == 'up':
            return [center, (0, 0), (BLOCK_SIZE, 0)]
        elif self.direction == 'down':
            return [center, (0, BLOCK_SIZE), (BLOCK_SIZE, BLOCK_SIZE)]
        return None

    def move(self, dx, dy, level):
        """Move Pacman in given direction if possible"""
        new_x = self.grid_x + dx
        new_y = self.grid_y + dy
        if not level.is_wall(new_x, new_y):
            self.grid_x = new_x
            self.grid_y = new_y
            # Update direction for mouth animation
            if dx > 0:
                self.direction = 'right'
            elif dx < 0:
                self.direction = 'left'
            elif dy > 0:
                self.direction = 'down'
            elif dy < 0:
                self.direction = 'up'
            self.update_position()
            return True
        return False

    def reset_position(self):
        """Reset Pacman to starting position"""
        self.grid_x = PACMAN_START_X
        self.grid_y = PACMAN_START_Y
        self.direction = 'right'
        self.update_position()

# === Ghost Class ===
class Ghost(GameObject):
    """AI-controlled ghost enemy"""
    
    def __init__(self, x, y, color, start_pos):
        """Initialize ghost with color and starting position"""
        super().__init__(x, y)
        self.color = color
        self.direction = random.choice(['up', 'down', 'left', 'right'])
        self.move_delay = GHOST_MOVE_DELAY  # Frames between movements
        self.move_counter = 0
        self.frightened = False  # When Pacman has powerup
        self.start_pos = start_pos  # Starting position for respawn
        self.invisible = False  # Invisible period after respawn
        self.invisible_end_time = 0

    def update(self, level, pacman):
        """Update ghost AI and movement"""
        self.move_counter += 1
        if self.move_counter < self.move_delay:
            return
        self.move_counter = 0

        # Check invisibility period
        if self.invisible and pygame.time.get_ticks() > self.invisible_end_time:
            self.invisible = False

        possible_dirs = []
        for d in ['up', 'down', 'left', 'right']:
            nx, ny = self.get_new_position(d)
            if not level.is_wall(nx, ny):
                possible_dirs.append(d)
        
        if possible_dirs:
            if self.frightened:
                # Run away from Pacman
                best_dir = max(possible_dirs, key=lambda d: 
                    self.manhattan_distance(self.get_new_position(d), (pacman.grid_x, pacman.grid_y)))
            else:
                # Chase Pacman
                best_dir = min(possible_dirs, key=lambda d: 
                    self.manhattan_distance(self.get_new_position(d), (pacman.grid_x, pacman.grid_y)))
            
            # Add some randomness (10% chance)
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
        """Get new position based on direction"""
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
        """Calculate Manhattan distance between two positions"""
        return abs(pos[0] - target[0]) + abs(pos[1] - target[1])

    def draw(self):
        """Draw the ghost"""
        self.image.fill((0, 0, 0, 0))
        
        # Don't draw if invisible
        if self.invisible:
            return
            
        center = (BLOCK_SIZE // 2, BLOCK_SIZE // 2)
        draw_color = CYAN if self.frightened else self.color
        pygame.draw.circle(self.image, draw_color, center, BLOCK_SIZE // 2)
        pygame.draw.rect(self.image, draw_color, 
                        pygame.Rect(BLOCK_SIZE // 4, BLOCK_SIZE // 2, BLOCK_SIZE // 2, BLOCK_SIZE // 2))

    def respawn(self):
        """Respawn ghost at starting position with invisibility period"""
        self.grid_x, self.grid_y = self.start_pos
        self.frightened = False
        self.direction = random.choice(['up', 'down', 'left', 'right'])
        self.invisible = True
        self.invisible_end_time = pygame.time.get_ticks() + GHOST_RESPAWN_INVISIBILITY_DURATION
        self.update_position()
        
    def set_frightened(self, frightened):
        """Set frightened state"""
        self.frightened = frightened

# === Game Class ===
class Game:
    """Main game controller with improved features"""
    
    def __init__(self):
        """Initialize the game"""
        self.level = Level(LEVEL_LAYOUT)
        self.pacman = Pacman(PACMAN_START_X, PACMAN_START_Y)
        self.ghosts = pygame.sprite.Group()
        
        # Create ghosts with different colors
        for i, (start_pos, color) in enumerate(zip(GHOST_START_POSITIONS, GHOST_COLORS)):
            self.ghosts.add(Ghost(start_pos[0], start_pos[1], color, start_pos))
            
        self.all_sprites = pygame.sprite.Group(self.pacman, *self.ghosts)
        self.score = 0
        self.lives = START_LIVES
        self.state = STATE_START
        
        # Centralized powerup management (moved from Pacman class)
        self.powerup_active = False
        self.powerup_end_time = 0
        self.is_new_highscore = False

    def reset(self):
        """Reset game to initial state"""
        self.level = Level(LEVEL_LAYOUT)
        self.pacman.reset_position()
        
        # Reset all ghosts
        for ghost in self.ghosts:
            ghost.respawn()
            
        self.score = 0
        self.lives = START_LIVES
        self.powerup_active = False
        self.powerup_end_time = 0
        self.is_new_highscore = False
        self.state = STATE_PLAYING
        
        # Play game start sound
        sound_manager.play_game_start_sound()

    def process_events(self):
        """Handle user input and events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if self.state == STATE_START:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.state = STATE_PLAYING
                        sound_manager.play_game_start_sound()
                    elif event.key == pygame.K_h:
                        self.state = STATE_HELP
                        
            elif self.state == STATE_HELP:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_h:
                    self.state = STATE_START
                    
            elif self.state == STATE_PLAYING:
                if event.type == pygame.KEYDOWN:
                    moved = False
                    if event.key in (pygame.K_w, pygame.K_UP):
                        moved = self.pacman.move(0, -1, self.level)
                    elif event.key in (pygame.K_s, pygame.K_DOWN):
                        moved = self.pacman.move(0, 1, self.level)
                    elif event.key in (pygame.K_a, pygame.K_LEFT):
                        moved = self.pacman.move(-1, 0, self.level)
                    elif event.key in (pygame.K_d, pygame.K_RIGHT):
                        moved = self.pacman.move(1, 0, self.level)
                    elif event.key == pygame.K_p:
                        self.state = STATE_PAUSED
                    elif event.key == pygame.K_h:
                        self.state = STATE_HELP
                        
            elif self.state == STATE_PAUSED:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.state = STATE_PLAYING
                    elif event.key == pygame.K_h:
                        self.state = STATE_HELP
                        
            elif self.state in [STATE_GAMEOVER, STATE_WIN]:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.reset()

    def update(self):
        """Update game logic"""
        if self.state == STATE_PLAYING:
            self.pacman.update()
            
            # Check item collection
            result = self.level.collect_item(self.pacman.grid_x, self.pacman.grid_y)
            if result == "point":
                self.score += POINTS_PER_DOT
                sound_manager.play_point_sound()
            elif result == "power":
                self.score += POINTS_PER_POWER_PELLET
                self.activate_powerup()
                sound_manager.play_powerup_sound()

            # Check level completion
            if self.level.is_complete():
                self.state = STATE_WIN
                self.is_new_highscore = ui_renderer.update_highscore(self.score)
                sound_manager.play_level_complete_sound()

            # Update powerup state
            if self.powerup_active and pygame.time.get_ticks() > self.powerup_end_time:
                self.deactivate_powerup()

            # Update ghosts
            for ghost in self.ghosts:
                ghost.update(self.level, self.pacman)

            # Check collisions with ghosts
            collided_ghosts = pygame.sprite.spritecollide(self.pacman, self.ghosts, False)
            for ghost in collided_ghosts:
                # Skip collision with invisible ghosts
                if ghost.invisible:
                    continue
                    
                if self.powerup_active:
                    # Eat the ghost
                    self.score += POINTS_PER_GHOST
                    ghost.respawn()
                    sound_manager.play_ghost_sound()
                else:
                    # Pacman dies
                    self.lives -= 1
                    self.pacman.reset_position()
                    sound_manager.play_death_sound()
                    
                    if self.lives <= 0:
                        self.state = STATE_GAMEOVER
                        self.is_new_highscore = ui_renderer.update_highscore(self.score)
                        sound_manager.play_game_over_sound()
                    break  # Only process one collision per frame

    def activate_powerup(self):
        """Activate powerup mode with proper stacking"""
        # Always extend powerup duration, even if already active (fixes stacking issue)
        self.powerup_active = True
        self.powerup_end_time = pygame.time.get_ticks() + POWERUP_DURATION
        
        # Set all ghosts to frightened
        for ghost in self.ghosts:
            ghost.set_frightened(True)
    
    def deactivate_powerup(self):
        """Deactivate powerup mode"""
        self.powerup_active = False
        
        # Remove frightened state from all ghosts
        for ghost in self.ghosts:
            ghost.set_frightened(False)

    def draw(self):
        """Draw the game"""
        screen.fill(BLACK)
        
        if self.state == STATE_START:
            ui_renderer.draw_start_screen()
        elif self.state == STATE_HELP:
            ui_renderer.draw_help_screen()
        elif self.state == STATE_PLAYING:
            self.level.draw(screen)
            self.all_sprites.draw(screen)
            ui_renderer.draw_game_ui(self.score, self.lives, self.powerup_active, self.powerup_end_time)
        elif self.state == STATE_PAUSED:
            self.level.draw(screen)
            self.all_sprites.draw(screen)
            ui_renderer.draw_game_ui(self.score, self.lives, self.powerup_active, self.powerup_end_time)
            ui_renderer.draw_pause_screen()
        elif self.state == STATE_GAMEOVER:
            ui_renderer.draw_game_over_screen(self.score, self.is_new_highscore)
        elif self.state == STATE_WIN:
            ui_renderer.draw_win_screen(self.score, self.is_new_highscore)
            
        pygame.display.flip()

    def run(self):
        """Main game loop"""
        while True:
            clock.tick(FPS)
            self.process_events()
            if self.state == STATE_PLAYING:
                self.update()
            self.draw()

# === Main Function ===
def main():
    """Main entry point for the PacMan game"""
    game = Game()
    # Start the game in start screen state
    game.run()

if __name__ == "__main__":
    main()
