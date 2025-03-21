# Window settings
WIDTH = 920
HEIGHT = 600
FPS = 60

# Game settings
PLAYER_SIZE_WIDTH = 100
PLAYER_SIZE_HEIGHT = 60
BUG_SIZE = 20
BASE_PLAYER_SPEED = 3  # Reduced from 5 (40% slower)
BOOSTED_PLAYER_SPEED = 3.9  # Reduced from 6.5 (40% slower)
NORMAL_BUG_SPEED = 3
GOLDEN_BUG_SPEED = 5
POWER_BUG_SPEED = 4
GRAVITY = 0.238
JUMP_FORCE = -10
POWER_UP_DURATION = 5 * 60  # 5 seconds (60 frames per second)

# Power-up durations
SPEED_POWER_DURATION = 5 * 60  # 5 seconds for speed boost
GOLDEN_POWER_DURATION = 5 * 60  # 5 seconds for black bug immunity

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 155, 0)
GOLD = (255, 215, 0)
BLUE = (0, 191, 255)

# Background dimensions
BACKGROUND_WIDTH = 920
BACKGROUND_HEIGHT = 600

# Score thresholds for speed increases
SPEED_THRESHOLD_1 = 20
SPEED_THRESHOLD_2 = 50
SPEED_THRESHOLD_3 = 100
SPEED_THRESHOLD_4 = 150

# Speed multipliers for each threshold
SPEED_MULTIPLIER_1 = 1.2
SPEED_MULTIPLIER_2 = 1.5
SPEED_MULTIPLIER_3 = 1.8
SPEED_MULTIPLIER_4 = 2.0

# Add with other bug constants
BLACK_BUG_SPEED = 4
BLACK_BUG_SPAWN_THRESHOLD = 15  # Changed from 30 to 15 points
BLACK_BUG_SPAWN_INTERVAL = 30   # Points needed for additional black bugs

# Power bug timing (in frames)
POWER_BUG_MIN_SPAWN_TIME = 5 * 60  # Minimum 5 seconds between spawns
POWER_BUG_MAX_SPAWN_TIME = 15 * 60  # Maximum 15 seconds between spawns
GOLDEN_BUG_MIN_SPAWN_TIME = 8 * 60  # Minimum 8 seconds between spawns
GOLDEN_BUG_MAX_SPAWN_TIME = 20 * 60  # Maximum 20 seconds between spawns

# Regular bug spawn settings
NORMAL_BUG_POINTS_THRESHOLD = 10  # Points needed for additional bug
NORMAL_BUG_MAX_COUNT = 10  # Maximum number of normal bugs allowed 