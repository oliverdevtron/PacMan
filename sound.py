"""
PacMan Sound Effects Management
Handles all game sound effects and audio
"""

import pygame
import sys

class SoundManager:
    """Manages all sound effects for the PacMan game"""
    
    def __init__(self):
        """Initialize the sound manager"""
        self.sounds_enabled = True
        self.sounds = {}
        self._init_pygame_mixer()
        self._create_sound_effects()
    
    def _init_pygame_mixer(self):
        """Initialize pygame mixer for sound effects"""
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        except pygame.error as e:
            print(f"Warning: Could not initialize sound system: {e}")
            self.sounds_enabled = False
    
    def _create_sound_effects(self):
        """Create simple sound effects using pygame's sound generation"""
        if not self.sounds_enabled:
            return
            
        try:
            # Create sound effects using simple waveforms
            self.sounds['point'] = self._create_tone(800, 0.1, volume=0.3)
            self.sounds['powerup'] = self._create_tone(400, 0.3, volume=0.4) 
            self.sounds['death'] = self._create_descending_tone(600, 200, 0.5, volume=0.4)
            self.sounds['ghost'] = self._create_tone(300, 0.2, volume=0.3)
            self.sounds['game_start'] = self._create_ascending_tone(200, 600, 0.4, volume=0.3)
            self.sounds['game_over'] = self._create_descending_tone(500, 100, 0.8, volume=0.4)
            self.sounds['level_complete'] = self._create_ascending_tone(400, 800, 0.6, volume=0.4)
        except Exception as e:
            print(f"Warning: Could not create sound effects: {e}")
            self.sounds_enabled = False
    
    def _create_tone(self, frequency, duration, volume=0.5):
        """Create a simple tone sound effect"""
        try:
            sample_rate = 22050
            frames = int(duration * sample_rate)
            arr = []
            
            for i in range(frames):
                time = float(i) / sample_rate
                wave = 4096 * volume * (0.5 * pygame.math.Vector2(1, 0).rotate(frequency * 360 * time).x)
                arr.append([int(wave), int(wave)])
            
            sound = pygame.sndarray.make_sound(pygame.array.array('i', arr))
            return sound
        except:
            return None
    
    def _create_ascending_tone(self, start_freq, end_freq, duration, volume=0.5):
        """Create an ascending tone sound effect"""
        try:
            sample_rate = 22050
            frames = int(duration * sample_rate)
            arr = []
            
            for i in range(frames):
                time = float(i) / sample_rate
                progress = time / duration
                frequency = start_freq + (end_freq - start_freq) * progress
                wave = 4096 * volume * (0.5 * pygame.math.Vector2(1, 0).rotate(frequency * 360 * time).x)
                arr.append([int(wave), int(wave)])
            
            sound = pygame.sndarray.make_sound(pygame.array.array('i', arr))
            return sound
        except:
            return None
    
    def _create_descending_tone(self, start_freq, end_freq, duration, volume=0.5):
        """Create a descending tone sound effect"""
        try:
            sample_rate = 22050
            frames = int(duration * sample_rate)
            arr = []
            
            for i in range(frames):
                time = float(i) / sample_rate
                progress = time / duration
                frequency = start_freq - (start_freq - end_freq) * progress
                wave = 4096 * volume * (0.5 * pygame.math.Vector2(1, 0).rotate(frequency * 360 * time).x)
                arr.append([int(wave), int(wave)])
            
            sound = pygame.sndarray.make_sound(pygame.array.array('i', arr))
            return sound
        except:
            return None
    
    def play_sound(self, sound_name):
        """Play a sound effect by name"""
        if not self.sounds_enabled or sound_name not in self.sounds:
            return
            
        sound = self.sounds[sound_name]
        if sound:
            try:
                sound.play()
            except pygame.error:
                pass  # Ignore sound errors
    
    def play_point_sound(self):
        """Play sound when collecting a point"""
        self.play_sound('point')
    
    def play_powerup_sound(self):
        """Play sound when collecting a power pellet"""
        self.play_sound('powerup')
    
    def play_death_sound(self):
        """Play sound when Pacman dies"""
        self.play_sound('death')
    
    def play_ghost_sound(self):
        """Play sound when eating a ghost"""
        self.play_sound('ghost')
    
    def play_game_start_sound(self):
        """Play sound when game starts"""
        self.play_sound('game_start')
    
    def play_game_over_sound(self):
        """Play sound when game is over"""
        self.play_sound('game_over')
    
    def play_level_complete_sound(self):
        """Play sound when level is completed"""
        self.play_sound('level_complete')
    
    def enable_sounds(self):
        """Enable sound effects"""
        self.sounds_enabled = True
    
    def disable_sounds(self):
        """Disable sound effects"""
        self.sounds_enabled = False
    
    def toggle_sounds(self):
        """Toggle sound effects on/off"""
        self.sounds_enabled = not self.sounds_enabled

# Global sound manager instance
sound_manager = None

def get_sound_manager():
    """Get or create the global sound manager instance"""
    global sound_manager
    if sound_manager is None:
        sound_manager = SoundManager()
    return sound_manager