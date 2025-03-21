import pygame
import random
import math
from ..utils.constants import (WIDTH, HEIGHT, BUG_SIZE, NORMAL_BUG_SPEED, 
                             GOLDEN_BUG_SPEED, POWER_BUG_SPEED, BLACK_BUG_SPEED,
                             GREEN, GOLD, BLUE, BLACK)
from ..utils.image_processor import load_and_clean_sprite

class Bug(pygame.sprite.Sprite):
    def __init__(self, bug_type="normal"):
        super().__init__()
        self.bug_type = bug_type
        
        # Set type-specific properties
        if bug_type == "black":
            self.speed = BLACK_BUG_SPEED
            self.points = 0  # Deadly, no points
            self.change_interval = random.randint(30, 60)
        elif bug_type == "golden":
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
        
        # Try to load images with transparency
        self.load_image()
        
        self.rect = self.image.get_rect()
        self.reset_position()
        self.angle = random.uniform(0, 2 * math.pi)
        self.movement_timer = 0

    def create_bug_surface(self):
        # Create a surface with alpha channel for smooth edges
        surface = pygame.Surface((BUG_SIZE, BUG_SIZE), pygame.SRCALPHA)
        
        # Calculate dimensions
        center = (BUG_SIZE//2, BUG_SIZE//2)
        body_radius = BUG_SIZE//2
        wing_width = BUG_SIZE//2
        wing_height = BUG_SIZE//3
        
        # Draw main body (circle)
        pygame.draw.circle(surface, self.color, center, body_radius - 1)  # -1 for smoother edge
        
        # Draw wings with more rounded edges
        left_wing = pygame.Rect(0, BUG_SIZE//4, wing_width, wing_height)
        right_wing = pygame.Rect(BUG_SIZE//2, BUG_SIZE//4, wing_width, wing_height)
        
        # Darker color for wings
        wing_color = (self.color[0]//2, self.color[1]//2, self.color[2]//2)
        
        # Draw elliptical wings
        pygame.draw.ellipse(surface, wing_color, left_wing)
        pygame.draw.ellipse(surface, wing_color, right_wing)
        
        # Add highlights for depth
        highlight_radius = 2
        highlight_pos = (center[0] - body_radius//3, center[1] - body_radius//3)
        highlight_color = (min(self.color[0] + 50, 255), 
                          min(self.color[1] + 50, 255), 
                          min(self.color[2] + 50, 255))
        pygame.draw.circle(surface, highlight_color, highlight_pos, highlight_radius)
        
        return surface

    def reset_position(self):
        self.rect.x = random.randint(0, WIDTH - BUG_SIZE)
        self.rect.y = random.randint(0, HEIGHT - BUG_SIZE)
        
    def update(self):
        self.movement_timer += 1
        if self.movement_timer >= self.change_interval:
            self.angle = random.uniform(0, 2 * math.pi)
            self.movement_timer = 0

        self.rect.x += math.cos(self.angle) * self.speed
        self.rect.y += math.sin(self.angle) * self.speed

        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.angle = math.pi - self.angle
            self.rect.x = max(0, min(self.rect.x, WIDTH - BUG_SIZE))
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.angle = -self.angle
            self.rect.y = max(0, min(self.rect.y, HEIGHT - BUG_SIZE))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def load_image(self):
        try:
            image_paths = {
                "normal": "bug.png",
                "golden": "golden.png",
                "power": "power.png",
                "black": "black.png"
            }
            
            image_path = image_paths.get(self.bug_type, "bug.png")
            self.image = load_and_clean_sprite(image_path, (BUG_SIZE, BUG_SIZE))
            
            if not self.image:
                raise Exception("Image loading failed")
        except:
            print(f"Could not load {self.bug_type} bug image, using default shape")
            self.image = self.create_bug_surface() 