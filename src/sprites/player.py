import pygame
from ..utils.constants import WIDTH, HEIGHT, PLAYER_SIZE_WIDTH, PLAYER_SIZE_HEIGHT, BASE_PLAYER_SPEED, GRAVITY, JUMP_FORCE
from ..utils.image_processor import load_and_clean_sprite

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.load_image()
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        
        # Movement properties
        self.velocity_x = 0
        self.velocity_y = 0
        self.speed = BASE_PLAYER_SPEED
        self.facing_right = False
        self.is_grounded = False  # New property to track if player is on ground

    def load_image(self):
        try:
            self.image = load_and_clean_sprite("player.png", (PLAYER_SIZE_WIDTH, PLAYER_SIZE_HEIGHT))
            if self.image:
                self.image = pygame.transform.flip(self.image, True, False)
            else:
                raise Exception("Image loading failed")
        except:
            print("Could not load player image, using default shape")
            self.image = self.create_player_surface()

    def create_player_surface(self):
        surface = pygame.Surface((PLAYER_SIZE_WIDTH, PLAYER_SIZE_HEIGHT), pygame.SRCALPHA)
        pygame.draw.circle(surface, (200, 200, 200), 
                          (PLAYER_SIZE_WIDTH//2, PLAYER_SIZE_HEIGHT//2), 
                          min(PLAYER_SIZE_WIDTH, PLAYER_SIZE_HEIGHT)//2)
        pygame.draw.polygon(surface, (200, 200, 200), [
            (PLAYER_SIZE_WIDTH//4, PLAYER_SIZE_HEIGHT//4), 
            (PLAYER_SIZE_WIDTH//2, 0), 
            (3*PLAYER_SIZE_WIDTH//4, PLAYER_SIZE_HEIGHT//4)
        ])
        pygame.draw.polygon(surface, (200, 200, 200), [
            (PLAYER_SIZE_WIDTH//2, PLAYER_SIZE_HEIGHT//4), 
            (3*PLAYER_SIZE_WIDTH//4, 0), 
            (PLAYER_SIZE_WIDTH, PLAYER_SIZE_HEIGHT//4)
        ])
        return surface

    def handle_event(self, event):
        """Handle jump events - can jump even when grounded"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.velocity_y = JUMP_FORCE
                self.is_grounded = False  # Ensure we're not grounded when jumping

    def update(self):
        # Handle continuous keyboard input
        keys = pygame.key.get_pressed()
        
        # Only allow horizontal movement when in the air (not grounded)
        # This simulates swimming/floating movement for the fish
        if not self.is_grounded:
            # Handle keyboard input
            if keys[pygame.K_LEFT]:
                self.velocity_x = -self.speed
                self.facing_right = False
            elif keys[pygame.K_RIGHT]:
                self.velocity_x = self.speed
                self.facing_right = True
            
            # Update position based on velocity (whether from keys or test)
            self.rect.x += self.velocity_x
        else:
            # No horizontal movement when on ground
            self.velocity_x = 0

        # Handle vertical movement
        self.velocity_y += GRAVITY
        next_y = self.rect.y + self.velocity_y
        
        # Check if we'll hit the floor
        if next_y + self.rect.height >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.is_grounded = True  # Set grounded state
            # Only reset velocity if we're moving downward
            if self.velocity_y > 0:
                self.velocity_y = 0
        else:
            self.rect.y = next_y
            self.is_grounded = False  # Set not grounded when in air

        # Top boundary collision
        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocity_y = 1

        # Side boundaries collision
        if self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.right >= WIDTH:
            self.rect.right = WIDTH

    def draw(self, screen):
        if self.facing_right:
            flipped_image = pygame.transform.flip(self.image, True, False)
            screen.blit(flipped_image, self.rect)
        else:
            screen.blit(self.image, self.rect) 