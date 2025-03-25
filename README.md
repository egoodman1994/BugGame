# Bug Catcher Game 🎮🐛

A fun PyGame where you control a player trying to catch different types of bugs. Each bug type offers different rewards and challenges!

## 🎮 Game Features

- **Three Bug Types:**
  - 🟢 Green Bugs (Normal) = 1 point
  - 🌟 Golden Bugs = 5 points
  - 🔵 Blue Bugs = Speed power-up

- **Dynamic Difficulty:**
  - Bugs speed up as your score increases
  - Speed thresholds at 20, 50, 100, and 150 points
  - Each level makes bugs progressively faster

- **Movement Mechanics:**
  - Double jump capability
  - Left/Right movement
  - Speed power-ups from blue bugs

## 🛠️ Installation

### Using Virtual Environment (Recommended)
1. **Prerequisites:**
   ```bash
   # Make sure you have Python 3.7+ installed
   python3 --version

   # Make sure you have Node.js and npm installed
   node --version
   npm --version
   ```

2. **Setup:**
   ```bash
   # Clone or download the game files
   git clone https://github.com/yourusername/cat-and-bugs-game.git
   cd cat-and-bugs-game
   
   # Setup virtual environment and install dependencies
   # On macOS/Linux:
   npm run setup
   
   # On Windows:
   npm run setup-win
   ```

3. **Run the game:**
   ```bash
   npm start
   ```

### Troubleshooting Installation
If you encounter any issues:
1. Make sure you're not in any virtual environment when starting the installation (run `deactivate` if needed)
2. You can manually set up the environment:
   ```bash
   # Create and activate virtual environment
   python3 -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   
   # Install dependencies
   python3 -m pip install -r requirements.txt
   ```
3. After manual setup, you can still use `npm start` to run the game

## 🎯 How to Play

### Controls:
- **←/→ Arrow Keys**: Move left/right
- **Spacebar**: Jump
- **Close Window**: Quit game

### Movement Mechanics:
- The fish can only move left/right while in the air
- Jump to start swimming/moving
- This creates a fluid, swimming-like motion
- Must jump off the ground to initiate movement

### Scoring:
- Catch green bugs for 1 point
- Catch golden bugs for 5 points
- Catch blue bugs for temporary speed boost

### Power-ups:
- Blue bugs give 5-second speed boosts
- Speed boost helps catch other bugs more easily

### Difficulty Progression:
- Score 20: Bugs move 20% faster
- Score 50: Bugs move 50% faster
- Score 100: Bugs move 80% faster
- Score 150: Bugs move twice as fast

## 🎨 Customization

You can customize the game by adding your own images in the `assets/images/` folder:
- `player.png`: Your custom player sprite
- `bug.png`: Normal bug sprite
- `golden.png`: Golden bug sprite
- `power.png`: Power-up bug sprite
- `background.png`: Game background

Images will automatically scale to fit the game's dimensions.

## 📊 Game Stats Display

The game shows various information on screen:
- Current Score
- Remaining Jumps
- Active Speed Boost timer
- Current Speed Level (when bugs are faster)

## 🐞 Troubleshooting

If you encounter issues:
1. Verify Python version is 3.7+
2. Ensure pygame is installed correctly
3. Check that all game files are in the correct directory structure
4. Make sure you're running from the game's root directory

## 🎮 Tips

1. Use double jumps to reach high-flying bugs
2. Prioritize golden bugs for quick score increases
3. Use speed boosts strategically
4. Watch for increasing difficulty as your score grows

## Testing

The game includes a comprehensive test suite using pytest. To run the tests:

```bash
# Run all tests
npm run test
```

### Test Coverage
- Player movement and collision detection
- Bug behavior and spawning mechanics
- Game state management
- Power-up system
- Score tracking and leaderboard

## Building Executable

To create a standalone executable:
```bash
npm run build  # For Unix/Mac
npm run build-win  # For Windows
```

Enjoy playing! 🎮✨ 