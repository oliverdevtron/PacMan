"""
PacMan UI Components
Handles help screen, highscore display, and other UI elements
"""

import pygame
import os
from constants import *

class HighScoreManager:
    """Manages highscore persistence and display"""
    
    def __init__(self):
        self.highscore = self.load_highscore()
    
    def load_highscore(self):
        """Load highscore from file"""
        try:
            if os.path.exists(HIGHSCORE_FILE):
                with open(HIGHSCORE_FILE, 'r') as f:
                    return int(f.read().strip())
        except (ValueError, IOError):
            pass
        return 0
    
    def save_highscore(self, score):
        """Save new highscore if it's higher than current"""
        if score > self.highscore:
            self.highscore = score
            try:
                with open(HIGHSCORE_FILE, 'w') as f:
                    f.write(str(score))
                return True  # New highscore achieved
            except IOError:
                pass
        return False
    
    def get_highscore(self):
        """Get current highscore"""
        return self.highscore

class UIRenderer:
    """Handles rendering of UI elements"""
    
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.highscore_manager = HighScoreManager()
    
    def draw_text(self, text, color, x, y, center=True):
        """Draw text on screen"""
        rendered = self.font.render(text, True, color)
        if center:
            rect = rendered.get_rect(center=(x, y))
            self.screen.blit(rendered, rect)
        else:
            self.screen.blit(rendered, (x, y))
        return rendered.get_rect()
    
    def draw_start_screen(self):
        """Draw the start screen"""
        center_x = WINDOW_WIDTH // 2
        center_y = WINDOW_HEIGHT // 2
        
        # Title
        self.draw_text("PAC-MAN", YELLOW, center_x, center_y + TITLE_OFFSET_Y)
        
        # Instructions
        self.draw_text("Press Enter to Start", WHITE, center_x, center_y + SUBTITLE_OFFSET_Y)
        self.draw_text("Press H for Help", WHITE, center_x, center_y + SUBTITLE_OFFSET_Y + 40)
        
        # Highscore
        highscore = self.highscore_manager.get_highscore()
        if highscore > 0:
            self.draw_text(f"High Score: {highscore}", GREEN, center_x, center_y + SUBTITLE_OFFSET_Y + 80)
    
    def draw_help_screen(self):
        """Draw the help/controls screen"""
        center_x = WINDOW_WIDTH // 2
        start_y = WINDOW_HEIGHT // 4
        
        # Title
        self.draw_text("CONTROLS", YELLOW, center_x, start_y)
        
        # Controls
        controls = [
            "WASD or Arrow Keys - Move Pacman",
            "P - Pause/Unpause",
            "H - Show/Hide Help",
            "Enter - Start Game/Restart",
            "",
            "GAME RULES:",
            "• Collect all dots to win",
            "• Avoid ghosts (red, green, purple, orange)", 
            "• Eat power pellets (large purple dots)",
            "• When powered up, you can eat ghosts",
            "• You have 3 lives",
            "",
            "Press H to return to game"
        ]
        
        y_offset = start_y + 50
        for i, line in enumerate(controls):
            color = WHITE if line and not line.startswith("•") else CYAN if line.startswith("•") else GRAY
            if line:  # Don't draw empty lines
                self.draw_text(line, color, center_x, y_offset + i * HELP_TEXT_SPACING)
    
    def draw_game_ui(self, score, lives, powered_up=False, powerup_end_time=0):
        """Draw game UI elements (score, lives, timer)"""
        # Score
        score_text = self.font.render(f"Score: {score}", True, WHITE)
        self.screen.blit(score_text, (SCORE_DISPLAY_X, SCORE_DISPLAY_Y))
        
        # Lives
        lives_text = self.font.render(f"Lives: {lives}", True, WHITE)
        self.screen.blit(lives_text, (SCORE_DISPLAY_X, LIVES_DISPLAY_Y))
        
        # Power-up timer
        if powered_up and powerup_end_time > pygame.time.get_ticks():
            remaining = (powerup_end_time - pygame.time.get_ticks()) // 1000
            timer_text = self.font.render(f"Power: {remaining}s", True, PURPLE)
            self.screen.blit(timer_text, (WINDOW_WIDTH - TIMER_DISPLAY_X, SCORE_DISPLAY_Y))
    
    def draw_pause_screen(self):
        """Draw pause overlay"""
        center_x = WINDOW_WIDTH // 2
        center_y = WINDOW_HEIGHT // 2
        
        # Semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Pause text
        self.draw_text("PAUSED", RED, center_x, center_y)
        self.draw_text("Press P to continue", WHITE, center_x, center_y + 50)
    
    def draw_game_over_screen(self, score, is_new_highscore=False):
        """Draw game over screen"""
        center_x = WINDOW_WIDTH // 2
        center_y = WINDOW_HEIGHT // 2
        
        self.draw_text("GAME OVER", RED, center_x, center_y + TITLE_OFFSET_Y)
        self.draw_text(f"Final Score: {score}", WHITE, center_x, center_y)
        
        if is_new_highscore:
            self.draw_text("NEW HIGH SCORE!", GREEN, center_x, center_y + 40)
        
        highscore = self.highscore_manager.get_highscore()
        self.draw_text(f"High Score: {highscore}", GREEN, center_x, center_y + 80)
        self.draw_text("Press Enter to Restart", WHITE, center_x, center_y + 120)
    
    def draw_win_screen(self, score, is_new_highscore=False):
        """Draw win screen"""
        center_x = WINDOW_WIDTH // 2
        center_y = WINDOW_HEIGHT // 2
        
        self.draw_text("YOU WIN!", GREEN, center_x, center_y + TITLE_OFFSET_Y)
        self.draw_text(f"Final Score: {score}", WHITE, center_x, center_y)
        
        if is_new_highscore:
            self.draw_text("NEW HIGH SCORE!", GREEN, center_x, center_y + 40)
        
        highscore = self.highscore_manager.get_highscore()
        self.draw_text(f"High Score: {highscore}", GREEN, center_x, center_y + 80)
        self.draw_text("Press Enter to Play Again", WHITE, center_x, center_y + 120)
    
    def update_highscore(self, score):
        """Update highscore and return True if new highscore"""
        return self.highscore_manager.save_highscore(score)
    
    def get_highscore(self):
        """Get current highscore"""
        return self.highscore_manager.get_highscore()