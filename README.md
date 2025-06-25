# PacMan Game

A classic PacMan implementation built with Python and Pygame. Navigate through a maze, collect dots, avoid ghosts, and use power pills to turn the tables on your enemies!

## 🎮 Game Features

- **Classic PacMan Gameplay**: Navigate through a maze collecting dots while avoiding ghosts
- **Power-Up System**: Collect power pills (purple circles) to make ghosts frightened and edible for 5 seconds
- **AI Ghost Behavior**: Intelligent ghost movement using Manhattan distance pathfinding
- **Multiple Game States**: Start screen, gameplay, pause, game over, and victory screens
- **Score & Lives System**: Earn points for collecting dots (10 pts) and eating ghosts (50 pts), with 3 starting lives
- **Smooth Animations**: Animated PacMan mouth and responsive movement
- **Keyboard Controls**: Support for both WASD and arrow key controls

## 🎯 Game Mechanics

### Scoring System
- **Dots**: 10 points each
- **Eating Frightened Ghosts**: 50 points each
- **Objective**: Collect all dots and power pills to win the level

### Power-Up Mode
- Collect purple power pills to activate power-up mode
- Ghosts turn cyan and become frightened (try to avoid PacMan)
- PacMan can eat frightened ghosts during this time
- Power-up lasts for 5 seconds

### Ghost AI
- **Normal Mode**: Ghosts use Manhattan distance to chase PacMan
- **Frightened Mode**: Ghosts try to maximize distance from PacMan
- **Random Element**: 10% chance for random movement to add unpredictability
- **Collision Detection**: Lose a life when touching a ghost (unless powered up)

## 🛠️ Technical Requirements

- **Python**: 3.6 or higher
- **Pygame**: 2.0 or higher

## 📦 Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/oliverdevtron/PacMan.git
   cd PacMan
   ```

2. **Install Pygame**:
   ```bash
   pip install pygame
   ```

3. **Run the game**:
   ```bash
   python PacMan_v1.0.py
   ```

## 🎮 Controls

| Key | Action |
|-----|--------|
| **Enter** | Start game / Restart after game over |
| **Arrow Keys** or **WASD** | Move PacMan |
| **P** | Pause/Unpause game |
| **ESC** or **Close Window** | Quit game |

## 🏗️ Code Architecture

The game is structured using object-oriented programming with clear separation of concerns:

### Core Classes

#### `Level` Class
- **Purpose**: Manages the game board and level layout
- **Key Methods**:
  - `draw()`: Renders walls, dots, and power pills
  - `is_wall()`: Collision detection for walls
  - `collect_item()`: Handles dot/power pill collection
  - `is_complete()`: Checks if level is finished

#### `GameObject` Class (Base Class)
- **Purpose**: Base class for all moving game objects
- **Features**: Grid-based positioning and sprite management
- **Inheritance**: Extended by both `Pacman` and `Ghost` classes

#### `Pacman` Class
- **Purpose**: Player character implementation
- **Features**:
  - Animated mouth with timing system
  - Power-up state management
  - Movement validation and grid-based positioning
- **Key Methods**:
  - `update()`: Handles animation and power-up timing
  - `move()`: Validates and executes movement
  - `draw()`: Renders PacMan with mouth animation

#### `Ghost` Class
- **Purpose**: AI-controlled enemy characters
- **Features**:
  - Intelligent pathfinding using Manhattan distance
  - Frightened mode behavior during power-ups
  - Individual colors and starting positions
- **Key Methods**:
  - `update()`: AI movement logic and pathfinding
  - `manhattan_distance()`: Distance calculation for AI
  - `respawn()`: Reset to starting position

#### `Game` Class
- **Purpose**: Main game controller and state manager
- **Responsibilities**:
  - Game state management (start, playing, paused, gameover, win)
  - Event handling and input processing
  - Collision detection between game objects
  - Score tracking and lives management
  - Rendering coordination
- **Key Methods**:
  - `run()`: Main game loop
  - `update()`: Game logic updates
  - `process_events()`: Input handling
  - `draw()`: Coordinate all rendering

### Game Configuration

#### Constants & Settings
```python
BLOCK_SIZE = 24          # Size of each grid cell in pixels
FPS = 10                 # Game framerate
POWERUP_DURATION = 5000  # Power-up duration in milliseconds
START_LIVES = 3          # Starting number of lives
```

#### Level Layout
The game level is defined as a string array where:
- `#` = Walls (rendered as blue rectangles)
- `.` = Dots (rendered as white circles)
- `P` = Power pills (rendered as purple circles)
- ` ` = Empty space (walkable)

## 🎨 Visual Design

- **Grid-Based**: 24x24 pixel blocks for retro feel
- **Color Scheme**:
  - Walls: Blue (`#0000FF`)
  - PacMan: Yellow (`#FFFF00`)
  - Dots: White (`#FFFFFF`)
  - Power Pills: Purple (`#FF00FF`)
  - Ghosts: Red, Green, Purple (Cyan when frightened)
- **UI Elements**: Score, lives counter, and power-up timer

## 🚀 How to Extend

### Adding New Levels
1. Modify the `level_layout` array in the global constants section
2. Ensure the layout uses valid characters (`#`, `.`, `P`, ` `)
3. The grid dimensions are automatically calculated

### Adding More Ghosts
1. In the `Game.__init__()` method, add more ghosts to the `self.ghosts` group:
   ```python
   self.ghosts.add(Ghost(x, y, COLOR, (start_x, start_y)))
   ```

### Modifying Ghost AI
- Adjust `move_delay` in `Ghost.__init__()` for speed
- Modify the random movement probability (currently 10%)
- Implement different AI strategies in the `Ghost.update()` method

### Adding Sound Effects
1. Load sound files using `pygame.mixer.Sound()`
2. Play sounds at appropriate game events (eating dots, power-ups, etc.)

## 📋 Future Improvements

- [ ] Multiple levels with increasing difficulty
- [ ] Sound effects and background music
- [ ] High score persistence
- [ ] Different ghost personalities and behaviors
- [ ] Fruits and bonus items
- [ ] Improved graphics and animations
- [ ] Menu system with options
- [ ] Multiplayer support

## 👨‍💻 Developer Information

**Designed by**: oliver@devtron.pro  
**Copyright**: (c) 2025 by oliver@devtron.pro  
**License**: Open source

## 🐛 Troubleshooting

### Common Issues

1. **ModuleNotFoundError: No module named 'pygame'**
   - Solution: Install pygame with `pip install pygame`

2. **Game window doesn't appear**
   - Ensure you have a display available (not running headless)
   - Check that pygame is properly installed

3. **Performance issues**
   - Adjust the `FPS` constant for better performance
   - Close other applications that might be using graphics resources

## 🤝 Contributing

Feel free to fork this repository and submit pull requests for improvements. Some areas where contributions would be welcome:
- Bug fixes and optimizations
- New features and game mechanics
- Code documentation improvements
- Additional levels and content

---

Enjoy playing PacMan! 🟡👻