import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH = 800
HEIGHT = 600
CAT_SIZE = 50
BUG_SIZE = 20
BASE_CAT_SPEED = 5
BOOSTED_CAT_SPEED = 8
NORMAL_BUG_SPEED = 3
GOLDEN_BUG_SPEED = 5
POWER_BUG_SPEED = 4
GRAVITY = 0.5
JUMP_FORCE = -10
POWER_UP_DURATION = 5 * 60  # 5 seconds (60 frames per second)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 155, 0)
GOLD = (255, 215, 0)
BLUE = (0, 191, 255)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cat and Bugs Game")

# Create a simple cat image using basic shapes
def create_cat_surface():
    surface = pygame.Surface((CAT_SIZE, CAT_SIZE), pygame.SRCALPHA)
    pygame.draw.circle(surface, (200, 200, 200), (CAT_SIZE//2, CAT_SIZE//2), CAT_SIZE//2)
    pygame.draw.polygon(surface, (200, 200, 200), [
        (CAT_SIZE//4, CAT_SIZE//4), 
        (CAT_SIZE//2, 0), 
        (3*CAT_SIZE//4, CAT_SIZE//4)
    ])
    pygame.draw.polygon(surface, (200, 200, 200), [
        (CAT_SIZE//2, CAT_SIZE//4), 
        (3*CAT_SIZE//4, 0), 
        (CAT_SIZE, CAT_SIZE//4)
    ])
    return surface

# Create bug surfaces
def create_bug_surface(color):
    surface = pygame.Surface((BUG_SIZE, BUG_SIZE), pygame.SRCALPHA)
    pygame.draw.circle(surface, color, (BUG_SIZE//2, BUG_SIZE//2), BUG_SIZE//2)
    pygame.draw.ellipse(surface, (color[0]//2, color[1]//2, color[2]//2), 
                       (0, BUG_SIZE//4, BUG_SIZE//2, BUG_SIZE//2))
    pygame.draw.ellipse(surface, (color[0]//2, color[1]//2, color[2]//2), 
                       (BUG_SIZE//2, BUG_SIZE//4, BUG_SIZE//2, BUG_SIZE//2))
    return surface

# Bug class
class Bug:
    def __init__(self, bug_type="normal"):
        self.bug_type = bug_type
        if bug_type == "golden":
            self.speed = GOLDEN_BUG_SPEED
            self.points = 5
            self.change_interval = random.randint(30, 60)
        elif bug_type == "power":
            self.speed = POWER_BUG_SPEED
            self.points = 0
            self.change_interval = random.randint(45, 90)
        else:  # normal
            self.speed = NORMAL_BUG_SPEED
            self.points = 1
            self.change_interval = random.randint(60, 120)
            
        self.reset_position()
        self.angle = random.uniform(0, 2 * math.pi)
        self.movement_timer = 0

    def reset_position(self):
        self.x = random.randint(0, WIDTH - BUG_SIZE)
        self.y = random.randint(0, HEIGHT - BUG_SIZE)
        
    def move(self):
        self.movement_timer += 1
        if self.movement_timer >= self.change_interval:
            self.angle = random.uniform(0, 2 * math.pi)
            self.movement_timer = 0

        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed

        if self.x <= 0 or self.x >= WIDTH - BUG_SIZE:
            self.angle = math.pi - self.angle
            self.x = max(0, min(self.x, WIDTH - BUG_SIZE))
        if self.y <= 0 or self.y >= HEIGHT - BUG_SIZE:
            self.angle = -self.angle
            self.y = max(0, min(self.y, HEIGHT - BUG_SIZE))

# Cat properties
cat_x = WIDTH // 2
cat_y = HEIGHT // 2
cat_velocity_y = 0
cat_velocity_x = 0
cat_facing_right = True
jumps_remaining = 2
speed_boost_timer = 0
cat_speed = BASE_CAT_SPEED

# Initialize bugs
normal_bug = Bug("normal")
golden_bug = Bug("golden")
power_bug = Bug("power")

# Score
score = 0

# Initialize images
try:
    cat_image = pygame.image.load("cat.png")
    cat_image = pygame.transform.scale(cat_image, (CAT_SIZE, CAT_SIZE))
except:
    cat_image = create_cat_surface()

normal_bug_image = create_bug_surface(GREEN)
golden_bug_image = create_bug_surface(GOLD)
power_bug_image = create_bug_surface(BLUE)

# Font for display
font = pygame.font.Font(None, 36)

# Game loop
clock = pygame.time.Clock()

while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # Handle spacebar for jumping
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and jumps_remaining > 0:
                cat_velocity_y = JUMP_FORCE
                jumps_remaining -= 1

    # Update speed boost timer
    if speed_boost_timer > 0:
        speed_boost_timer -= 1
        cat_speed = BOOSTED_CAT_SPEED
        if speed_boost_timer == 0:
            cat_speed = BASE_CAT_SPEED

    # Handle continuous keyboard input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        cat_velocity_x = -cat_speed
        cat_facing_right = False
    elif keys[pygame.K_RIGHT]:
        cat_velocity_x = cat_speed
        cat_facing_right = True
    else:
        cat_velocity_x = 0

    # Update cat position
    cat_y += cat_velocity_y
    cat_x += cat_velocity_x
    
    # Apply gravity
    cat_velocity_y += GRAVITY

    # Bottom boundary collision
    if cat_y >= HEIGHT - CAT_SIZE:
        cat_y = HEIGHT - CAT_SIZE
        cat_velocity_y = 0
        jumps_remaining = 2

    # Side boundaries collision
    if cat_x <= 0:
        cat_x = 0
    elif cat_x >= WIDTH - CAT_SIZE:
        cat_x = WIDTH - CAT_SIZE

    # Update bug positions
    normal_bug.move()
    golden_bug.move()
    power_bug.move()

    # Check for collisions
    cat_rect = pygame.Rect(cat_x, cat_y, CAT_SIZE, CAT_SIZE)
    normal_bug_rect = pygame.Rect(normal_bug.x, normal_bug.y, BUG_SIZE, BUG_SIZE)
    golden_bug_rect = pygame.Rect(golden_bug.x, golden_bug.y, BUG_SIZE, BUG_SIZE)
    power_bug_rect = pygame.Rect(power_bug.x, power_bug.y, BUG_SIZE, BUG_SIZE)
    
    if cat_rect.colliderect(normal_bug_rect):
        score += normal_bug.points
        normal_bug = Bug("normal")
    
    if cat_rect.colliderect(golden_bug_rect):
        score += golden_bug.points
        golden_bug = Bug("golden")

    if cat_rect.colliderect(power_bug_rect):
        speed_boost_timer = POWER_UP_DURATION
        power_bug = Bug("power")

    # Clear the screen
    screen.fill(WHITE)

    # Draw the bugs
    screen.blit(normal_bug_image, (normal_bug.x, normal_bug.y))
    screen.blit(golden_bug_image, (golden_bug.x, golden_bug.y))
    screen.blit(power_bug_image, (power_bug.x, power_bug.y))

    # Draw the cat
    if cat_facing_right:
        screen.blit(cat_image, (int(cat_x), int(cat_y)))
    else:
        flipped_cat = pygame.transform.flip(cat_image, True, False)
        screen.blit(flipped_cat, (int(cat_x), int(cat_y)))

    # Draw the score
    score_text = font.render(f'Score: {score}', True, BLACK)
    screen.blit(score_text, (10, 10))

    # Draw jumps remaining
    jumps_text = font.render(f'Jumps: {jumps_remaining}', True, BLACK)
    screen.blit(jumps_text, (10, 50))

    # Draw speed boost timer
    if speed_boost_timer > 0:
        boost_text = font.render(f'Speed Boost: {speed_boost_timer // 60 + 1}s', True, BLUE)
        screen.blit(boost_text, (10, 90))

    # Update the display
    pygame.display.flip()

    # Control game speed
    clock.tick(60)
